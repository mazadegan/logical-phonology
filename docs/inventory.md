# Table of Contents

* [logical\_phonology.inventory](#logical_phonology.inventory)
  * [ExtensionEntry](#logical_phonology.inventory.ExtensionEntry)
  * [Inventory](#logical_phonology.inventory.Inventory)
    * [render](#logical_phonology.inventory.Inventory.render)
    * [tokenize](#logical_phonology.inventory.Inventory.tokenize)
    * [iter\_extension](#logical_phonology.inventory.Inventory.iter_extension)
    * [extend](#logical_phonology.inventory.Inventory.extend)
    * [\_\_contains\_\_](#logical_phonology.inventory.Inventory.__contains__)
    * [\_\_len\_\_](#logical_phonology.inventory.Inventory.__len__)
    * [\_\_getitem\_\_](#logical_phonology.inventory.Inventory.__getitem__)
    * [name\_of](#logical_phonology.inventory.Inventory.name_of)
    * [min\_intensions](#logical_phonology.inventory.Inventory.min_intensions)
    * [minimal\_pairs](#logical_phonology.inventory.Inventory.minimal_pairs)
    * [contrasts\_for](#logical_phonology.inventory.Inventory.contrasts_for)
    * [save](#logical_phonology.inventory.Inventory.save)
    * [extensions\_to\_intensions](#logical_phonology.inventory.Inventory.extensions_to_intensions)

<a id="logical_phonology.inventory"></a>

# logical\_phonology.inventory

<a id="logical_phonology.inventory.ExtensionEntry"></a>

## ExtensionEntry Objects

```python
@dataclass(frozen=True)
class ExtensionEntry()
```

The intensions and minimal intensions for a single extension.

**Attributes**:

- `intensions` - All natural classes that produce this extension.
- `minimal_intensions` - The subset of intensions with fewest features.

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
        obj: NaturalClass | NaturalClassUnion | NaturalClassSequence,
        filter_boundaries: bool = True) -> Iterator[Segment] | Iterator[Word]
```

Iterate over all members of a natural class, union, or sequence.

**Arguments**:

- `obj` - A NaturalClass, NaturalClassUnion, or NaturalClassSequence.
- `filter_boundaries` - If True (default), BOS and EOS pseudo-segments
  are excluded from results.
  

**Returns**:

  An iterator over Segments if `obj` is a NaturalClass or
  NaturalClassUnion, or an iterator over Words if `obj` is a
  NaturalClassSequence.

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

<a id="logical_phonology.inventory.Inventory.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(name: str) -> Segment
```

Look up a segment by name.

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

<a id="logical_phonology.inventory.Inventory.min_intensions"></a>

#### min\_intensions

```python
def min_intensions(segments: Collection[Segment],
                   features: Collection[str] | None = None,
                   *,
                   filter_boundaries: bool = True,
                   max_features: int = 8) -> list[NaturalClass]
```

Return all minimal natural classes with an exact target extension.

The search space is derived from features common to all target
segments (same feature and same value). If `features` is provided, it
further restricts this common-feature set. Candidate classes are
evaluated with bit masks over the inventory and matched by exact
extension equality.

**Arguments**:

- `segments` - Target extension as a collection of segments.
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
- `UnknownSegmentError` - If any target segment is not in this inventory.
- `UnknownFeatureError` - If any searched feature is unknown.
- `ValueError` - If the searched feature count exceeds `max_features`.

<a id="logical_phonology.inventory.Inventory.minimal_pairs"></a>

#### minimal\_pairs

```python
def minimal_pairs(max_distance: int = 1) -> list[tuple[str, str, int]]
```

Return all segment pairs within a given feature distance.

**Arguments**:

- `max_distance` - Maximum Hamming distance between segment pairs.
  Defaults to 1 (classic minimal pairs).
  

**Returns**:

  A list of (name1, name2, distance) tuples for each pair of named
  segments whose Hamming distance is at most `max_distance`.

<a id="logical_phonology.inventory.Inventory.contrasts_for"></a>

#### contrasts\_for

```python
def contrasts_for(feature: str, measure_absence: bool = False) -> bool
```

Return True if the feature distinguishes any segment pair.

**Arguments**:

- `feature` - The feature name to test.
- `measure_absence` - If True, treat present-vs-absent as a contrast.
  If False (default), only count +/- oppositions where both
  segments specify the feature.
  

**Returns**:

  True if at least one pair of named segments is distinguished by
  this feature.

<a id="logical_phonology.inventory.Inventory.save"></a>

#### save

```python
def save(path: "Path | str", delimiter: str = ",") -> None
```

Save this inventory to a CSV or TSV file.

Writes a header row with 'ipa' followed by sorted feature names, then
one row per user-named segment with +/-/0 values for each feature.

**Arguments**:

- `path` - Path to write the file to.
- `delimiter` - Column delimiter. Defaults to ',' for CSV; use '\t'
  for TSV.

<a id="logical_phonology.inventory.Inventory.extensions_to_intensions"></a>

#### extensions\_to\_intensions

```python
def extensions_to_intensions(
        features: Collection[str] | None = None,
        *,
        filter_boundaries: bool = True,
        max_features: int = 8) -> dict[frozenset[Segment], ExtensionEntry]
```

Map each non-empty extension to its intensions and minimal intensions.

Enumerates all natural classes over the given feature set, groups them
by the set of inventory segments they pick out, and identifies the
minimal intensions for each group. Uses bitmask evaluation for
efficiency.

**Arguments**:

- `features` - Feature names to enumerate over. Defaults to all features
  in this feature system.
- `filter_boundaries` - If True (default), BOS/EOS are excluded.
- `max_features` - Maximum number of features allowed. Defaults to 8.
  

**Returns**:

  A dict mapping each non-empty extension (frozenset of Segments) to
  an ExtensionEntry with its intensions and minimal intensions.
  

**Raises**:

- `UnknownFeatureError` - If any feature is not in this feature system.
- `ValueError` - If the feature count exceeds `max_features`.

