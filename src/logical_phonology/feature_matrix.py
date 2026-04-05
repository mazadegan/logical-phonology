from collections import Counter
from typing import cast

import tomllib

from .errors import (
    DuplicateFeaturesError,
    InvalidElementTypeError,
    InvalidTypeError,
    MissingKeyError,
)


def load_feature_system(path: str) -> frozenset[str]:
    with open(path, "rb") as f:
        data: dict[str, object] = tomllib.load(f)
    if "features" not in data:
        raise MissingKeyError("features")
    if not isinstance(data["features"], list):
        raise InvalidTypeError("features", list)
    features = cast(list[object], data["features"])
    invalid: list[object] = [f for f in features if not isinstance(f, str)]
    if invalid:
        raise InvalidElementTypeError("features", str, invalid)
    feature_strings = cast(list[str], features)
    duplicates: set[str] = {
        k for k, v in Counter(feature_strings).items() if v > 1
    }
    if duplicates:
        raise DuplicateFeaturesError(frozenset(duplicates))
    return frozenset(feature_strings)
