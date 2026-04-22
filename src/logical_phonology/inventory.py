from __future__ import annotations

from collections import defaultdict
from collections.abc import Collection, Mapping
from dataclasses import dataclass, field
from itertools import combinations, product
from types import MappingProxyType
from typing import TYPE_CHECKING, Iterator, overload

from logical_phonology.natural_class_union import NaturalClassUnion

from .errors import (
    AliasError,
    AmbiguousTokenizationError,
    DuplicateNameError,
    UnknownFeatureError,
    UnknownNameError,
    UnknownSegmentError,
    UntokenizableInputError,
)
from .feature_value import FeatureValue

if TYPE_CHECKING:
    from .feature_system import FeatureSystem
from .natural_class import NaturalClass
from .natural_class_sequence import NaturalClassSequence
from .segment import Segment
from .word import Word


@dataclass(frozen=True)
class ExtensionEntry:
    """The intensions and minimal intensions for a single extension.

    Attributes:
        intensions: All natural classes that produce this extension.
        minimal_intensions: The subset of intensions with fewest features.
    """

    intensions: list[NaturalClass]
    minimal_intensions: list[NaturalClass]


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
        token is looked up directly. Otherwise, dynamic programming over string
        positions is used to find all valid segmentations.

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

        n = len(input_str)
        # memo[i] stores all parses of input_str[i:] as lists of segments
        memo: dict[int, list[list[Segment]]] = {n: [[]]}
        name_to_segment = self.name_to_segment

        for i in range(n - 1, -1, -1):
            parses_from_i: list[list[Segment]] = []
            for name in self.names_in_order:
                if not input_str.startswith(name, i):
                    continue
                end = i + len(name)
                for suffix_parse in memo.get(end, []):
                    parses_from_i.append(
                        [name_to_segment[name]] + suffix_parse
                    )
            memo[i] = parses_from_i

        all_tokenizations = [Word(tuple(parse)) for parse in memo.get(0, [])]

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
        self, obj: NaturalClassUnion, filter_boundaries: bool = True
    ) -> Iterator[Segment]: ...

    @overload
    def iter_extension(
        self, obj: NaturalClassSequence, filter_boundaries: bool = True
    ) -> Iterator[Word]: ...

    def iter_extension(
        self,
        obj: NaturalClass | NaturalClassUnion | NaturalClassSequence,
        filter_boundaries: bool = True,
    ) -> Iterator[Segment] | Iterator[Word]:
        """Iterate over all members of a natural class, union, or sequence.

        Args:
            obj: A NaturalClass, NaturalClassUnion, or NaturalClassSequence.
            filter_boundaries: If True (default), BOS and EOS pseudo-segments
                are excluded from results.

        Returns:
            An iterator over Segments if `obj` is a NaturalClass or
            NaturalClassUnion, or an iterator over Words if `obj` is a
            NaturalClassSequence.
        """
        if isinstance(obj, NaturalClassSequence):
            return self._iter_ncs(obj, filter_boundaries)
        if isinstance(obj, NaturalClassUnion):
            return self._iter_ncu(obj, filter_boundaries)
        return self._iter_nc(obj, filter_boundaries)

    ### These private methods are needed to satisfy mypy because generators ###
    def _iter_ncu(
        self, ncu: NaturalClassUnion, filter_boundaries: bool = True
    ) -> Iterator[Segment]:
        for seg in self.segment_to_name:
            if seg in ncu:
                if not filter_boundaries or seg not in (
                    self.feature_system.BOS,
                    self.feature_system.EOS,
                ):
                    yield seg

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

    def __getitem__(self, name: str) -> Segment:
        """Look up a segment by name.

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

    def min_intensions(
        self,
        segments: Collection[Segment],
        features: Collection[str] | None = None,
        *,
        filter_boundaries: bool = True,
        max_features: int = 8,
    ) -> list[NaturalClass]:
        """Return all minimal natural classes with an exact target extension.

        The search space is derived from features common to all target
        segments (same feature and same value). If `features` is provided, it
        further restricts this common-feature set. Candidate classes are
        evaluated with bit masks over the inventory and matched by exact
        extension equality.

        Args:
            segments: Target extension as a collection of segments.
            features: Optional subset filter over common features.
            filter_boundaries: If True (default), BOS/EOS are excluded when
                computing extensions.
            max_features: Maximum number of unique features allowed for
                enumeration.

        Returns:
            A list of minimal natural classes. The list is sorted by string
            form for deterministic order and is empty if no class matches.

        Raises:
            ValueError: If `segments` is empty.
            UnknownSegmentError: If any target segment is not in this inventory.
            UnknownFeatureError: If any searched feature is unknown.
            ValueError: If the searched feature count exceeds `max_features`.
        """  # noqa: E501
        segment_list = list(segments)
        if not segment_list:
            raise ValueError("segments must be non-empty")

        for segment in segment_list:
            if segment not in self:
                raise UnknownSegmentError(segment)

        common_items = set(segment_list[0].features.items())
        for segment in segment_list[1:]:
            common_items &= set(segment.features.items())
        common_features = {feature for feature, _ in common_items}

        if features is None:
            feature_set = tuple(sorted(common_features))
        else:
            feature_filter = set(features)
            unknown = feature_filter - self.feature_system.valid_features
            if unknown:
                raise UnknownFeatureError(unknown)
            feature_set = tuple(sorted(common_features & feature_filter))

        if len(feature_set) > max_features:
            raise ValueError(
                f"Feature set size {len(feature_set)} exceeds max_features="
                f"{max_features}. Pass a higher max_features to override."
            )

        universe = [
            seg
            for seg in self.segment_to_name
            if (not filter_boundaries)
            or seg not in (self.feature_system.BOS, self.feature_system.EOS)
        ]
        seg_to_idx = {seg: i for i, seg in enumerate(universe)}
        if any(seg not in seg_to_idx for seg in segment_list):
            return []

        target_mask = 0
        for seg in segment_list:
            target_mask |= 1 << seg_to_idx[seg]

        literal_masks: dict[tuple[str, FeatureValue], int] = {}
        for feature in feature_set:
            pos_mask = 0
            neg_mask = 0
            for i, seg in enumerate(universe):
                if feature in seg:
                    if seg[feature] == FeatureValue.POS:
                        pos_mask |= 1 << i
                    elif seg[feature] == FeatureValue.NEG:
                        neg_mask |= 1 << i
            literal_masks[(feature, FeatureValue.POS)] = pos_mask
            literal_masks[(feature, FeatureValue.NEG)] = neg_mask

        full_mask = (1 << len(universe)) - 1

        for size in range(0, len(feature_set) + 1):
            matches: list[NaturalClass] = []
            for subset in combinations(feature_set, size):
                for values in product(
                    (FeatureValue.POS, FeatureValue.NEG), repeat=size
                ):
                    mask = full_mask
                    specification: dict[str, FeatureValue] = {}
                    for feature, value in zip(subset, values):
                        mask &= literal_masks[(feature, value)]
                        if (mask & target_mask) != target_mask:
                            break
                        specification[feature] = value
                    else:
                        if mask == target_mask:
                            matches.append(
                                self.feature_system.natural_class(
                                    specification
                                )
                            )
            if matches:
                return sorted(matches, key=str)

        return []

    def extensions_to_intensions(
        self,
        features: Collection[str] | None = None,
        *,
        filter_boundaries: bool = True,
        max_features: int = 8,
    ) -> dict[frozenset[Segment], ExtensionEntry]:
        """
        Map each non-empty extension to its intensions and minimal intensions.

        Enumerates all natural classes over the given feature set, groups them
        by the set of inventory segments they pick out, and identifies the
        minimal intensions for each group. Uses bitmask evaluation for
        efficiency.

        Args:
            features: Feature names to enumerate over. Defaults to all features
                in this feature system.
            filter_boundaries: If True (default), BOS/EOS are excluded.
            max_features: Maximum number of features allowed. Defaults to 8.

        Returns:
            A dict mapping each non-empty extension (frozenset of Segments) to
            an ExtensionEntry with its intensions and minimal intensions.

        Raises:
            UnknownFeatureError: If any feature is not in this feature system.
            ValueError: If the feature count exceeds `max_features`.
        """
        feature_set = tuple(
            sorted(
                set(features)
                if features is not None
                else self.feature_system.valid_features
            )
        )
        unknown = set(feature_set) - self.feature_system.valid_features
        if unknown:
            raise UnknownFeatureError(unknown)
        if len(feature_set) > max_features:
            raise ValueError(
                f"Feature set size {len(feature_set)} exceeds max_features="
                f"{max_features}. Pass a higher max_features to override."
            )

        universe = [
            seg
            for seg in self.segment_to_name
            if (not filter_boundaries)
            or seg not in (self.feature_system.BOS, self.feature_system.EOS)
        ]
        idx_to_seg = dict(enumerate(universe))
        full_mask = (1 << len(universe)) - 1

        literal_masks: dict[tuple[str, FeatureValue], int] = {}
        for feature in feature_set:
            pos_mask = 0
            neg_mask = 0
            for i, seg in enumerate(universe):
                if feature in seg:
                    if seg[feature] == FeatureValue.POS:
                        pos_mask |= 1 << i
                    elif seg[feature] == FeatureValue.NEG:
                        neg_mask |= 1 << i
            literal_masks[(feature, FeatureValue.POS)] = pos_mask
            literal_masks[(feature, FeatureValue.NEG)] = neg_mask

        extension_map: dict[int, list[NaturalClass]] = {}
        for assignment in product(
            (None, FeatureValue.POS, FeatureValue.NEG), repeat=len(feature_set)
        ):
            spec = {
                f: v for f, v in zip(feature_set, assignment) if v is not None
            }
            mask = full_mask
            for f, v in spec.items():
                mask &= literal_masks[(f, v)]
            if mask == 0:
                continue
            nc = self.feature_system.natural_class(spec)
            extension_map.setdefault(mask, []).append(nc)

        result: dict[frozenset[Segment], ExtensionEntry] = {}
        for mask, intensions in extension_map.items():
            extension = frozenset(
                idx_to_seg[i] for i in range(len(universe)) if mask & (1 << i)
            )
            min_len = min(len(nc.feature_specification) for nc in intensions)
            minimal = sorted(
                (
                    nc
                    for nc in intensions
                    if len(nc.feature_specification) == min_len
                ),
                key=str,
            )
            result[extension] = ExtensionEntry(
                intensions=sorted(intensions, key=str),
                minimal_intensions=minimal,
            )
        return result
