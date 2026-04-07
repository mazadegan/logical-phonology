from dataclasses import dataclass
from typing import cast, overload

from .natural_class import NaturalClass
from .word import Word


@dataclass(frozen=True)
class NaturalClassSequence:
    sequence: tuple[NaturalClass, ...]

    def __len__(self) -> int:
        return len(self.sequence)

    def __contains__(self, item: Word) -> bool:
        if len(self.sequence) != len(item):
            return False
        return all(seg in nc for seg, nc in zip(item, self.sequence))

    @overload
    def __getitem__(self, index: int) -> NaturalClass: ...

    @overload
    def __getitem__(self, index: slice) -> "NaturalClassSequence": ...

    def __getitem__(
        self, index: int | slice
    ) -> "NaturalClass | NaturalClassSequence":
        result = self.sequence[index]
        if isinstance(index, slice):
            return NaturalClassSequence(cast(tuple[NaturalClass, ...], result))
        return cast(NaturalClass, result)
