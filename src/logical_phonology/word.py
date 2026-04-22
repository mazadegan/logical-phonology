from dataclasses import dataclass
from typing import Collection, Iterator, cast, overload

from .natural_class import NaturalClass
from .natural_class_union import NaturalClassUnion
from .segment import Segment


@dataclass(frozen=True)
class Word:
    """An immutable ordered sequence of segments representing a phonological
    word.

    Words support indexing and slicing — integer indices return a `Segment`,
    while slices return a new `Word`. BOS and EOS boundary pseudo-segments
    can be added via `FeatureSystem.add_boundaries()`.

    Use `FeatureSystem.word()` or `Inventory.tokenize()` to construct.

    Attributes:
        segments: An ordered tuple of Segment objects.
    """

    segments: tuple[Segment, ...]

    def __len__(self) -> int:
        """
        Return the number of segments in the word, including any boundaries.
        """
        return len(self.segments)

    def __iter__(self) -> Iterator[Segment]:
        """
        Iterate over the segments in the word.
        """
        return iter(self.segments)

    @overload
    def __getitem__(self, index: int) -> Segment: ...

    @overload
    def __getitem__(self, index: slice) -> "Word": ...

    def __getitem__(self, index: int | slice) -> "Segment | Word":
        """Return a segment by index or a new word by slice.

        Args:
            index: An integer index or slice.

        Returns:
            A Segment if index is an integer, or a new Word if index is a slice.
        """  # noqa: E501
        result = self.segments[index]
        if isinstance(index, slice):
            return Word(cast(tuple[Segment, ...], result))
        return cast(Segment, result)

    def __add__(self, other: "Word | Segment") -> "Word":
        """Concatenate this word with another word or segment.

        Args:
            other: A Word or Segment to append.

        Returns:
            A new Word containing the segments of this word followed by
            the segments of other.

        Note:
            Boundaries are not checked — callers are responsible for
            ensuring BOS and EOS appear only at the edges of the final word.
        """
        if isinstance(other, Segment):
            return Word(self.segments + (other,))
        return Word(self.segments + other.segments)

    def _check_aligned(self, other: "Word") -> None:
        if len(self) != len(other):
            raise ValueError(
                f"Words must have the same length ({len(self)} != {len(other)})"  # noqa: E501
            )

    def unify(self, other: "Word") -> "Word":
        """Unify two words element-wise. Also available as the `|` operator."""
        self._check_aligned(other)
        return Word(
            tuple(s.unify(t) for s, t in zip(self.segments, other.segments))
        )

    def __or__(self, other: "Word") -> "Word":
        """Unify this word with another element-wise. See ``unify``."""
        return self.unify(other)

    def subtract(self, other: "Word") -> "Word":
        """
        Subtract two words element-wise. Also available as the `-` operator.
        """
        self._check_aligned(other)
        return Word(
            tuple(s.subtract(t) for s, t in zip(self.segments, other.segments))
        )

    def __sub__(self, other: "Word") -> "Word":
        """
        Subtract another word from this one element-wise. See ``subtract``.
        """
        return self.subtract(other)

    def intersect(self, other: "Word") -> "Word":
        """
        Intersect two words element-wise. Also available as the `&` operator.
        """
        self._check_aligned(other)
        return Word(
            tuple(
                s.intersect(t) for s, t in zip(self.segments, other.segments)
            )
        )

    def __and__(self, other: "Word") -> "Word":
        """Intersect this word with another element-wise. See ``intersect``."""
        return self.intersect(other)

    def project(self, restricted_feature_set: Collection[str]) -> "Word":
        """
        Return a new Word with each segment projected onto the feature set.
        """
        return Word(
            tuple(seg.project(restricted_feature_set) for seg in self.segments)
        )

    def __matmul__(self, restricted_feature_set: Collection[str]) -> "Word":
        """Project each segment onto a feature set. See ``project``."""
        return self.project(restricted_feature_set)

    def ngrams(self, n: int) -> list[tuple[int, int, "Word"]]:
        """Return all contiguous n-grams of this word.

        Args:
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
            (i, i + n, self[i : i + n])
            for i in range(max(len(self) - n + 1, 0))
        ]

    def tier(self, nc: NaturalClass | NaturalClassUnion) -> "Word":
        """Return the subsequence of segments belonging to a natural class.

        Args:
            nc: A `NaturalClass` or `NaturalClassUnion` to match against.

        Returns:
            A new Word containing only the segments of this word that belong
            to `nc`, in their original relative order.
        """
        return Word(tuple(s for s in self.segments if s in nc))

    def as_segment(self) -> Segment:
        """Return the sole segment; raises ValueError if len != 1."""
        if len(self.segments) != 1:
            raise ValueError(
                f"as_segment() requires a length-1 Word, got length {len(self.segments)}"  # noqa: E501
            )
        return self.segments[0]

    def __str__(self) -> str:
        """Return the canonical string representation of the word.

        Words are rendered as angle-bracketed, space-separated segment
        strings, e.g. ``<{+F} {-G}>``.
        """
        return "<" + " ".join(str(seg) for seg in self.segments) + ">"
