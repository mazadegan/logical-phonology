from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logical_phonology.word import Word

from .errors import UnificationError
from .feature_value import FeatureValue


@dataclass(frozen=True)
class Segment:
    """An immutable feature bundle representing a phonological segment.

    Use `FeatureSystem.segment()` to construct. Direct construction is
    possible but bypasses feature validation.

    Attributes:
        features: An immutable mapping of feature names to FeatureValues.
    """

    features: Mapping[str, FeatureValue]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "features", MappingProxyType(dict(self.features))
        )

    def subtract(self, other: "Segment") -> "Segment":
        """A \\ B = {cF | cF ∈ A ∧ cF ∉ B}

        Returns a new segment containing all valued features from this segment
        that do not appear with the same value in `other`. Features with
        conflicting values are kept. Also available as the `-` operator.

        Args:
            other: The segment whose features are subtracted.

        Returns:
            A new Segment with the result of the subtraction.
        """
        return Segment(
            {
                k: v
                for k, v in self.features.items()
                if k not in other or other[k] != v
            }
        )

    def __sub__(self, other: "Segment") -> "Segment":
        """Subtract another segment's features from this one. See ``subtract``."""
        return self.subtract(other)

    def unify(self, other: "Segment") -> "Segment":
        """A ⊔ B = A ∪ {cF | cF ∈ B ∧ ¬cF ∉ A}

        Returns a new segment containing all features from this segment, plus
        any features from `other` that do not conflict. Conflicting features
        are silently ignored. Also available as the `|` operator.

        Args:
            other: The segment to unify with.

        Returns:
            A new Segment with the result of unification.
        """
        result = dict(self.features)
        for f, v in other.features.items():
            if f not in self.features:
                result[f] = v
            # if f in self.features and value differs, skip (lax)
        return Segment(result)

    def unify_strict(self, other: "Segment") -> "Segment":
        """Same as `unify`, but raises UnificationError on conflicting features.

        Args:
            other: The segment to unify with.

        Returns:
            A new Segment with the result of unification.

        Raises:
            UnificationError: If both segments specify conflicting values for
                the same feature.
        """  # noqa: E501
        result = dict(self.features)
        for f, v in other.features.items():
            if f not in self.features:
                result[f] = v
            elif self.features[f] != v:
                raise UnificationError(f, self.features[f], v)
        return Segment(result)

    def __or__(self, other: "Segment") -> "Segment":
        """Unify this segment with another. See ``unify``."""
        return self.unify(other)

    def project(self, restricted_feature_set: frozenset[str]) -> "Segment":
        """Return a new segment containing only the specified features.

        Also available as the `&` operator.

        Args:
            restricted_feature_set: The set of feature names to keep.

        Returns:
            A new Segment containing only the features in `restricted_feature_set`.
        """  # noqa: E501
        return Segment(
            {
                k: v
                for k, v in self.features.items()
                if k in restricted_feature_set
            }
        )

    def __and__(self, restricted_feature_set: frozenset[str]) -> "Segment":
        """Project this segment onto a feature set. See ``project``."""
        return self.project(restricted_feature_set)

    # dict are not hashable, must use frozenset of features' items
    def __hash__(self) -> int:
        """Hash based on the feature bundle."""
        return hash((frozenset(self.features.items())))

    def __getitem__(self, key: str) -> FeatureValue:
        """Look up the value of a feature by name."""
        return self.features[key]

    def __contains__(self, item: str) -> bool:
        """Return True if this segment has a value for the given feature name."""
        return item in self.features

    def __str__(self) -> str:
        """Return the canonical string representation of the segment.

        Features are sorted alphabetically and formatted as `{+F1-F2}`.
        This canonical form is used as the name for aliased segments in
        an Inventory.
        """
        parts = sorted(f"{v}{f}" for f, v in self.features.items())
        return "{" + "".join(parts) + "}"

    def __add__(self, other: "Segment | Word") -> "Word":
        """Concatenate this segment with another segment or word.

        Args:
            other: A Segment or Word to append.

        Returns:
            A new Word with this segment followed by the segments of other.

        Note:
            Boundaries are not checked — callers are responsible for
            ensuring BOS and EOS appear only at the edges of the final word.
        """
        from logical_phonology.word import Word

        if isinstance(other, Segment):
            return Word((self, other))
        return Word((self,) + other.segments)
