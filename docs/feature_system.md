# Table of Contents

* [logical\_phonology.feature\_system](#logical_phonology.feature_system)
  * [FeatureSystem](#logical_phonology.feature_system.FeatureSystem)
    * [from\_features](#logical_phonology.feature_system.FeatureSystem.from_features)
    * [BOS](#logical_phonology.feature_system.FeatureSystem.BOS)
    * [EOS](#logical_phonology.feature_system.FeatureSystem.EOS)
    * [BOS\_NC](#logical_phonology.feature_system.FeatureSystem.BOS_NC)
    * [EOS\_NC](#logical_phonology.feature_system.FeatureSystem.EOS_NC)
    * [segment](#logical_phonology.feature_system.FeatureSystem.segment)
    * [word](#logical_phonology.feature_system.FeatureSystem.word)
    * [add\_boundaries](#logical_phonology.feature_system.FeatureSystem.add_boundaries)
    * [remove\_boundaries](#logical_phonology.feature_system.FeatureSystem.remove_boundaries)
    * [natural\_class](#logical_phonology.feature_system.FeatureSystem.natural_class)
    * [natural\_class\_union](#logical_phonology.feature_system.FeatureSystem.natural_class_union)
    * [natural\_class\_sequence](#logical_phonology.feature_system.FeatureSystem.natural_class_sequence)
    * [inventory](#logical_phonology.feature_system.FeatureSystem.inventory)
    * [full\_inventory](#logical_phonology.feature_system.FeatureSystem.full_inventory)

<a id="logical_phonology.feature_system"></a>

# logical\_phonology.feature\_system

<a id="logical_phonology.feature_system.FeatureSystem"></a>

## FeatureSystem Objects

```python
@dataclass(frozen=True)
class FeatureSystem()
```

The central factory object for all Logical Phonology primitives.

A `FeatureSystem` defines the universal set of valid features for an
analysis. All LP objects — segments, natural classes, natural class
sequences, words, and inventories — are constructed through a
`FeatureSystem` instance, ensuring that feature validity is enforced
at construction time.

The feature names `'BOS'` and `'EOS'` are reserved and cannot be used
in user-defined feature systems.

**Attributes**:

- `valid_features` - The frozenset of valid feature names for this system.
  

**Raises**:

- `ReservedFeatureError` - If any feature name in `valid_features` is
  reserved.

<a id="logical_phonology.feature_system.FeatureSystem.from_features"></a>

#### from\_features

```python
@classmethod
def from_features(cls, features: Collection[str]) -> "FeatureSystem"
```

Construct a FeatureSystem from any collection of feature names.

**Arguments**:

- `features` - Feature names as a collection, e.g. list, tuple, set, or
  frozenset.
  

**Returns**:

  A FeatureSystem with immutable `valid_features`.
  

**Raises**:

- `ValueError` - If duplicate feature names are provided.
- `ReservedFeatureError` - If reserved names are included.

<a id="logical_phonology.feature_system.FeatureSystem.BOS"></a>

#### BOS

```python
@property
def BOS() -> Segment
```

The beginning-of-string boundary pseudo-segment (⋉).

This is a reserved segment with a single feature `{'BOS': POS}`.
It is automatically added by `add_boundaries()` and recognized
by `Inventory.tokenize()` and `Inventory.render()`.

<a id="logical_phonology.feature_system.FeatureSystem.EOS"></a>

#### EOS

```python
@property
def EOS() -> Segment
```

The end-of-string boundary pseudo-segment (⋊).

This is a reserved segment with a single feature `{'EOS': POS}`.
It is automatically added by `add_boundaries()` and recognized
by `Inventory.tokenize()` and `Inventory.render()`.

<a id="logical_phonology.feature_system.FeatureSystem.BOS_NC"></a>

#### BOS\_NC

```python
@property
def BOS_NC() -> NaturalClass
```

Returns a natural match that contains only the BOS pseudo-segment.

<a id="logical_phonology.feature_system.FeatureSystem.EOS_NC"></a>

#### EOS\_NC

```python
@property
def EOS_NC() -> NaturalClass
```

Returns a natural match that contains only the EOS pseudo-segment.

<a id="logical_phonology.feature_system.FeatureSystem.segment"></a>

#### segment

```python
def segment(features: Mapping[str, object]) -> Segment
```

Construct a Segment from a feature specification.

**Arguments**:

- `features` - A mapping of feature names to `FeatureValue` or `'+'`/`'-'`
  strings. May be partial — unspecified features are simply absent
  from the segment's feature bundle.
  

**Returns**:

  A new Segment with the given feature specification.
  

**Raises**:

- `ReservedFeatureUsageError` - If any feature name is reserved.
- `UnknownFeatureError` - If any feature name is not in `valid_features`.

<a id="logical_phonology.feature_system.FeatureSystem.word"></a>

#### word

```python
def word(segments: list[Segment]) -> Word
```

Construct a Word from a list of segments.

**Arguments**:

- `segments` - An ordered list of Segment objects.
  

**Returns**:

  A new Word containing the given segments.

<a id="logical_phonology.feature_system.FeatureSystem.add_boundaries"></a>

#### add\_boundaries

```python
def add_boundaries(word: Word) -> Word
```

Return a new Word with BOS and EOS boundary pseudo-segments added.

**Arguments**:

- `word` - The word to add boundaries to.

**Returns**:

  A new Word with `BOS` prepended and `EOS` appended, if not already
  present.

<a id="logical_phonology.feature_system.FeatureSystem.remove_boundaries"></a>

#### remove\_boundaries

```python
def remove_boundaries(word: Word) -> Word
```

Return a new Word with BOS and EOS boundary pseudo-segments removed.

**Arguments**:

- `word` - The word to remove boundaries from.

**Returns**:

  A new Word with leading `BOS` and trailing `EOS` removed, if
  present.

<a id="logical_phonology.feature_system.FeatureSystem.natural_class"></a>

#### natural\_class

```python
def natural_class(features: dict[str, FeatureValue]) -> NaturalClass
```

Construct a NaturalClass from a feature specification.

Natural classes may reference reserved features such as 'BOS' and 'EOS'
to match boundary pseudo-segments.

**Arguments**:

- `features` - A partial mapping of feature names to FeatureValues
  defining the class.
  

**Returns**:

  A new NaturalClass with the given feature specification.
  

**Raises**:

- `UnknownFeatureError` - If any feature name is not in `valid_features`
  and is not a reserved feature.

<a id="logical_phonology.feature_system.FeatureSystem.natural_class_union"></a>

#### natural\_class\_union

```python
def natural_class_union(classes: list[NaturalClass]) -> NaturalClassUnion
```

Construct a NaturalClassUnion from a list of NaturalClass objects.

<a id="logical_phonology.feature_system.FeatureSystem.natural_class_sequence"></a>

#### natural\_class\_sequence

```python
def natural_class_sequence(
        classes: list[NaturalClass | NaturalClassUnion]
) -> NaturalClassSequence
```

Construct a NaturalClassSequence from an ordered list of natural
classes.

**Arguments**:

- `classes` - An ordered list of NaturalClass objects.
  

**Returns**:

  A new NaturalClassSequence containing the given natural classes.

<a id="logical_phonology.feature_system.FeatureSystem.inventory"></a>

#### inventory

```python
def inventory(name_to_segment: dict[str, Segment],
              allow_aliases: bool = True) -> Inventory
```

Construct an Inventory from a mapping of names to segments.

**Arguments**:

- `name_to_segment` - A mapping of symbol names to Segment objects.
  Multiple names may map to the same segment (aliases).
- `allow_aliases` - If True (default), multiple names may map to the
  same segment. If False, raises AliasError if aliases are
  detected.
  

**Returns**:

  A new Inventory with the given named segments.
  

**Raises**:

- `AliasError` - If aliases are detected and `allow_aliases=False`.
- `DuplicateNameError` - If any name collides with a reserved or
  canonical form name.

<a id="logical_phonology.feature_system.FeatureSystem.full_inventory"></a>

#### full\_inventory

```python
def full_inventory(max_feature_set_length: int = 8) -> Inventory
```

Construct an inventory containing all possible segments over this
feature system.

Enumerates all combinations of POS, NEG, and unspecified for every
feature, producing 3^n segments where n is the number of features.
Each segment is named by its canonical form (e.g. `{+F1-F2}`).

This is useful as a foundation for use cases where every possible
segment must be reachable. Users can then extend the result with
human-readable names via `Inventory.extend()`.

**Arguments**:

- `max_feature_set_length` - The maximum allowed number of features.
  Defaults to 8 (producing at most 6561 segments). Raise this
  limit with caution — at n=10 the inventory has 59049 segments.
  

**Returns**:

  An Inventory containing all possible segments over this feature
  system.
  

**Raises**:

- `CombinatoricExplosionError` - If the number of features exceeds
  `max_feature_set_length`.

