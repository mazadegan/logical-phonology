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
        """Reduce a non-empty word with a binary segment operation.

        Args:
            op: A binary operation that combines two segments into one.
            w: The word to reduce.

        Returns:
            The result of applying `op` across all segments in `w`.

        Raises:
            ValueError: If `w` is empty.
        """
        if len(w) == 0:
            raise ValueError("Cannot fold over an empty word.")
        return reduce(op, w)

    @overload
    def unify(self, a: Segment, b: Segment) -> Segment: ...
    @overload
    def unify(self, a: Word, b: Word) -> Word: ...
    def unify(self, a: object, b: object) -> Segment | Word:
        """Unify two segments or two words.

        For segments, this delegates to `Segment.unify()`.
        For words, each aligned pair of segments is unified and the resulting
        segments are reassembled into a new word.

        Args:
            a: A `Segment` or `Word`.
            b: A `Segment` or `Word` of the same type as `a`.

        Returns:
            A unified `Segment` or `Word`.

        Raises:
            TypeError: If `a` and `b` are not both segments or both words.
        """
        if isinstance(a, Segment) and isinstance(b, Segment):
            return a.unify(b)
        if isinstance(a, Word) and isinstance(b, Word):
            return self.fs.word([s.unify(t) for s, t in zip(a, b)])
        raise TypeError("Both arguments must be of the same type")

    @overload
    def subtract(self, a: Segment, b: Segment) -> Segment: ...
    @overload
    def subtract(self, a: Word, b: Word) -> Word: ...
    def subtract(self, a: object, b: object) -> Segment | Word:
        """Subtract one segment or word from another.

        For segments, this delegates to `Segment.subtract()`.
        For words, each aligned pair of segments is subtracted and the
        resulting segments are reassembled into a new word.

        Args:
            a: A `Segment` or `Word`.
            b: A `Segment` or `Word` of the same type as `a`.

        Returns:
            A resulting `Segment` or `Word`.

        Raises:
            TypeError: If `a` and `b` are not both segments or both words.
        """
        if isinstance(a, Segment) and isinstance(b, Segment):
            return a.subtract(b)
        if isinstance(a, Word) and isinstance(b, Word):
            return self.fs.word([s.subtract(t) for s, t in zip(a, b)])
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
        self, a: object, restricted_feature_set: frozenset[str]
    ) -> Segment | Word:
        """Project a segment or every segment in a word onto a feature set.

        For a segment, this delegates to `Segment.project()`.
        For a word, each segment is projected with the same feature set and
        the results are reassembled into a new word.

        Args:
            a: A `Segment` or `Word`.
            restricted_feature_set: The feature names to keep.

        Returns:
            A projected `Segment` or `Word`.

        Raises:
            TypeError: If `a` is neither a segment nor a word.
        """
        if isinstance(a, Segment):
            return a.project(restricted_feature_set)
        if isinstance(a, Word):
            return self.fs.word([s.project(restricted_feature_set) for s in a])
        raise TypeError("Argument must be a Segment or Word")
