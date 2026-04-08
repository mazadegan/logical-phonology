from dataclasses import dataclass
from typing import Iterator, cast, overload

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
