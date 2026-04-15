from collections.abc import Collection
from functools import reduce
from typing import Callable, overload

from logical_phonology.feature_system import FeatureSystem
from logical_phonology.natural_class import NaturalClass
from logical_phonology.natural_class_union import NaturalClassUnion
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
    def union(self, a: NaturalClass, b: NaturalClass) -> NaturalClassUnion: ...
    @overload
    def union(
        self, a: NaturalClass, b: NaturalClassUnion
    ) -> NaturalClassUnion: ...
    @overload
    def union(
        self, a: NaturalClassUnion, b: NaturalClass
    ) -> NaturalClassUnion: ...
    @overload
    def union(
        self, a: NaturalClassUnion, b: NaturalClassUnion
    ) -> NaturalClassUnion: ...
    def union(self, a: object, b: object) -> NaturalClassUnion:
        """Union two natural classes or natural class unions.

        This is an analysis-level helper for combining natural-class
        descriptions without introducing a segment-level union operation.

        Args:
            a: A `NaturalClass` or `NaturalClassUnion`.
            b: A `NaturalClass` or `NaturalClassUnion`.

        Returns:
            A `NaturalClassUnion` containing the classes from both inputs.

        Raises:
            TypeError: If either argument is not a natural class or natural
                class union.
        """
        if isinstance(a, NaturalClass) and isinstance(b, NaturalClass):
            return NaturalClassUnion((a, b))
        if isinstance(a, NaturalClass) and isinstance(b, NaturalClassUnion):
            return NaturalClassUnion((a,) + b.classes)
        if isinstance(a, NaturalClassUnion) and isinstance(b, NaturalClass):
            return NaturalClassUnion(a.classes + (b,))
        if isinstance(a, NaturalClassUnion) and isinstance(
            b, NaturalClassUnion
        ):
            return NaturalClassUnion(a.classes + b.classes)
        raise TypeError(
            "Both arguments must be natural classes or natural class unions"
        )

    @overload
    def tier(self, w: Word, nc: NaturalClass) -> Word: ...
    @overload
    def tier(self, w: Word, nc: NaturalClassUnion) -> Word: ...
    def tier(self, w: Word, nc: NaturalClass | NaturalClassUnion) -> Word:
        """Return the subsequence of a word that belongs to a natural class.

        Args:
            w: The word to filter.
            nc: A `NaturalClass` or `NaturalClassUnion` to match against.

        Returns:
            A new word containing only the segments of `w` that belong to
            `nc`, in their original relative order.
        """
        return self.fs.word([s for s in w if s in nc])

    def ngrams(self, w: Word, n: int) -> list[tuple[int, int, Word]]:
        """Return all contiguous n-grams of a word.

        The word is treated as-is, so any BOS/EOS boundary segments already
        present in `w` are included in the n-gram windows.

        Args:
            w: The word to slice into contiguous subsequences.
            n: The length of each n-gram. Must be positive.

        Returns:
            A list of `(start, end, subsequence)` tuples, where `end` is
            exclusive.

        Raises:
            ValueError: If `n` is not positive.
        """
        if n <= 0:
            raise ValueError("n must be positive")
        return [
            (i, i + n, w[i : i + n]) for i in range(max(len(w) - n + 1, 0))
        ]

    @overload
    def intersect(self, a: Segment, b: Segment) -> Segment: ...
    @overload
    def intersect(self, a: Word, b: Word) -> Word: ...
    def intersect(self, a: object, b: object) -> Segment | Word:
        """Intersect two segments or two words.

        For segments, this returns the segment consisting of the valued
        features that are the same in both segments.

        For words, each aligned pair of segments is intersected and the
        resulting segments are reassembled into a new word.

        Args:
            a: A `Segment` or `Word`.
            b: A `Segment` or `Word` of the same type as `a`.

        Returns:
            The segment- or word-level intersection.

        Raises:
            TypeError: If `a` and `b` are not both segments or both words.
        """
        if isinstance(a, Segment) and isinstance(b, Segment):
            return Segment(
                {f: v for f, v in a.features.items() if f in b and b[f] == v}
            )
        if isinstance(a, Word) and isinstance(b, Word):
            return self.fs.word(
                [
                    Segment(
                        {
                            f: v
                            for f, v in s.features.items()
                            if f in t and t[f] == v
                        }
                    )
                    for s, t in zip(a, b)
                ]
            )
        raise TypeError("Both arguments must be of the same type")

    @overload
    def project(
        self, a: Segment, restricted_feature_set: Collection[str]
    ) -> Segment: ...
    @overload
    def project(
        self, a: Word, restricted_feature_set: Collection[str]
    ) -> Word: ...
    def project(
        self, a: object, restricted_feature_set: Collection[str]
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
