from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterator, cast, overload

from .natural_class import NaturalClass
from .word import Word

if TYPE_CHECKING:
    from .inventory import Inventory


@dataclass(frozen=True)
class NaturalClassSequence:
    """An immutable ordered sequence of natural classes defining a set of words.

    A word belongs to a natural class sequence if each of its segments
    belongs to the corresponding natural class in the sequence, pointwise.
    The sequence also supports substring matching via `matches_at` and
    `find_all`.

    Use `FeatureSystem.natural_class_sequence()` to construct.

    Attributes:
        sequence: An ordered tuple of NaturalClass objects.
    """  # noqa: E501

    sequence: tuple[NaturalClass, ...]

    def matches_at(self, word: Word, position: int) -> bool:
        """Return True if the sequence matches the word starting at position.

        Args:
            word: The word to match against.
            position: The index in the word to start matching from.

        Returns:
            True if the subsequence of the word starting at `position` matches
            this natural class sequence, False otherwise.
        """
        return word[position : position + len(self)] in self

    def find_all(self, word: Word) -> list[int]:
        """Return all positions in the word where the sequence matches.

        Args:
            word: The word to search.

        Returns:
            A list of positions where this natural class sequence matches
            as a substring of the word.
        """
        return [
            i
            for i in range(len(word) - len(self) + 1)
            if self.matches_at(word, i)
        ]

    def over(
        self, inv: Inventory, filter_boundaries: bool = True
    ) -> Iterator[Word]:
        """Iterate over all words matching this sequence over a given inventory.

        Args:
            inv: The inventory to evaluate the sequence over.
            filter_boundaries: If True (default), BOS and EOS pseudo-segments
                are excluded from the results.

        Returns:
            An iterator over all words in the inventory that match this
            natural class sequence.
        """  # noqa: E501
        return inv.iter_extension(self, filter_boundaries)

    def __len__(self) -> int:
        return len(self.sequence)

    def __contains__(self, item: Word) -> bool:
        """Return True if the word matches this natural class sequence exactly.

        The word must have the same length as the sequence, and each segment
        must belong to the corresponding natural class, pointwise. Also
        available via the `in` operator.

        Args:
            item: The word to test for membership.

        Returns:
            True if the word matches this sequence, False otherwise.
        """
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
