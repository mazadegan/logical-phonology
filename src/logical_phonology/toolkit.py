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

    @overload
    def subtract(self, a: Segment, b: Segment) -> Segment: ...
    @overload
    def subtract(self, a: Word, b: Word) -> Word: ...
    def subtract(self, a: Segment | Word, b: Segment | Word) -> Segment | Word:
        if isinstance(a, Segment) and isinstance(b, Segment):
            return a.subtract(b)
        if isinstance(a, Word) and isinstance(b, Word):
            return self.fs.word([s.subtract(t) for s, t in zip(a, b)])
        else:
            raise TypeError("Both arguments must be of the same type")

    @overload
    def project(
        self, a: Segment, restricted_feature_set: frozenset[str]
    ) -> Segment: ...
    @overload
    def project(
        self, a: Word, restricted_feature_set: frozenset[str]
    ) -> Word: ...
    def project(
        self, a: Segment | Word, restricted_feature_set: frozenset[str]
    ) -> Segment | Word:
        if isinstance(a, Segment):
            return a.project(restricted_feature_set)
        if isinstance(a, Word):
            return self.fs.word(
                [s.project(restricted_feature_set) for s in a]
            )
        raise TypeError("Argument must be a Segment or Word")
