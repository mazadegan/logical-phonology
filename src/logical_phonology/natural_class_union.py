from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logical_phonology.natural_class import NaturalClass
    from logical_phonology.segment import Segment


@dataclass(frozen=True)
class NaturalClassUnion:
    classes: tuple[NaturalClass, ...]

    def __contains__(self, seg: Segment) -> bool:
        """Return True if the segment belongs to any class in this union."""
        return any(seg in nc for nc in self.classes)

    def __or__(
        self, other: NaturalClass | NaturalClassUnion
    ) -> NaturalClassUnion:
        """
        Return a new union combining this union with another class or union.
        """
        if isinstance(other, NaturalClassUnion):
            return NaturalClassUnion(self.classes + other.classes)
        return NaturalClassUnion(self.classes + (other,))
