# Table of Contents

* [logical\_phonology.natural\_class\_sequence](#logical_phonology.natural_class_sequence)
  * [NaturalClassSequence](#logical_phonology.natural_class_sequence.NaturalClassSequence)
    * [matches\_at](#logical_phonology.natural_class_sequence.NaturalClassSequence.matches_at)
    * [find\_all](#logical_phonology.natural_class_sequence.NaturalClassSequence.find_all)
    * [over](#logical_phonology.natural_class_sequence.NaturalClassSequence.over)
    * [\_\_contains\_\_](#logical_phonology.natural_class_sequence.NaturalClassSequence.__contains__)

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

<a id="logical_phonology.natural_class_sequence.NaturalClassSequence.find_all"></a>

#### find\_all

```python
def find_all(word: Word) -> list[int]
```

Return all positions in the word where the sequence matches.

**Arguments**:

- `word` - The word to search.
  

**Returns**:

  A list of positions where this natural class sequence matches
  as a substring of the word.

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

