from dataclasses import dataclass
from typing import Iterator, cast, overload

from .segment import Segment


@dataclass(frozen=True)
class Word:
    segments: tuple[Segment, ...]

    def __len__(self) -> int:
        return len(self.segments)

    def __iter__(self) -> Iterator[Segment]:
        return iter(self.segments)

    @overload
    def __getitem__(self, index: int) -> Segment: ...

    @overload
    def __getitem__(self, index: slice) -> "Word": ...

    def __getitem__(self, index: int | slice) -> "Segment | Word":
        result = self.segments[index]
        if isinstance(index, slice):
            return Word(cast(tuple[Segment, ...], result))
        return cast(Segment, result)
