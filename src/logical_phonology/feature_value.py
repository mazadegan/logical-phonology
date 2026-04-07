from enum import Enum

from .errors import InvalidFeatureValueError


class FeatureValue(Enum):
    POS = "+"
    NEG = "-"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_str(cls, s: str) -> "FeatureValue":
        for member in cls:
            if member.value == s:
                return member
        raise InvalidFeatureValueError(s)


POS = FeatureValue.POS
NEG = FeatureValue.NEG
