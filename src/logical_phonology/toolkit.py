from collections.abc import Collection, Iterator, Sequence
from functools import reduce
from itertools import combinations, product
from typing import Callable, overload

from logical_phonology.errors import UnknownFeatureError, UnknownSegmentError
from logical_phonology.feature_system import FeatureSystem
from logical_phonology.feature_value import FeatureValue
from logical_phonology.inventory import Inventory
from logical_phonology.natural_class import NaturalClass
from logical_phonology.natural_class_union import NaturalClassUnion
from logical_phonology.segment import Segment
from logical_phonology.word import Word


class Toolkit:
    def __init__(self, fs: FeatureSystem) -> None:
        self.fs = fs

    def fold(
        self,
        op: Callable[[Segment, Segment], Segment],
        segments: Sequence[Segment],
    ) -> Segment:
        """Reduce a non-empty segment sequence with a binary operation.

        Args:
            op: A binary operation that combines two segments into one.
            segments: The ordered segment sequence to reduce.

        Returns:
            The result of applying `op` across all segments.

        Raises:
            ValueError: If `segments` is empty.
        """
        if len(segments) == 0:
            raise ValueError("Cannot fold over an empty segment sequence.")
        return reduce(op, segments)

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

    def natural_classes_over(
        self,
        features: Collection[str],
        include_empty: bool = True,
        max_features: int = 8,
    ) -> Iterator[NaturalClass]:
        """Yield all natural classes over a given feature set.

        Features are deduplicated and sorted to ensure deterministic ordering.
        Each feature can be absent, positive, or negative, producing `3^n`
        classes over `n` unique features.

        Args:
            features: The feature names to build classes over.
            include_empty: If True, include the empty class (no feature
                specifications).
            max_features: Maximum number of unique features to allow.

        Yields:
            NaturalClass objects over the given feature set.

        Raises:
            UnknownFeatureError: If any feature is not in this feature system.
            ValueError: If the number of unique features exceeds
                `max_features`.
        """
        feature_names = tuple(sorted(set(features)))
        unknown = set(feature_names) - self.fs.valid_features
        if unknown:
            raise UnknownFeatureError(unknown)
        if len(feature_names) > max_features:
            raise ValueError(
                f"Feature set size {len(feature_names)} exceeds max_features="
                f"{max_features}. Pass a higher max_features to override."
            )

        values = (None, FeatureValue.POS, FeatureValue.NEG)
        for assignment in product(values, repeat=len(feature_names)):
            if not include_empty and all(v is None for v in assignment):
                continue
            spec = {
                f: v
                for f, v in zip(feature_names, assignment)
                if v is not None
            }
            yield self.fs.natural_class(spec)

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

    def min_intensions(
        self,
        segments: Collection[Segment],
        inv: Inventory,
        features: Collection[str] | None = None,
        *,
        strict_feature_system: bool = True,
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
            inv: The inventory that defines the universe for extensions.
            features: Optional subset filter over common features.
            strict_feature_system: If True (default), require that this
                toolkit's feature system matches `inv.feature_system`.
            filter_boundaries: If True (default), BOS/EOS are excluded when
                computing extensions.
            max_features: Maximum number of unique features allowed for
                enumeration.

        Returns:
            A list of minimal natural classes. The list is sorted by string
            form for deterministic order and is empty if no class matches.

        Raises:
            ValueError: If `segments` is empty.
            ValueError: If `strict_feature_system=True` and feature systems
                do not match.
            UnknownSegmentError: If any target segment is not in `inv`.
            UnknownFeatureError: If any searched feature is unknown.
            ValueError: If the searched feature count exceeds `max_features`.
        """
        if strict_feature_system and inv.feature_system != self.fs:
            raise ValueError(
                "Toolkit feature system and inventory feature system must "
                "match. Pass strict_feature_system=False to override."
            )

        segment_list = list(segments)
        if not segment_list:
            raise ValueError("segments must be non-empty")

        for segment in segment_list:
            if segment not in inv:
                raise UnknownSegmentError(segment)

        common_items = set(segment_list[0].features.items())
        for segment in segment_list[1:]:
            common_items &= set(segment.features.items())
        common_features = {feature for feature, _ in common_items}

        if features is None:
            feature_set = tuple(sorted(common_features))
        else:
            feature_filter = set(features)
            unknown = feature_filter - self.fs.valid_features
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
            for seg in inv.segment_to_name
            if (not filter_boundaries)
            or seg not in (inv.feature_system.BOS, inv.feature_system.EOS)
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
                                self.fs.natural_class(specification)
                            )
            if matches:
                return sorted(matches, key=str)

        return []
