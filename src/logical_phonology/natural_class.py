from dataclasses import dataclass

from .errors import UnknownFeatureError
from .segment import FeatureValue, Segment


@dataclass(frozen=True)
class NaturalClass:
    feature_specification: dict[str, FeatureValue]
    size: int

    def contains(self, s: Segment) -> bool:
        return all(
            s.features[f] == v for f, v in self.feature_specification.items()
        )

    def __hash__(self) -> int:
        return hash(frozenset(self.feature_specification.items()))

    def __len__(self) -> int:
        return self.size


@dataclass(frozen=True)
class NaturalClassFactory:
    valid_features: frozenset[str]

    def create(self, features: dict[str, FeatureValue]) -> NaturalClass:
        unknown = features.keys() - self.valid_features
        if unknown:
            raise UnknownFeatureError(unknown)
        size = 3 ** (len(self.valid_features) - len(features))
        return NaturalClass(features, size)
