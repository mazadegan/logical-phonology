# Table of Contents

* [logical\_phonology.word](#logical_phonology.word)
  * [Word](#logical_phonology.word.Word)
    * [\_\_len\_\_](#logical_phonology.word.Word.__len__)
    * [\_\_iter\_\_](#logical_phonology.word.Word.__iter__)
    * [\_\_getitem\_\_](#logical_phonology.word.Word.__getitem__)
    * [\_\_add\_\_](#logical_phonology.word.Word.__add__)
    * [unify](#logical_phonology.word.Word.unify)
    * [\_\_or\_\_](#logical_phonology.word.Word.__or__)
    * [subtract](#logical_phonology.word.Word.subtract)
    * [\_\_sub\_\_](#logical_phonology.word.Word.__sub__)
    * [intersect](#logical_phonology.word.Word.intersect)
    * [\_\_and\_\_](#logical_phonology.word.Word.__and__)
    * [project](#logical_phonology.word.Word.project)
    * [\_\_matmul\_\_](#logical_phonology.word.Word.__matmul__)
    * [ngrams](#logical_phonology.word.Word.ngrams)
    * [tier](#logical_phonology.word.Word.tier)
    * [find\_all](#logical_phonology.word.Word.find_all)
    * [find\_after](#logical_phonology.word.Word.find_after)
    * [find\_before](#logical_phonology.word.Word.find_before)
    * [minimal\_pair\_with](#logical_phonology.word.Word.minimal_pair_with)
    * [as\_segment](#logical_phonology.word.Word.as_segment)
    * [\_\_str\_\_](#logical_phonology.word.Word.__str__)

<a id="logical_phonology.word"></a>

# logical\_phonology.word

<a id="logical_phonology.word.Word"></a>

## Word Objects

```python
@dataclass(frozen=True)
class Word()
```

An immutable ordered sequence of segments representing a phonological
word.

Words support indexing and slicing — integer indices return a `Segment`,
while slices return a new `Word`. BOS and EOS boundary pseudo-segments
can be added via `FeatureSystem.add_boundaries()`.

Use `FeatureSystem.word()` or `Inventory.tokenize()` to construct.

**Attributes**:

- `segments` - An ordered tuple of Segment objects.

<a id="logical_phonology.word.Word.__len__"></a>

#### \_\_len\_\_

```python
def __len__() -> int
```

Return the number of segments in the word, including any boundaries.

<a id="logical_phonology.word.Word.__iter__"></a>

#### \_\_iter\_\_

```python
def __iter__() -> Iterator[Segment]
```

Iterate over the segments in the word.

<a id="logical_phonology.word.Word.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(index: int | slice) -> "Segment | Word"
```

Return a segment by index or a new word by slice.

**Arguments**:

- `index` - An integer index or slice.
  

**Returns**:

  A Segment if index is an integer, or a new Word if index is a slice.

<a id="logical_phonology.word.Word.__add__"></a>

#### \_\_add\_\_

```python
def __add__(other: "Word | Segment") -> "Word"
```

Concatenate this word with another word or segment.

**Arguments**:

- `other` - A Word or Segment to append.
  

**Returns**:

  A new Word containing the segments of this word followed by
  the segments of other.
  

**Notes**:

  Boundaries are not checked — callers are responsible for
  ensuring BOS and EOS appear only at the edges of the final word.

<a id="logical_phonology.word.Word.unify"></a>

#### unify

```python
def unify(other: "Word") -> "Word"
```

Unify two words element-wise. Also available as the `|` operator.

<a id="logical_phonology.word.Word.__or__"></a>

#### \_\_or\_\_

```python
def __or__(other: "Word") -> "Word"
```

Unify this word with another element-wise. See ``unify``.

<a id="logical_phonology.word.Word.subtract"></a>

#### subtract

```python
def subtract(other: "Word") -> "Word"
```

Subtract two words element-wise. Also available as the `-` operator.

<a id="logical_phonology.word.Word.__sub__"></a>

#### \_\_sub\_\_

```python
def __sub__(other: "Word") -> "Word"
```

Subtract another word from this one element-wise. See ``subtract``.

<a id="logical_phonology.word.Word.intersect"></a>

#### intersect

```python
def intersect(other: "Word") -> "Word"
```

Intersect two words element-wise. Also available as the `&` operator.

<a id="logical_phonology.word.Word.__and__"></a>

#### \_\_and\_\_

```python
def __and__(other: "Word") -> "Word"
```

Intersect this word with another element-wise. See ``intersect``.

<a id="logical_phonology.word.Word.project"></a>

#### project

```python
def project(restricted_feature_set: Collection[str]) -> "Word"
```

Return a new Word with each segment projected onto the feature set.

<a id="logical_phonology.word.Word.__matmul__"></a>

#### \_\_matmul\_\_

```python
def __matmul__(restricted_feature_set: Collection[str]) -> "Word"
```

Project each segment onto a feature set. See ``project``.

<a id="logical_phonology.word.Word.ngrams"></a>

#### ngrams

```python
def ngrams(n: int) -> list[tuple[int, int, "Word"]]
```

Return all contiguous n-grams of this word.

**Arguments**:

- `n` - The length of each n-gram. Must be positive.
  

**Returns**:

  A list of `(start, end, subsequence)` tuples, where `end` is
  exclusive.
  

**Raises**:

- `ValueError` - If `n` is not positive.

<a id="logical_phonology.word.Word.tier"></a>

#### tier

```python
def tier(nc: NaturalClass | NaturalClassUnion) -> "Word"
```

Return the subsequence of segments belonging to a natural class.

**Arguments**:

- `nc` - A `NaturalClass` or `NaturalClassUnion` to match against.
  

**Returns**:

  A new Word containing only the segments of this word that belong
  to `nc`, in their original relative order.

<a id="logical_phonology.word.Word.find_all"></a>

#### find\_all

```python
def find_all(ncs: "NaturalClassSequence") -> list[int]
```

Return start indices of all matches of a natural class sequence.

**Arguments**:

- `ncs` - The natural class sequence to search for.
  

**Returns**:

  A list of start indices where `ncs` matches in this word.

<a id="logical_phonology.word.Word.find_after"></a>

#### find\_after

```python
def find_after(pos: int, ncs: "NaturalClassSequence") -> int | None
```

Return the index of the first match at or after pos, or None.

**Arguments**:

- `pos` - The position to start searching from (inclusive).
- `ncs` - The natural class sequence to search for.
  

**Returns**:

  The index of the first matching position, or None if no match found.

<a id="logical_phonology.word.Word.find_before"></a>

#### find\_before

```python
def find_before(pos: int | None, ncs: "NaturalClassSequence") -> int | None
```

Return the index of the last match before pos, or None.

**Arguments**:

- `pos` - Search only positions before this index (exclusive).
  If None, searches the entire word.
- `ncs` - The natural class sequence to search for.
  

**Returns**:

  The index of the last matching position, or None if no match found.

<a id="logical_phonology.word.Word.minimal_pair_with"></a>

#### minimal\_pair\_with

```python
def minimal_pair_with(other: "Word") -> int | None
```

Return the index of the single differing position, or None.

**Arguments**:

- `other` - The word to compare against.
  

**Returns**:

  The index of the unique differing segment if the words differ at
  exactly one position, or None if they have different lengths or
  differ at zero or more than one position.

<a id="logical_phonology.word.Word.as_segment"></a>

#### as\_segment

```python
def as_segment() -> Segment
```

Return the sole segment; raises ValueError if len != 1.

<a id="logical_phonology.word.Word.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Return the canonical string representation of the word.

Words are rendered as angle-bracketed, space-separated segment
strings, e.g. ``<{+F} {-G}>``.

