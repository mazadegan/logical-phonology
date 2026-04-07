from dataclasses import dataclass

from .errors import UnknownFeatureError
from .feature_value import FeatureValue
from .natural_class import NaturalClass
from .segment import Segment
from .word import ReservedSymbol, Word


@dataclass(frozen=True)
class FeatureSystem:
    valid_features: frozenset[str]

    def segment(self, features: dict[str, FeatureValue]) -> Segment:
        unknown = features.keys() - self.valid_features
        if unknown:
            raise UnknownFeatureError(unknown)
        return Segment(features)

    def natural_class(self, features: dict[str, FeatureValue]) -> NaturalClass:
        unknown = features.keys() - self.valid_features
        if unknown:
            raise UnknownFeatureError(unknown)
        size = 3 ** (len(self.valid_features) - len(features))
        return NaturalClass(features, size)

    def word(self, segments: list[Segment]) -> Word:
        symbols: list[Segment | ReservedSymbol] = (
            [ReservedSymbol.BOS] + segments + [ReservedSymbol.EOS]
        )
        return Word(tuple(symbols))
