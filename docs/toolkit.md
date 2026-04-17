# Table of Contents

* [logical\_phonology.toolkit](#logical_phonology.toolkit)
  * [Toolkit](#logical_phonology.toolkit.Toolkit)
    * [fold](#logical_phonology.toolkit.Toolkit.fold)
    * [unify](#logical_phonology.toolkit.Toolkit.unify)
    * [subtract](#logical_phonology.toolkit.Toolkit.subtract)
    * [union](#logical_phonology.toolkit.Toolkit.union)
    * [tier](#logical_phonology.toolkit.Toolkit.tier)
    * [natural\_classes\_over](#logical_phonology.toolkit.Toolkit.natural_classes_over)
    * [ngrams](#logical_phonology.toolkit.Toolkit.ngrams)
    * [intersect](#logical_phonology.toolkit.Toolkit.intersect)
    * [project](#logical_phonology.toolkit.Toolkit.project)
    * [min\_intensions](#logical_phonology.toolkit.Toolkit.min_intensions)

<a id="logical_phonology.toolkit"></a>

# logical\_phonology.toolkit

<a id="logical_phonology.toolkit.Toolkit"></a>

## Toolkit Objects

```python
class Toolkit()
```

<a id="logical_phonology.toolkit.Toolkit.fold"></a>

#### fold

```python
def fold(op: Callable[[Segment, Segment], Segment], w: Word) -> Segment
```

Reduce a non-empty word with a binary segment operation.

**Arguments**:

- `op` - A binary operation that combines two segments into one.
- `w` - The word to reduce.
  

**Returns**:

  The result of applying `op` across all segments in `w`.
  

**Raises**:

- `ValueError` - If `w` is empty.

<a id="logical_phonology.toolkit.Toolkit.unify"></a>

#### unify

```python
def unify(a: object, b: object) -> Segment | Word
```

Unify two segments or two words.

For segments, this delegates to `Segment.unify()`.
For words, each aligned pair of segments is unified and the resulting
segments are reassembled into a new word.

**Arguments**:

- `a` - A `Segment` or `Word`.
- `b` - A `Segment` or `Word` of the same type as `a`.
  

**Returns**:

  A unified `Segment` or `Word`.
  

**Raises**:

- `TypeError` - If `a` and `b` are not both segments or both words.

<a id="logical_phonology.toolkit.Toolkit.subtract"></a>

#### subtract

```python
def subtract(a: object, b: object) -> Segment | Word
```

Subtract one segment or word from another.

For segments, this delegates to `Segment.subtract()`.
For words, each aligned pair of segments is subtracted and the
resulting segments are reassembled into a new word.

**Arguments**:

- `a` - A `Segment` or `Word`.
- `b` - A `Segment` or `Word` of the same type as `a`.
  

**Returns**:

  A resulting `Segment` or `Word`.
  

**Raises**:

- `TypeError` - If `a` and `b` are not both segments or both words.

<a id="logical_phonology.toolkit.Toolkit.union"></a>

#### union

```python
def union(a: object, b: object) -> NaturalClassUnion
```

Union two natural classes or natural class unions.

This is an analysis-level helper for combining natural-class
descriptions without introducing a segment-level union operation.

**Arguments**:

- `a` - A `NaturalClass` or `NaturalClassUnion`.
- `b` - A `NaturalClass` or `NaturalClassUnion`.
  

**Returns**:

  A `NaturalClassUnion` containing the classes from both inputs.
  

**Raises**:

- `TypeError` - If either argument is not a natural class or natural
  class union.

<a id="logical_phonology.toolkit.Toolkit.tier"></a>

#### tier

```python
def tier(w: Word, nc: NaturalClass | NaturalClassUnion) -> Word
```

Return the subsequence of a word that belongs to a natural class.

**Arguments**:

- `w` - The word to filter.
- `nc` - A `NaturalClass` or `NaturalClassUnion` to match against.
  

**Returns**:

  A new word containing only the segments of `w` that belong to
  `nc`, in their original relative order.

<a id="logical_phonology.toolkit.Toolkit.natural_classes_over"></a>

#### natural\_classes\_over

```python
def natural_classes_over(features: Collection[str],
                         include_empty: bool = True,
                         max_features: int = 8) -> Iterator[NaturalClass]
```

Yield all natural classes over a given feature set.

Features are deduplicated and sorted to ensure deterministic ordering.
Each feature can be absent, positive, or negative, producing `3^n`
classes over `n` unique features.

**Arguments**:

- `features` - The feature names to build classes over.
- `include_empty` - If True, include the empty class (no feature
  specifications).
- `max_features` - Maximum number of unique features to allow.
  

**Yields**:

  NaturalClass objects over the given feature set.
  

**Raises**:

- `UnknownFeatureError` - If any feature is not in this feature system.
- `ValueError` - If the number of unique features exceeds
  `max_features`.

<a id="logical_phonology.toolkit.Toolkit.ngrams"></a>

#### ngrams

```python
def ngrams(w: Word, n: int) -> list[tuple[int, int, Word]]
```

Return all contiguous n-grams of a word.

The word is treated as-is, so any BOS/EOS boundary segments already
present in `w` are included in the n-gram windows.

**Arguments**:

- `w` - The word to slice into contiguous subsequences.
- `n` - The length of each n-gram. Must be positive.
  

**Returns**:

  A list of `(start, end, subsequence)` tuples, where `end` is
  exclusive.
  

**Raises**:

- `ValueError` - If `n` is not positive.

<a id="logical_phonology.toolkit.Toolkit.intersect"></a>

#### intersect

```python
def intersect(a: object, b: object) -> Segment | Word
```

Intersect two segments or two words.

For segments, this returns the segment consisting of the valued
features that are the same in both segments.

For words, each aligned pair of segments is intersected and the
resulting segments are reassembled into a new word.

**Arguments**:

- `a` - A `Segment` or `Word`.
- `b` - A `Segment` or `Word` of the same type as `a`.
  

**Returns**:

  The segment- or word-level intersection.
  

**Raises**:

- `TypeError` - If `a` and `b` are not both segments or both words.

<a id="logical_phonology.toolkit.Toolkit.project"></a>

#### project

```python
def project(a: object,
            restricted_feature_set: Collection[str]) -> Segment | Word
```

Project a segment or every segment in a word onto a feature set.

For a segment, this delegates to `Segment.project()`.
For a word, each segment is projected with the same feature set and
the results are reassembled into a new word.

**Arguments**:

- `a` - A `Segment` or `Word`.
- `restricted_feature_set` - The feature names to keep.
  

**Returns**:

  A projected `Segment` or `Word`.
  

**Raises**:

- `TypeError` - If `a` is neither a segment nor a word.

<a id="logical_phonology.toolkit.Toolkit.min_intensions"></a>

#### min\_intensions

```python
def min_intensions(segments: Collection[Segment],
                   inv: Inventory,
                   features: Collection[str] | None = None,
                   *,
                   filter_boundaries: bool = True,
                   max_features: int = 8) -> list[NaturalClass]
```

Return all minimal natural classes with an exact target extension.

The search space is derived from the features common to all target
segments (same feature and same value). If `features` is provided, it
further restricts this common-feature set.

Candidate classes are then filtered to those whose extension over `inv`
is exactly `segments` (all and only), and only minimum-cardinality
matches are returned.

**Arguments**:

- `segments` - Target extension as a collection of segments.
- `inv` - The inventory that defines the universe for extensions.
- `features` - Optional subset filter over common features.
- `filter_boundaries` - If True (default), BOS/EOS are excluded when
  computing extensions.
- `max_features` - Maximum number of unique features allowed for
  enumeration.
  

**Returns**:

  A list of minimal natural classes. The list is sorted by string
  form for deterministic order and is empty if no class matches.
  

**Raises**:

- `ValueError` - If `segments` is empty.
- `UnknownSegmentError` - If any target segment is not in `inv`.
- `UnknownFeatureError` - If any searched feature is unknown.
- `ValueError` - If the searched feature count exceeds `max_features`.

