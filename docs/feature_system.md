# Table of Contents

* [logical\_phonology.feature\_system](#logical_phonology.feature_system)
  * [FeatureSystem](#logical_phonology.feature_system.FeatureSystem)
    * [BOS](#logical_phonology.feature_system.FeatureSystem.BOS)
    * [EOS](#logical_phonology.feature_system.FeatureSystem.EOS)
    * [segment](#logical_phonology.feature_system.FeatureSystem.segment)
    * [word](#logical_phonology.feature_system.FeatureSystem.word)
    * [add\_boundaries](#logical_phonology.feature_system.FeatureSystem.add_boundaries)
    * [natural\_class](#logical_phonology.feature_system.FeatureSystem.natural_class)
    * [natural\_class\_sequence](#logical_phonology.feature_system.FeatureSystem.natural_class_sequence)
    * [inventory](#logical_phonology.feature_system.FeatureSystem.inventory)

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

<a id="logical_phonology.feature_system.FeatureSystem.segment"></a>

#### segment

```python
def segment(features: dict[str, FeatureValue]) -> Segment
```

Construct a Segment from a feature specification.

**Arguments**:

- `features` - A mapping of feature names to FeatureValues. May be
  partial — unspecified features are simply absent from the
  segment's feature bundle.
  

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

  A new Word with `BOS` prepended and `EOS` appended.

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

<a id="logical_phonology.feature_system.FeatureSystem.natural_class_sequence"></a>

#### natural\_class\_sequence

```python
def natural_class_sequence(
        classes: list[NaturalClass]) -> NaturalClassSequence
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

