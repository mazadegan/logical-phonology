from dataclasses import dataclass

from .feature_value import FeatureValue
from .segment import Segment


@dataclass(frozen=True)
class NaturalClass:
    feature_specification: dict[str, FeatureValue]

    def __contains__(self, s: Segment) -> bool:
        return self.feature_specification.items() <= s.features.items()

    def __hash__(self) -> int:
        return hash(frozenset(self.feature_specification.items()))
