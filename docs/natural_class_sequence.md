# Table of Contents

* [logical\_phonology.natural\_class\_sequence](#logical_phonology.natural_class_sequence)
  * [NaturalClassSequence](#logical_phonology.natural_class_sequence.NaturalClassSequence)
    * [matches\_at](#logical_phonology.natural_class_sequence.NaturalClassSequence.matches_at)
    * [over](#logical_phonology.natural_class_sequence.NaturalClassSequence.over)
    * [extension](#logical_phonology.natural_class_sequence.NaturalClassSequence.extension)
    * [\_\_len\_\_](#logical_phonology.natural_class_sequence.NaturalClassSequence.__len__)
    * [\_\_contains\_\_](#logical_phonology.natural_class_sequence.NaturalClassSequence.__contains__)
    * [\_\_getitem\_\_](#logical_phonology.natural_class_sequence.NaturalClassSequence.__getitem__)
    * [\_\_add\_\_](#logical_phonology.natural_class_sequence.NaturalClassSequence.__add__)
    * [\_\_str\_\_](#logical_phonology.natural_class_sequence.NaturalClassSequence.__str__)

<a id="logical_phonology.natural_class_sequence"></a>

# logical\_phonology.natural\_class\_sequence

<a id="logical_phonology.natural_class_sequence.NaturalClassSequence"></a>

## NaturalClassSequence Objects

```python
@dataclass(frozen=True)
class NaturalClassSequence()
```

An immutable ordered sequence of natural classes defining a set of words.

A word belongs to a natural class sequence if each of its segments
belongs to the corresponding natural class in the sequence, pointwise.
The sequence also supports substring matching via `matches_at` and
`find_all`.

Use `FeatureSystem.natural_class_sequence()` to construct.

**Attributes**:

- `sequence` - An ordered tuple of NaturalClass objects.

<a id="logical_phonology.natural_class_sequence.NaturalClassSequence.matches_at"></a>

#### matches\_at

```python
def matches_at(word: Word, position: int) -> bool
```

Return True if the sequence matches the word starting at position.

**Arguments**:

- `word` - The word to match against.
- `position` - The index in the word to start matching from.
  

**Returns**:

  True if the subsequence of the word starting at `position` matches
  this natural class sequence, False otherwise.

<a id="logical_phonology.natural_class_sequence.NaturalClassSequence.over"></a>

#### over

```python
def over(inv: Inventory, filter_boundaries: bool = True) -> Iterator[Word]
```

Iterate over all words matching this sequence over a given inventory.

**Arguments**:

- `inv` - The inventory to evaluate the sequence over.
- `filter_boundaries` - If True (default), BOS and EOS pseudo-segments
  are excluded from the results.
  

**Returns**:

  An iterator over all words in the inventory that match this
  natural class sequence.

<a id="logical_phonology.natural_class_sequence.NaturalClassSequence.extension"></a>

#### extension

```python
def extension(inv: Inventory,
              filter_boundaries: bool = True) -> tuple[tuple[str, Word], ...]
```

Return the materialized extension of this sequence over an inventory
as (name, word) pairs.

**Arguments**:

- `inv` - The inventory to evaluate the sequence over.
- `filter_boundaries` - If True (default), BOS and EOS pseudo-segments
  are excluded from the results.
  

**Returns**:

  A tuple of (name, word) pairs for each matching word.

<a id="logical_phonology.natural_class_sequence.NaturalClassSequence.__len__"></a>

#### \_\_len\_\_

```python
def __len__() -> int
```

Return the number of natural classes in this sequence.

<a id="logical_phonology.natural_class_sequence.NaturalClassSequence.__contains__"></a>

#### \_\_contains\_\_

```python
def __contains__(item: Word) -> bool
```

Return True if the word matches this natural class sequence exactly.

The word must have the same length as the sequence, and each segment
must belong to the corresponding natural class, pointwise. Also
available via the `in` operator.

**Arguments**:

- `item` - The word to test for membership.
  

**Returns**:

  True if the word matches this sequence, False otherwise.

<a id="logical_phonology.natural_class_sequence.NaturalClassSequence.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(index: int | slice) -> "NaturalClass | NaturalClassSequence"
```

Return a natural class by index or a subsequence by slice.

**Arguments**:

- `index` - An integer index or slice.
  

**Returns**:

  A NaturalClass if index is an integer, or a new
  NaturalClassSequence if index is a slice.

<a id="logical_phonology.natural_class_sequence.NaturalClassSequence.__add__"></a>

#### \_\_add\_\_

```python
def __add__(
    other: "NaturalClass | NaturalClassUnion | NaturalClassSequence"
) -> "NaturalClassSequence"
```

Return a new sequence with the other class or sequence appended.

<a id="logical_phonology.natural_class_sequence.NaturalClassSequence.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Return a canonical bracketed representation of this sequence.

Elements are rendered as natural-class specs, with unions using `|`,
joined by spaces inside one outer pair of brackets.

