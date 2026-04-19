from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterator, cast, overload

from logical_phonology.natural_class_union import NaturalClassUnion

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

    sequence: tuple[NaturalClass | NaturalClassUnion, ...]

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

    def find_first(self, word: Word, from_pos: int = 0) -> int | None:
        """Return the position of the first match at or after from_pos.

        Args:
            word: The word to search.
            from_pos: The position to start searching from (inclusive).

        Returns:
            The index of the first matching position, or None if no match found.
        """  # noqa: E501
        for i in range(max(from_pos, 0), len(word) - len(self) + 1):
            if self.matches_at(word, i):
                return i
        return None

    def find_last(
        self, word: Word, before_pos: int | None = None
    ) -> int | None:
        """Return the position of the last match before before_pos.

        Args:
            word: The word to search.
            before_pos: Search only positions before this index (exclusive).
                If None, searches the entire word.

        Returns:
            The index of the last matching position, or None if no match found.
        """  # noqa: E501
        end = len(word) - len(self) + 1
        if before_pos is not None:
            end = min(end, before_pos)
        for i in range(end - 1, -1, -1):
            if self.matches_at(word, i):
                return i
        return None

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

    def extension(
        self,
        inv: Inventory,
        filter_boundaries: bool = True,
        as_names: bool = False,
    ) -> tuple[Word, ...] | tuple[str, ...]:
        """
        Return the materialized extension of this sequence over an inventory.

        Args:
            inv: The inventory to evaluate the sequence over.
            filter_boundaries: If True (default), BOS and EOS pseudo-segments
                are excluded from the results.
            as_names: If True, return rendered word strings instead of `Word`
                objects.

        Returns:
            A tuple of matching words (default) or rendered word strings when
            `as_names=True`.
        """
        words = tuple(self.over(inv, filter_boundaries))
        if as_names:
            return tuple(inv.render(word) for word in words)
        return words

    def __len__(self) -> int:
        """Return the number of natural classes in this sequence."""
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
        """Return a natural class by index or a subsequence by slice.

        Args:
            index: An integer index or slice.

        Returns:
            A NaturalClass if index is an integer, or a new
            NaturalClassSequence if index is a slice.
        """
        result = self.sequence[index]
        if isinstance(index, slice):
            return NaturalClassSequence(cast(tuple[NaturalClass, ...], result))
        return cast(NaturalClass, result)

    def __str__(self) -> str:
        """Return a canonical bracketed representation of this sequence.

        Elements are rendered as natural-class specs, with unions using `|`,
        joined by spaces inside one outer pair of brackets.
        """
        parts: list[str] = []
        for item in self.sequence:
            if isinstance(item, NaturalClassUnion):
                part = "|".join(
                    "{"
                    + ",".join(
                        f"{value}{feature}"
                        for feature, value in sorted(
                            nc.feature_specification.items()
                        )
                    )
                    + "}"
                    for nc in item.classes
                )
                parts.append(part)
            else:
                parts.append(
                    "{"
                    + ",".join(
                        f"{value}{feature}"
                        for feature, value in sorted(
                            item.feature_specification.items()
                        )
                    )
                    + "}"
                )
        return "[" + " ".join(parts) + "]"
