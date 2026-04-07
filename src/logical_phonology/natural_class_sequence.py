from dataclasses import dataclass
from typing import cast, overload

from .natural_class import NaturalClass
from .word import Word


@dataclass(frozen=True)
class NaturalClassSequence:
    sequence: tuple[NaturalClass, ...]

    def matches_at(self, word: Word, position: int) -> bool:
        """Return True if the sequence matches the word starting at position."""  # noqa: E501
        return word[position : position + len(self)] in self

    def find_all(self, word: Word) -> list[int]:
        """Return all positions in the word where the sequence matches."""
        return [
            i
            for i in range(len(word) - len(self) + 1)
            if self.matches_at(word, i)
        ]

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
