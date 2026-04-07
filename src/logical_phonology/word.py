from dataclasses import dataclass
from enum import Enum

from .segment import Segment


class ReservedSymbol(Enum):
    BOS = "⋉"
    EOS = "⋊"


@dataclass(frozen=True)
class Word:
    segments: tuple[Segment | ReservedSymbol, ...]

    def __len__(self) -> int:
        # return length of word excluding BOS/EOS symbols
        return sum(1 for s in self.segments if isinstance(s, Segment))
