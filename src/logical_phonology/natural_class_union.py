from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterator, overload

if TYPE_CHECKING:
    from logical_phonology.inventory import Inventory
    from logical_phonology.natural_class import NaturalClass
    from logical_phonology.segment import Segment


@dataclass(frozen=True)
class NaturalClassUnion:
    classes: tuple[NaturalClass, ...]

    def __contains__(self, seg: Segment) -> bool:
        """Return True if the segment belongs to any class in this union."""
        return any(seg in nc for nc in self.classes)

    def over(
        self, inv: Inventory, filter_boundaries: bool = True
    ) -> Iterator[Segment]:
        """Iterate over all segments in this union over a given inventory.

        Args:
            inv: The inventory to evaluate the union over.
            filter_boundaries: If True (default), BOS and EOS pseudo-segments
                are excluded from the results.

        Returns:
            An iterator over all segments in the inventory that belong to this
            union.
        """
        for seg in inv.segment_to_name:
            if seg in self:
                if not filter_boundaries or seg not in (
                    inv.feature_system.BOS,
                    inv.feature_system.EOS,
                ):
                    yield seg

    def extension(
        self,
        inv: Inventory,
        filter_boundaries: bool = True,
        as_names: bool = False,
    ) -> tuple[Segment, ...] | tuple[str, ...]:
        """Return the materialized extension of this union over an inventory.

        Args:
            inv: The inventory to evaluate the union over.
            filter_boundaries: If True (default), BOS and EOS pseudo-segments
                are excluded from the results.
            as_names: If True, return inventory names instead of segments.

        Returns:
            A tuple of matching segments (default) or matching names when
            `as_names=True`.
        """
        segments = tuple(self.over(inv, filter_boundaries))
        if as_names:
            return tuple(inv.name_of(seg) for seg in segments)
        return segments

    @overload
    def __or__(self, other: NaturalClass) -> NaturalClassUnion: ...
    @overload
    def __or__(self, other: NaturalClassUnion) -> NaturalClassUnion: ...
    def __or__(
        self, other: NaturalClass | NaturalClassUnion
    ) -> NaturalClassUnion:
        """
        Return a new union combining this union with another class or union.
        """
        if isinstance(other, NaturalClassUnion):
            return NaturalClassUnion(self.classes + other.classes)
        return NaturalClassUnion(self.classes + (other,))

    def __str__(self) -> str:
        """Return a canonical bracketed representation of this union."""
        return (
            "["
            + "|".join(
                "{"
                + "".join(
                    f"{value}{feature}"
                    for feature, value in sorted(
                        nc.feature_specification.items()
                    )
                )
                + "}"
                for nc in self.classes
            )
            + "]"
        )
