from dataclasses import dataclass
from enum import Enum

from .errors import (
    InvalidFeatureValueError,
    InvalidSegmentNameError,
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
    name: str
    features: dict[str, FeatureValue]

    # dict are not hashable, must use frozenset of features' items
    def __hash__(self) -> int:
        return hash((self.name, frozenset(self.features.items())))


@dataclass(frozen=True)
class SegmentFactory:
    valid_features: frozenset[str]

    def create(self, name: str, features: dict[str, FeatureValue]) -> Segment:
        if name == "":
            raise InvalidSegmentNameError(name)
        # Disallows unknown features
        unknown = features.keys() - self.valid_features
        if unknown:
            raise UnknownFeatureError(unknown)
        # Forces underspecification to be explicit.
        complete = {
            f: features.get(f, FeatureValue.UND) for f in self.valid_features
        }
        return Segment(name, complete)
