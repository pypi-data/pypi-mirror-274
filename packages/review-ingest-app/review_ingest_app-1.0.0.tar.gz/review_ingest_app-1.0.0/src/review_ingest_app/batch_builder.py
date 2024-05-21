import json
import os
from copy import deepcopy
from datetime import datetime, timedelta, timezone

from pydantic import ValidationError
from tqdm import tqdm

from review_ingest_app.data.data_models import (
    RestaurantReviewAggregate,
    Review,
    ReviewAge,
)
from review_ingest_app.utils import (
    convert_str_to_datetime,
    is_inappropriate,
    load_inappropriate_words,
    write_to_jsonl,
)


class BatchBuilder:
    def __init__(self, raw_file_dir, batch_size):
        self.directory = raw_file_dir
        self.chunk_size = batch_size

    def _read_jsonl_file(self, file_path):
        with open(file_path, "r") as file:
            for line in file:
                yield json.loads(line)

    def _get_jsonl_files(self):
        for file_name in os.listdir(self.directory):
            if file_name.endswith(".jsonl"):
                yield os.path.join(self.directory, file_name)

    def load_reviews(self):
        reviews_batch = []
        for file_path in self._get_jsonl_files():
            for review in self._read_jsonl_file(file_path):
                try:
                    reviews_batch.append(Review(**review))
                except ValidationError as e:
                    # Handle the ValidationError here
                    print("Validation Error occurred:")
                    for error in e.errors():
                        print(f"- {error['msg']}")
                    continue

                if len(reviews_batch) == self.chunk_size:
                    yield reviews_batch
                    reviews_batch = []
        yield reviews_batch


class BatchValidator:
    restaurant_metrics = {}

    def __init__(
        self,
        inappropriate_words_src_path: str,
        inappropriate_words_thresh_in_pct: int,
        aggregated_metrics_out: str,
        review_age_limit_in_yrs: int,
        validated_reviews: str,
        default_tz: str,
        fuzzy_match_thresh: int,
    ) -> None:
        self.inappropriate_words = load_inappropriate_words(inappropriate_words_src_path)  # Read the file
        self.inappropriate_words_thresh_in_pct = inappropriate_words_thresh_in_pct
        self.review_age_limit_in_yrs = review_age_limit_in_yrs
        self.validated_reviews = validated_reviews
        self.default_tz = default_tz
        self.aggregated_metrics_out = aggregated_metrics_out
        self.fuzzy_match_thresh = fuzzy_match_thresh
        self.agg_metrics = {"total_reviews": 0, "total_score": 0.0, "total_review_len": 0.0, "review_age": []}

    def process_reviews(self, reviews):
        processed_reviews = []
        current_date = datetime.now().replace(tzinfo=timezone.utc)

        for review in tqdm(reviews, desc="Processing reviews"):
            review_age = current_date - convert_str_to_datetime(review.publishedAt, default_tz=self.default_tz)
            if review_age > timedelta(days=3 * 365):
                continue  # Review validation 1 : Reject reviews older than 3 years

            words = review.text.split()
            inappropriate_count = sum(
                1
                for word in words
                if is_inappropriate(word.strip().lower(), self.inappropriate_words, self.fuzzy_match_thresh)
            )
            if inappropriate_count / len(words) > 0.2:
                continue  # Review validation 2 : Reject if inappropriate words are more than 20%

            review.text = " ".join(
                "****"
                if is_inappropriate(word.strip().lower(), self.inappropriate_words, self.fuzzy_match_thresh)
                else word
                for word in words
            )
            processed_reviews.append(review)

            # Aggregations
            self.update_agg_metrics(review, current_date)

        write_to_jsonl(processed_reviews, self.validated_reviews)
        return processed_reviews

    def update_agg_metrics(self, review, current_date):
        if review.restaurantId not in BatchValidator.restaurant_metrics:
            BatchValidator.restaurant_metrics[review.restaurantId] = deepcopy(self.agg_metrics)
        BatchValidator.restaurant_metrics[review.restaurantId]["total_reviews"] += 1
        BatchValidator.restaurant_metrics[review.restaurantId]["total_score"] += review.rating
        BatchValidator.restaurant_metrics[review.restaurantId]["total_review_len"] += len(
            review.text
        )  # Total number of characters
        review_age = current_date - convert_str_to_datetime(review.publishedAt, default_tz=self.default_tz)
        BatchValidator.restaurant_metrics[review.restaurantId]["review_age"].append(review_age.days)

    def compute_metrics(self):
        for r_id, r_data in BatchValidator.restaurant_metrics.items():
            r_age = ReviewAge(
                oldest=max(r_data["review_age"]),
                newest=min(r_data["review_age"]),
                average=sum(r_data["review_age"]) // len(r_data["review_age"]),
            )
            agg_obj = RestaurantReviewAggregate(
                restaurantId=r_id,
                reviewCount=r_data["total_reviews"],
                averageRating=r_data["total_score"] / r_data["total_reviews"],
                averageReviewLength=r_data["total_review_len"] / r_data["total_reviews"],
                reviewAge=r_age,
            )
            write_to_jsonl(agg_obj, self.aggregated_metrics_out)


if __name__ == "__main__":
    pass
