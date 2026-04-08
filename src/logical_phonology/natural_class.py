from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, Iterator

from .feature_value import FeatureValue
from .segment import Segment

if TYPE_CHECKING:
    from .inventory import Inventory


@dataclass(frozen=True)
class NaturalClass:
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
        return inv.iter_extension(self, filter_boundaries)

    def __contains__(self, s: Segment) -> bool:
        return self.feature_specification.items() <= s.features.items()

    def __hash__(self) -> int:
        return hash(frozenset(self.feature_specification.items()))
