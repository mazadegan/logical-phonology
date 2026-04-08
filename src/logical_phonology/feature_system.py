from dataclasses import dataclass

from .errors import (
    ReservedFeatureError,
    ReservedFeatureUsageError,
    UnknownFeatureError,
)
from .feature_value import FeatureValue
from .inventory import Inventory
from .natural_class import NaturalClass
from .natural_class_sequence import NaturalClassSequence
from .segment import Segment
from .word import Word

RESERVED_FEATURES = frozenset(["BOS", "EOS"])


@dataclass(frozen=True)
class FeatureSystem:
    """The central factory object for all Logical Phonology primitives.

    A `FeatureSystem` defines the universal set of valid features for an
    analysis. All LP objects — segments, natural classes, natural class
    sequences, words, and inventories — are constructed through a
    `FeatureSystem` instance, ensuring that feature validity is enforced
    at construction time.

    The feature names `'BOS'` and `'EOS'` are reserved and cannot be used
    in user-defined feature systems.

    Attributes:
        valid_features: The frozenset of valid feature names for this system.

    Raises:
        ReservedFeatureError: If any feature name in `valid_features` is
            reserved.
    """

    valid_features: frozenset[str]

    def __post_init__(self) -> None:
        reserved_conflicts = self.valid_features & RESERVED_FEATURES
        if reserved_conflicts:
            raise ReservedFeatureError(reserved_conflicts)

    @property
    def BOS(self) -> Segment:
        """The beginning-of-string boundary pseudo-segment (⋉).

        This is a reserved segment with a single feature `{'BOS': POS}`.
        It is automatically added by `add_boundaries()` and recognized
        by `Inventory.tokenize()` and `Inventory.render()`.
        """
        return Segment({"BOS": FeatureValue.POS})

    @property
    def EOS(self) -> Segment:
        """The end-of-string boundary pseudo-segment (⋊).

        This is a reserved segment with a single feature `{'EOS': POS}`.
        It is automatically added by `add_boundaries()` and recognized
        by `Inventory.tokenize()` and `Inventory.render()`.
        """
        return Segment({"EOS": FeatureValue.POS})

    def segment(self, features: dict[str, FeatureValue]) -> Segment:
        """Construct a Segment from a feature specification.

        Args:
            features: A mapping of feature names to FeatureValues. May be
                partial — unspecified features are simply absent from the
                segment's feature bundle.

        Returns:
            A new Segment with the given feature specification.

        Raises:
            ReservedFeatureUsageError: If any feature name is reserved.
            UnknownFeatureError: If any feature name is not in `valid_features`.
        """  # noqa: E501
        reserved_used = features.keys() & RESERVED_FEATURES
        if reserved_used:
            raise ReservedFeatureUsageError(frozenset(reserved_used))
        unknown = features.keys() - self.valid_features
        if unknown:
            raise UnknownFeatureError(unknown)
        return Segment(features)

    def word(self, segments: list[Segment]) -> Word:
        """Construct a Word from a list of segments.

        Args:
            segments: An ordered list of Segment objects.

        Returns:
            A new Word containing the given segments.
        """
        return Word(tuple(segments))

    def add_boundaries(self, word: Word) -> Word:
        """Return a new Word with BOS and EOS boundary pseudo-segments added.

        Args:
            word: The word to add boundaries to.

        Returns:
            A new Word with `BOS` prepended and `EOS` appended.
        """
        return Word(tuple([self.BOS, *word, self.EOS]))

    def natural_class(self, features: dict[str, FeatureValue]) -> NaturalClass:
        """Construct a NaturalClass from a feature specification.

        Natural classes may reference reserved features such as 'BOS' and 'EOS'
        to match boundary pseudo-segments.

        Args:
            features: A partial mapping of feature names to FeatureValues
                defining the class.

        Returns:
            A new NaturalClass with the given feature specification.

        Raises:
            UnknownFeatureError: If any feature name is not in `valid_features`
                and is not a reserved feature.
        """
        unknown = (features.keys() - self.valid_features) - RESERVED_FEATURES
        if unknown:
            raise UnknownFeatureError(unknown)
        return NaturalClass(features)

    def natural_class_sequence(
        self, classes: list[NaturalClass]
    ) -> NaturalClassSequence:
        """Construct a NaturalClassSequence from an ordered list of natural
        classes.

        Args:
            classes: An ordered list of NaturalClass objects.

        Returns:
            A new NaturalClassSequence containing the given natural classes.
        """
        return NaturalClassSequence(tuple(classes))

    def inventory(
        self, name_to_segment: dict[str, Segment], allow_aliases: bool = True
    ) -> Inventory:
        """Construct an Inventory from a mapping of names to segments.

        Args:
            name_to_segment: A mapping of symbol names to Segment objects.
                Multiple names may map to the same segment (aliases).
            allow_aliases: If True (default), multiple names may map to the
                same segment. If False, raises AliasError if aliases are
                detected.

        Returns:
            A new Inventory with the given named segments.

        Raises:
            AliasError: If aliases are detected and `allow_aliases=False`.
            DuplicateNameError: If any name collides with a reserved or
                canonical form name.
        """
        return Inventory(self, name_to_segment, allow_aliases=allow_aliases)
