from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, Iterator

from logical_phonology.natural_class_union import NaturalClassUnion

from .feature_value import FeatureValue
from .segment import Segment

if TYPE_CHECKING:
    from .inventory import Inventory


@dataclass(frozen=True)
class NaturalClass:
    """An immutable partial feature specification defining a set of segments.

    A natural class is defined by a set of features and their values.
    A segment belongs to a natural class if it has at least the feature
    values specified.

    Use `FeatureSystem.natural_class()` to construct.

    Attributes:
        feature_specification: An immutable mapping of feature names to
            FeatureValues defining the class.
    """

    feature_specification: Mapping[str, FeatureValue]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "feature_specification",
            MappingProxyType(dict(self.feature_specification)),
        )

    def over(
        self, inv: Inventory, filter_boundaries: bool = True
    ) -> Iterator[Segment]:
        """Iterate over all segments in this natural class over a given inventory.

        Args:
            inv: The inventory to evaluate the natural class over.
            filter_boundaries: If True (default), BOS and EOS pseudo-segments
                are excluded from the results.

        Returns:
            An iterator over all segments in the inventory that belong to
            this natural class.
        """  # noqa: E501
        return inv.iter_extension(self, filter_boundaries)

    def __contains__(self, s: Segment) -> bool:
        """Return True if the segment belongs to this natural class.

        A segment belongs to a natural class if its feature bundle contains
        all the feature-value pairs specified by the class. Also available
        via the `in` operator.

        Args:
            s: The segment to test for membership.

        Returns:
            True if the segment belongs to this natural class, False otherwise.
        """
        return self.feature_specification.items() <= s.features.items()

    def __hash__(self) -> int:
        """Hash based on the feature specification."""
        return hash(frozenset(self.feature_specification.items()))

    def __or__(self, other: NaturalClass) -> NaturalClassUnion:
        """Return a union of this natural class with another."""
        return NaturalClassUnion((self, other))
