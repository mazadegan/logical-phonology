# Table of Contents

* [logical\_phonology.toolkit](#logical_phonology.toolkit)
  * [Toolkit](#logical_phonology.toolkit.Toolkit)
    * [fold](#logical_phonology.toolkit.Toolkit.fold)
    * [unify](#logical_phonology.toolkit.Toolkit.unify)
    * [subtract](#logical_phonology.toolkit.Toolkit.subtract)
    * [union](#logical_phonology.toolkit.Toolkit.union)
    * [tier](#logical_phonology.toolkit.Toolkit.tier)
    * [intersect](#logical_phonology.toolkit.Toolkit.intersect)
    * [project](#logical_phonology.toolkit.Toolkit.project)

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
            restricted_feature_set: frozenset[str]) -> Segment | Word
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

