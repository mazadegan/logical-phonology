from functools import reduce
from typing import Callable, overload

from logical_phonology.feature_system import FeatureSystem
from logical_phonology.segment import Segment
from logical_phonology.word import Word


class Toolkit:
    def __init__(self, fs: FeatureSystem) -> None:
        self.fs = fs

    def fold(
        self, op: Callable[[Segment, Segment], Segment], w: Word
    ) -> Segment:
        if len(w) == 0:
            raise ValueError("Cannot fold over an empty word.")
        return reduce(op, w)

    @overload
    def unify(self, a: Segment, b: Segment) -> Segment: ...
    @overload
    def unify(self, a: Word, b: Word) -> Word: ...
    def unify(self, a: Segment | Word, b: Segment | Word) -> Segment | Word:
        if isinstance(a, Segment) and isinstance(b, Segment):
            return a.unify(b)
        if isinstance(a, Word) and isinstance(b, Word):
            return self.fs.word([s.unify(t) for s, t in zip(a, b)])
        else:
            raise TypeError("Both arguments must be of the same type")
