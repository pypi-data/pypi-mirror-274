from typing import Annotated

from pydantic import BaseModel, Field


class Review(BaseModel):
    restaurantId: Annotated[
        int, Field(gt=0, title="Restaurant ID", description="Globally unique identifier of a given restaurant")
    ]
    reviewId: Annotated[
        int,
        Field(
            gt=0,
            title="Review ID",
            description="Identifier of a given review. Only unique within a given Restaurant ID",
        ),
    ]
    text: Annotated[str, Field(min_length=1, title="Text", description="Textual content of a review")]
    rating: Annotated[
        float, Field(ge=1, le=10, title="Rating", description="The rating given to this restaurant by this review.")
    ]
    publishedAt: Annotated[str, Field(title="Published At", description="The publication date of this review.")]


class ReviewAge(BaseModel):
    oldest: Annotated[
        int, Field(ge=0, title="Oldest Review", description="Age of the oldest review for this restaurant in days")
    ]
    newest: Annotated[
        int, Field(ge=0, title="Newest Review", description="Age of the newest review for this restaurant in days")
    ]
    average: Annotated[
        int, Field(ge=0, title="Average Review Age", description="Average age of reviews for this restaurant in days")
    ]


class RestaurantReviewAggregate(BaseModel):
    restaurantId: Annotated[
        int, Field(gt=0, title="Restaurant ID", description="Globally unique identifier of a given restaurant")
    ]
    reviewCount: Annotated[
        int, Field(gt=0, title="Review Count", description="Number of reviews given to a restaurant")
    ]
    averageRating: Annotated[
        float,
        Field(
            ge=1,
            le=10,
            title="Average Rating",
            description="The average rating given by all reviews of this restaurant",
        ),
    ]
    averageReviewLength: Annotated[
        float,
        Field(
            ge=1,
            title="Average Review Length",
            description="The average length of reviews for this restaurant measured by character count",
        ),
    ]
    reviewAge: ReviewAge
