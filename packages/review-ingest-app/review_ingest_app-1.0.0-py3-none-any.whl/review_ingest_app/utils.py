import json

import pytz
from dateutil.parser import parse
from rapidfuzz import fuzz, process
from tqdm import tqdm


def load_inappropriate_words(file_path):
    with open(file_path, "r") as file:
        words = [line.strip().lower() for line in file if line.strip()]
    return set(words)


def is_inappropriate(word, inappropriate_words_set, threshold=80):
    match = process.extractOne(word, inappropriate_words_set, scorer=fuzz.ratio)
    return match and match[1] >= threshold


def convert_str_to_datetime(date_str, default_time="00:00:00", default_tz="UTC"):
    return parse(date_str).replace(tzinfo=pytz.timezone(default_tz))


def write_to_jsonl(obj_to_store, path):
    # Unpack
    if isinstance(obj_to_store, list):
        for obj in tqdm(obj_to_store, desc="Unpacking jsons"):
            with open(path, "a") as file:
                json.dump(obj.dict(), file, indent=4)
    else:
        with open(path, "a") as file:
            json.dump(obj_to_store.dict(), file, indent=4)
