from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING, Iterator, overload

from logical_phonology.natural_class_union import NaturalClassUnion

from .errors import (
    AliasError,
    AmbiguousTokenizationError,
    DuplicateNameError,
    UnknownNameError,
    UnknownSegmentError,
    UntokenizableInputError,
)

if TYPE_CHECKING:
    from .feature_system import FeatureSystem
from .natural_class import NaturalClass
from .natural_class_sequence import NaturalClassSequence
from .segment import Segment
from .word import Word


@dataclass(frozen=True)
class Inventory:
    """A named segment inventory supporting tokenization and rendering.

    An inventory maps symbol names to segments, enabling conversion between
    string representations and feature bundles. Multiple names may map to
    the same segment (aliases), in which case `name_of` returns the
    canonical form derived from the segment's feature bundle.

    BOS (⋉) and EOS (⋊) boundary pseudo-segments are automatically
    registered in every inventory.

    Use `FeatureSystem.inventory()` to construct.

    Attributes:
        feature_system: The FeatureSystem this inventory belongs to.
        name_to_segment: An immutable mapping of symbol names to Segments,
            including canonical forms for aliased segments and boundary
            pseudo-segments.
        segment_to_name: An immutable mapping of Segments to their canonical
            names.
        names_in_order: All symbol names in declaration order, used for
            tokenization.
        user_names: The frozenset of names explicitly provided by the user,
            excluding auto-generated canonical and reserved names.
        allow_aliases: Whether multiple names may map to the same segment.
    """

    feature_system: FeatureSystem
    name_to_segment: Mapping[str, Segment]
    allow_aliases: bool = True
    names_in_order: tuple[str, ...] = field(init=False)
    segment_to_name: Mapping[Segment, str] = field(init=False)
    user_names: frozenset[str] = field(init=False)

    def __post_init__(self) -> None:
        # grab a mutable copy of the user-provided name_to_segment mapping
        extended: dict[str, Segment] = dict(self.name_to_segment)

        # get user-provided names before any auto-generated names are added
        # this is used by extend() to distinguish user names from canonical
        # or reserved names
        object.__setattr__(self, "user_names", frozenset(extended.keys()))

        # build a mapping from segments to all names that refer to them
        # this is for detecting aliases
        d: dict[Segment, list[str]] = defaultdict(list)
        for name, segment in extended.items():
            d[segment].append(name)

        # build segment_to_name. This is the canonical name reverse lookup
        # unambiguous segments keep their user-provided name
        # aliased segments get their canonical form (e.g. "{+F1-F2}") as a name
        segment_to_name: dict[Segment, str] = {}
        for segment, names in d.items():
            if len(names) == 1:
                segment_to_name[segment] = names[0]
            else:
                segment_to_name[segment] = str(segment)

        # if aliases are disabled, raise if any segment has multiple names
        if not self.allow_aliases:
            aliased = {
                str(segment): names
                for segment, names in d.items()
                if len(names) > 1
            }
            if aliased:
                raise AliasError(aliased)

        # check that reserved boundary names were not used by the user
        # this must happen before we inject boundary segments
        user_names = set(extended.keys())
        reserved_names = {"⋉", "⋊"}
        conflicts = reserved_names & user_names
        if conflicts:
            raise DuplicateNameError(conflicts)

        # register canonical forms for aliased segments in extended. If the
        # canonical form is already in extended (e.g. from full_inventory),
        # skip it. This means the user already provided that name and it
        # points to the correct segment
        for segment, name in segment_to_name.items():
            if name == str(segment) and name not in extended:
                extended[name] = segment

        # inject BOS and EOS boundary pseudo-segments: these are always
        # available in every inventory
        extended["⋉"] = self.feature_system.BOS
        extended["⋊"] = self.feature_system.EOS
        segment_to_name[self.feature_system.BOS] = "⋉"
        segment_to_name[self.feature_system.EOS] = "⋊"

        # freeze everything. From this point on the inventory is immutable
        object.__setattr__(self, "name_to_segment", MappingProxyType(extended))
        object.__setattr__(self, "names_in_order", tuple(extended.keys()))
        object.__setattr__(
            self, "segment_to_name", MappingProxyType(segment_to_name)
        )

    def render(self, word: Word) -> str:
        """Render a word as a string using inventory names.

        Segments with unique names render as their name. Aliased segments
        render as their canonical form (e.g. `{-Syllabic}`). Boundary
        pseudo-segments render as `⋉` and `⋊`.

        Args:
            word: The word to render.

        Returns:
            A string representation of the word.

        Raises:
            UnknownSegmentError: If any segment in the word is not in
                this inventory.
        """
        return "".join(self.name_of(seg) for seg in word)

    def tokenize(
        self, input_str: str, allow_ambiguity: bool = False
    ) -> Word | list[Word]:
        """Tokenize a string into a Word using this inventory.

        If the string contains whitespace, it is split on whitespace and each
        token is looked up directly. Otherwise, recursive tokenization is used
        to find all valid segmentations.

        Args:
            input_str: The string to tokenize.
            allow_ambiguity: If True, returns all possible tokenizations as a
                list of Words when the input is ambiguous. If False (default),
                raises AmbiguousTokenizationError on ambiguous input.

        Returns:
            A Word if the tokenization is unambiguous, or a list of Words if
            `allow_ambiguity=True` and the input is ambiguous.

        Raises:
            UntokenizableInputError: If no valid tokenization exists.
            AmbiguousTokenizationError: If multiple tokenizations exist and
                `allow_ambiguity=False`.
        """
        if any(c.isspace() for c in input_str):
            tokens = input_str.split()
            if not all(tok in self for tok in tokens):
                raise UntokenizableInputError(input_str)
            return Word(tuple([self[tok] for tok in tokens]))

        all_tokenizations: list[Word] = []

        def recurse(input_str: str, current_parse: list[Segment]) -> None:
            if input_str == "":
                all_tokenizations.append(Word(tuple(current_parse)))
                return
            for name in self.names_in_order:
                if input_str.startswith(name):
                    next_parse = [seg for seg in current_parse] + [self[name]]
                    recurse(input_str[len(name) :], next_parse)

        recurse(input_str, [])

        if len(all_tokenizations) > 1:
            if not allow_ambiguity:
                raise AmbiguousTokenizationError(input_str, all_tokenizations)
            return all_tokenizations
        if len(all_tokenizations) == 0:
            raise UntokenizableInputError(input_str)
        return all_tokenizations[0]

    @overload
    def iter_extension(
        self, obj: NaturalClass, filter_boundaries: bool = True
    ) -> Iterator[Segment]: ...

    @overload
    def iter_extension(
        self, obj: NaturalClassSequence, filter_boundaries: bool = True
    ) -> Iterator[Word]: ...

    def iter_extension(
        self,
        obj: NaturalClass | NaturalClassSequence,
        filter_boundaries: bool = True,
    ) -> Iterator[Segment] | Iterator[Word]:
        """Iterate over all members of a natural class or natural class
        sequence.

        Args:
            obj: A NaturalClass or NaturalClassSequence to evaluate.
            filter_boundaries: If True (default), BOS and EOS pseudo-segments
                are excluded from results.

        Returns:
            An iterator over Segments if `obj` is a NaturalClass, or an
            iterator over Words if `obj` is a NaturalClassSequence.
        """
        if isinstance(obj, NaturalClass):
            return self._iter_nc(obj, filter_boundaries)
        return self._iter_ncs(obj, filter_boundaries)

    ### These private methods are needed to satisfy mypy because generators ###
    def _iter_nc(
        self, nc: NaturalClass, filter_boundaries: bool = True
    ) -> Iterator[Segment]:
        for seg in self.segment_to_name:
            if seg in nc:
                if not filter_boundaries or seg not in (
                    self.feature_system.BOS,
                    self.feature_system.EOS,
                ):
                    yield seg

    def _iter_ncs(
        self, ncs: NaturalClassSequence, filter_boundaries: bool = True
    ) -> Iterator[Word]:
        from itertools import product

        extensions: list[list[Segment]] = []
        for nc in ncs.sequence:
            if isinstance(nc, NaturalClassUnion):
                segs = [
                    seg
                    for seg in self.segment_to_name
                    if seg in nc
                    and (
                        not filter_boundaries
                        or seg
                        not in (
                            self.feature_system.BOS,
                            self.feature_system.EOS,
                        )
                    )
                ]
            else:
                segs = [
                    seg
                    for seg in self._iter_nc(nc, filter_boundaries)
                    if not filter_boundaries
                    or seg
                    not in (self.feature_system.BOS, self.feature_system.EOS)
                ]
            extensions.append(segs)
        for combo in product(*extensions):
            yield Word(tuple(combo))

    def extend(self, new_segments: dict[str, Segment]) -> Inventory:
        """Return a new Inventory with additional named segments.

        The original inventory is unchanged. Only user-provided names are
        carried over — canonical forms and reserved names are recomputed.

        Args:
            new_segments: A mapping of new symbol names to Segments.

        Returns:
            A new Inventory containing the original segments plus the new ones.

        Raises:
            DuplicateNameError: If any new name already exists in the inventory.
            AliasError: If any new segment is already in the inventory and `allow_aliases=False`.
        """  # noqa: E501
        conflicts = set(new_segments.keys()) & self.user_names
        if conflicts:
            raise DuplicateNameError(conflicts)
        if not self.allow_aliases:
            segment_conflicts = {
                name: seg for name, seg in new_segments.items() if seg in self
            }
            if segment_conflicts:
                aliased = {
                    str(seg): [self.name_of(seg), name]
                    for name, seg in segment_conflicts.items()
                }
                raise AliasError(aliased)
        merged = {
            k: v
            for k, v in self.name_to_segment.items()
            if k in self.user_names
        } | new_segments
        return Inventory(self.feature_system, merged, self.allow_aliases)

    def __contains__(self, item: object) -> bool:
        """Return True if the name or segment is in this inventory.

        Accepts either a string (name lookup) or a Segment (reverse lookup).

        Args:
            item: A string name or Segment to look up.

        Returns:
            True if the item is in this inventory, False otherwise.
        """
        if isinstance(item, str):
            return item in self.name_to_segment
        if isinstance(item, Segment):
            return item in self.segment_to_name
        return False

    def __len__(self) -> int:
        """Return the number of distinct segments in this inventory.

        Counts unique segments, not names — aliases are not double-counted.
        Use ``len(self.name_to_segment)`` if you want the total number of
        names including aliases and canonical forms.
        """
        return len(self.segment_to_name)

    def segment(self, name: str) -> Segment:
        """Look up a segment by name.

        Also available via the `[]` operator.

        Args:
            name: The symbol name to look up.

        Returns:
            The Segment corresponding to the given name.

        Raises:
            UnknownNameError: If the name is not in this inventory.
        """
        if name not in self:
            raise UnknownNameError(name)
        return self.name_to_segment[name]

    def __getitem__(self, name: str) -> Segment:
        """Look up a segment by name.

        Also available via the ``segment()`` method.

        Args:
            name: The symbol name to look up.

        Returns:
            The Segment corresponding to the given name.

        Raises:
            UnknownNameError: If the name is not in this inventory.
        """

        return self.segment(name)

    def name_of(self, seg: Segment) -> str:
        """Return the canonical name of a segment in this inventory.

        For unambiguous segments, returns the user-provided name. For aliased
        segments, returns the canonical form derived from the segment's feature
        bundle (e.g. `{-Syllabic}`).

        Args:
            seg: The segment to look up.

        Returns:
            The canonical name of the segment.

        Raises:
            UnknownSegmentError: If the segment is not in this inventory.
        """
        if seg not in self:
            raise UnknownSegmentError(seg)
        return self.segment_to_name[seg]
