from dataclasses import dataclass

from .errors import UnificationError
from .feature_value import FeatureValue


@dataclass(frozen=True)
class Segment:
    """
    A consistent feature bundle. Use FeatureSystem.segment() to construct.
    """

    features: dict[str, FeatureValue]

    def subtract(self, other: "Segment") -> "Segment":
        """A \\ B = {cF | cF ∈ A ∧ cF ∉ B}"""
        return Segment(
            {
                k: v
                for k, v in self.features.items()
                if k not in other or other[k] != v
            }
        )

    def __sub__(self, other: "Segment") -> "Segment":
        return self.subtract(other)

    def unify(self, other: "Segment") -> "Segment":
        """A ⊔ B = A ∪ {cF | cF ∈ B ∧ ¬cF ∉ A}"""
        result = dict(self.features)
        for f, v in other.features.items():
            if f not in self.features:
                result[f] = v
            # if f in self.features and value differs, skip (lax)
        return Segment(result)

    def unify_strict(self, other: "Segment") -> "Segment":
        """Same as unify, but raises UnificationError on unification failure"""
        result = dict(self.features)
        for f, v in other.features.items():
            if f not in self.features:
                result[f] = v
            elif self.features[f] != v:
                raise UnificationError(f, self.features[f], v)
        return Segment(result)

    def __or__(self, other: "Segment") -> "Segment":
        return self.unify(other)

    def project(self, restricted_feature_set: frozenset[str]) -> "Segment":
        return Segment(
            {
                k: v
                for k, v in self.features.items()
                if k in restricted_feature_set
            }
        )

    def __and__(self, restricted_feature_set: frozenset[str]) -> "Segment":
        return self.project(restricted_feature_set)

    # dict are not hashable, must use frozenset of features' items
    def __hash__(self) -> int:
        return hash((frozenset(self.features.items())))

    def __getitem__(self, key: str) -> FeatureValue:
        return self.features[key]

    def __contains__(self, item: str) -> bool:
        return item in self.features
