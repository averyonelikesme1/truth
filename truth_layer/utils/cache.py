from pathlib import Path
import json
import hashlib


CACHE_DIR = Path(
    "cache"
)

CACHE_DIR.mkdir(
    exist_ok=True
)


def get_cache_key(
    text: str
) -> str:

    return hashlib.md5(
        text.encode()
    ).hexdigest()


def save_cache(
    key: str,
    data: dict
):

    file_path = (
        CACHE_DIR /
        f"{key}.json"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )


def load_cache(
    key: str
):

    file_path = (
        CACHE_DIR /
        f"{key}.json"
    )

    if not file_path.exists():
        return None

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)