# Table of Contents

* [logical\_phonology.inventory](#logical_phonology.inventory)
  * [Inventory](#logical_phonology.inventory.Inventory)
    * [render](#logical_phonology.inventory.Inventory.render)
    * [tokenize](#logical_phonology.inventory.Inventory.tokenize)
    * [iter\_extension](#logical_phonology.inventory.Inventory.iter_extension)
    * [extend](#logical_phonology.inventory.Inventory.extend)
    * [\_\_contains\_\_](#logical_phonology.inventory.Inventory.__contains__)
    * [\_\_len\_\_](#logical_phonology.inventory.Inventory.__len__)
    * [segment](#logical_phonology.inventory.Inventory.segment)
    * [\_\_getitem\_\_](#logical_phonology.inventory.Inventory.__getitem__)
    * [name\_of](#logical_phonology.inventory.Inventory.name_of)

<a id="logical_phonology.inventory"></a>

# logical\_phonology.inventory

<a id="logical_phonology.inventory.Inventory"></a>

## Inventory Objects

```python
@dataclass(frozen=True)
class Inventory()
```

A named segment inventory supporting tokenization and rendering.

An inventory maps symbol names to segments, enabling conversion between
string representations and feature bundles. Multiple names may map to
the same segment (aliases), in which case `name_of` returns the
canonical form derived from the segment's feature bundle.

BOS (⋉) and EOS (⋊) boundary pseudo-segments are automatically
registered in every inventory.

Use `FeatureSystem.inventory()` to construct.

**Attributes**:

- `feature_system` - The FeatureSystem this inventory belongs to.
- `name_to_segment` - An immutable mapping of symbol names to Segments,
  including canonical forms for aliased segments and boundary
  pseudo-segments.
- `segment_to_name` - An immutable mapping of Segments to their canonical
  names.
- `names_in_order` - All symbol names in declaration order, used for
  tokenization.
- `user_names` - The frozenset of names explicitly provided by the user,
  excluding auto-generated canonical and reserved names.
- `allow_aliases` - Whether multiple names may map to the same segment.

<a id="logical_phonology.inventory.Inventory.render"></a>

#### render

```python
def render(word: Word) -> str
```

Render a word as a string using inventory names.

Segments with unique names render as their name. Aliased segments
render as their canonical form (e.g. `{-Syllabic}`). Boundary
pseudo-segments render as `⋉` and `⋊`.

**Arguments**:

- `word` - The word to render.
  

**Returns**:

  A string representation of the word.
  

**Raises**:

- `UnknownSegmentError` - If any segment in the word is not in
  this inventory.

<a id="logical_phonology.inventory.Inventory.tokenize"></a>

#### tokenize

```python
def tokenize(input_str: str,
             allow_ambiguity: bool = False) -> Word | list[Word]
```

Tokenize a string into a Word using this inventory.

If the string contains whitespace, it is split on whitespace and each
token is looked up directly. Otherwise, dynamic programming over string
positions is used to find all valid segmentations.

**Arguments**:

- `input_str` - The string to tokenize.
- `allow_ambiguity` - If True, returns all possible tokenizations as a
  list of Words when the input is ambiguous. If False (default),
  raises AmbiguousTokenizationError on ambiguous input.
  

**Returns**:

  A Word if the tokenization is unambiguous, or a list of Words if
  `allow_ambiguity=True` and the input is ambiguous.
  

**Raises**:

- `UntokenizableInputError` - If no valid tokenization exists.
- `AmbiguousTokenizationError` - If multiple tokenizations exist and
  `allow_ambiguity=False`.

<a id="logical_phonology.inventory.Inventory.iter_extension"></a>

#### iter\_extension

```python
def iter_extension(
        obj: NaturalClass | NaturalClassSequence,
        filter_boundaries: bool = True) -> Iterator[Segment] | Iterator[Word]
```

Iterate over all members of a natural class or natural class
sequence.

**Arguments**:

- `obj` - A NaturalClass or NaturalClassSequence to evaluate.
- `filter_boundaries` - If True (default), BOS and EOS pseudo-segments
  are excluded from results.
  

**Returns**:

  An iterator over Segments if `obj` is a NaturalClass, or an
  iterator over Words if `obj` is a NaturalClassSequence.

<a id="logical_phonology.inventory.Inventory.extend"></a>

#### extend

```python
def extend(new_segments: dict[str, Segment]) -> Inventory
```

Return a new Inventory with additional named segments.

The original inventory is unchanged. Only user-provided names are
carried over — canonical forms and reserved names are recomputed.

**Arguments**:

- `new_segments` - A mapping of new symbol names to Segments.
  

**Returns**:

  A new Inventory containing the original segments plus the new ones.
  

**Raises**:

- `DuplicateNameError` - If any new name already exists in the inventory.
- `AliasError` - If any new segment is already in the inventory and `allow_aliases=False`.

<a id="logical_phonology.inventory.Inventory.__contains__"></a>

#### \_\_contains\_\_

```python
def __contains__(item: object) -> bool
```

Return True if the name or segment is in this inventory.

Accepts either a string (name lookup) or a Segment (reverse lookup).

**Arguments**:

- `item` - A string name or Segment to look up.
  

**Returns**:

  True if the item is in this inventory, False otherwise.

<a id="logical_phonology.inventory.Inventory.__len__"></a>

#### \_\_len\_\_

```python
def __len__() -> int
```

Return the number of distinct segments in this inventory.

Counts unique segments, not names — aliases are not double-counted.
Use ``len(self.name_to_segment)`` if you want the total number of
names including aliases and canonical forms.

<a id="logical_phonology.inventory.Inventory.segment"></a>

#### segment

```python
def segment(name: str) -> Segment
```

Look up a segment by name.

Also available via the `[]` operator.

**Arguments**:

- `name` - The symbol name to look up.
  

**Returns**:

  The Segment corresponding to the given name.
  

**Raises**:

- `UnknownNameError` - If the name is not in this inventory.

<a id="logical_phonology.inventory.Inventory.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(name: str) -> Segment
```

Look up a segment by name.

Also available via the ``segment()`` method.

**Arguments**:

- `name` - The symbol name to look up.
  

**Returns**:

  The Segment corresponding to the given name.
  

**Raises**:

- `UnknownNameError` - If the name is not in this inventory.

<a id="logical_phonology.inventory.Inventory.name_of"></a>

#### name\_of

```python
def name_of(seg: Segment) -> str
```

Return the canonical name of a segment in this inventory.

For unambiguous segments, returns the user-provided name. For aliased
segments, returns the canonical form derived from the segment's feature
bundle (e.g. `{-Syllabic}`).

**Arguments**:

- `seg` - The segment to look up.
  

**Returns**:

  The canonical name of the segment.
  

**Raises**:

- `UnknownSegmentError` - If the segment is not in this inventory.

