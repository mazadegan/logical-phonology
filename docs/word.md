# Table of Contents

* [logical\_phonology.word](#logical_phonology.word)
  * [Word](#logical_phonology.word.Word)
    * [\_\_len\_\_](#logical_phonology.word.Word.__len__)
    * [\_\_iter\_\_](#logical_phonology.word.Word.__iter__)
    * [\_\_getitem\_\_](#logical_phonology.word.Word.__getitem__)
    * [\_\_add\_\_](#logical_phonology.word.Word.__add__)
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

<a id="logical_phonology.word.Word.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Return the canonical string representation of the word.

Words are rendered as angle-bracketed, space-separated segment
strings, e.g. ``<{+F} {-G}>``.

