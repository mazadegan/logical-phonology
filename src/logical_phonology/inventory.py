from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING, Iterator, overload

from .errors import (
    AliasError,
    AmbiguousTokenizationError,
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
    feature_system: FeatureSystem
    name_to_segment: Mapping[str, Segment]
    allow_aliases: bool = True
    names_in_order: tuple[str, ...] = field(init=False)
    segment_to_name: Mapping[Segment, str] = field(init=False)

    def __post_init__(self) -> None:
        # mutable copy
        extended: dict[str, Segment] = dict(self.name_to_segment)

        # build segment_to_name
        d: dict[Segment, list[str]] = defaultdict(list)
        for name, segment in extended.items():
            d[segment].append(name)
        segment_to_name: dict[Segment, str] = {}
        for segment, names in d.items():
            if len(names) == 1:
                segment_to_name[segment] = names[0]
            else:
                segment_to_name[segment] = str(segment)
        # check if aliases are allowed
        if not self.allow_aliases:
            aliased = {
                str(segment): names
                for segment, names in d.items()
                if len(names) > 1
            }
            if aliased:
                raise AliasError(aliased)
        # set up canonical forms for aliased segments
        for segment, name in segment_to_name.items():
            if name == str(segment):
                extended[name] = segment

        # add reserved segments
        extended["⋉"] = self.feature_system.BOS
        extended["⋊"] = self.feature_system.EOS
        segment_to_name[self.feature_system.BOS] = "⋉"
        segment_to_name[self.feature_system.EOS] = "⋊"

        # freeze everything
        object.__setattr__(self, "name_to_segment", MappingProxyType(extended))
        object.__setattr__(self, "names_in_order", tuple(extended.keys()))
        object.__setattr__(
            self, "segment_to_name", MappingProxyType(segment_to_name)
        )

    @property
    def BOS(self) -> Segment:
        return self.feature_system.BOS

    @property
    def EOS(self) -> Segment:
        return self.feature_system.EOS

    def render(self, word: Word) -> str:
        return "".join(self.name_of(seg) for seg in word)

    def tokenize(
        self, input_str: str, allow_ambiguity: bool = False
    ) -> Word | list[Word]:
        if " " in input_str:
            split = input_str.split(" ")
            if not all(tok in self for tok in split):
                raise UntokenizableInputError(input_str)
            return Word(tuple([self[tok] for tok in split]))

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
        if isinstance(obj, NaturalClass):
            return self._iter_nc(obj, filter_boundaries)
        return self._iter_ncs(obj, filter_boundaries)

    # -- These private methods are needed to satisfy mypy because generators --
    def _iter_nc(
        self, nc: NaturalClass, filter_boundaries: bool = True
    ) -> Iterator[Segment]:
        for seg in self.segment_to_name:
            if seg in nc:
                if not filter_boundaries or seg not in (self.BOS, self.EOS):
                    yield seg

    def _iter_ncs(
        self, ncs: NaturalClassSequence, filter_boundaries: bool = True
    ) -> Iterator[Word]:
        from itertools import product

        extensions = [
            [
                seg
                for seg in self._iter_nc(nc, filter_boundaries)
                if not filter_boundaries or seg not in (self.BOS, self.EOS)
            ]
            for nc in ncs.sequence
        ]
        for combo in product(*extensions):
            yield Word(tuple(combo))

    def __contains__(self, item: object) -> bool:
        if isinstance(item, str):
            return item in self.name_to_segment
        if isinstance(item, Segment):
            return item in self.segment_to_name
        return False

    def segment(self, name: str) -> Segment:
        if name not in self:
            raise UnknownNameError(name)
        return self.name_to_segment[name]

    def __getitem__(self, name: str) -> Segment:
        return self.segment(name)

    def name_of(self, seg: Segment) -> str:
        if seg not in self:
            raise UnknownSegmentError(seg)
        return self.segment_to_name[seg]
