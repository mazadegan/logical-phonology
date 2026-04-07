from dataclasses import dataclass

from .errors import ReservedFeatureError, UnknownFeatureError
from .feature_value import FeatureValue
from .natural_class import NaturalClass
from .natural_class_sequence import NaturalClassSequence
from .segment import Segment
from .word import Word

RESERVED_FEATURES = frozenset(["BOS", "EOS"])


@dataclass(frozen=True)
class FeatureSystem:
    valid_features: frozenset[str]

    def __post_init__(self) -> None:
        reserved_conflicts = self.valid_features & RESERVED_FEATURES
        if reserved_conflicts:
            raise ReservedFeatureError(reserved_conflicts)

    @property
    def BOS(self) -> Segment:
        return Segment({"BOS": FeatureValue.POS})

    @property
    def EOS(self) -> Segment:
        return Segment({"EOS": FeatureValue.POS})

    def segment(self, features: dict[str, FeatureValue]) -> Segment:
        unknown = (features.keys() - self.valid_features) - RESERVED_FEATURES
        if unknown:
            raise UnknownFeatureError(unknown)
        return Segment(features)

    def word(self, segments: list[Segment]) -> Word:
        return Word(tuple(segments))

    def add_boundaries(self, word: Word) -> Word:
        return Word(tuple([self.BOS, *word, self.EOS]))

    def natural_class(self, features: dict[str, FeatureValue]) -> NaturalClass:
        unknown = (features.keys() - self.valid_features) - RESERVED_FEATURES
        if unknown:
            raise UnknownFeatureError(unknown)
        return NaturalClass(features)

    def natural_class_sequence(
        self, classes: list[NaturalClass]
    ) -> NaturalClassSequence:
        return NaturalClassSequence(tuple(classes))
