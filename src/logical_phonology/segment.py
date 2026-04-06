from dataclasses import dataclass
from enum import Enum

from .errors import (
    InvalidFeatureValueError,
    UnknownFeatureError,
)


class FeatureValue(Enum):
    POS = "+"
    NEG = "-"
    UND = "0"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_str(cls, s: str) -> "FeatureValue":
        for member in cls:
            if member.value == s:
                return member
        raise InvalidFeatureValueError(s)


@dataclass(frozen=True)
class Segment:
    features: dict[str, FeatureValue]

    # dict are not hashable, must use frozenset of features' items
    def __hash__(self) -> int:
        return hash((frozenset(self.features.items())))


@dataclass(frozen=True)
class SegmentFactory:
    valid_features: frozenset[str]

    def create(self, features: dict[str, FeatureValue]) -> Segment:
        unknown = features.keys() - self.valid_features
        if unknown:
            raise UnknownFeatureError(unknown)
        # Forces underspecification to be explicit for segments.
        complete = {
            f: features.get(f, FeatureValue.UND) for f in self.valid_features
        }
        return Segment(complete)
