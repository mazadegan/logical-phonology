# Table of Contents

* [logical\_phonology.natural\_class](#logical_phonology.natural_class)
  * [NaturalClass](#logical_phonology.natural_class.NaturalClass)
    * [over](#logical_phonology.natural_class.NaturalClass.over)
    * [extension](#logical_phonology.natural_class.NaturalClass.extension)
    * [subintensions](#logical_phonology.natural_class.NaturalClass.subintensions)
    * [\_\_contains\_\_](#logical_phonology.natural_class.NaturalClass.__contains__)
    * [\_\_hash\_\_](#logical_phonology.natural_class.NaturalClass.__hash__)
    * [\_\_str\_\_](#logical_phonology.natural_class.NaturalClass.__str__)
    * [\_\_or\_\_](#logical_phonology.natural_class.NaturalClass.__or__)

<a id="logical_phonology.natural_class"></a>

# logical\_phonology.natural\_class

<a id="logical_phonology.natural_class.NaturalClass"></a>

## NaturalClass Objects

```python
@dataclass(frozen=True)
class NaturalClass()
```

An immutable partial feature specification defining a set of segments.

A natural class is defined by a set of features and their values.
A segment belongs to a natural class if it has at least the feature
values specified.

Use `FeatureSystem.natural_class()` to construct.

**Attributes**:

- `feature_specification` - An immutable mapping of feature names to
  FeatureValues defining the class.

<a id="logical_phonology.natural_class.NaturalClass.over"></a>

#### over

```python
def over(inv: Inventory, filter_boundaries: bool = True) -> Iterator[Segment]
```

Iterate over all segments in this natural class over a given inventory.

**Arguments**:

- `inv` - The inventory to evaluate the natural class over.
- `filter_boundaries` - If True (default), BOS and EOS pseudo-segments
  are excluded from the results.
  

**Returns**:

  An iterator over all segments in the inventory that belong to
  this natural class.

<a id="logical_phonology.natural_class.NaturalClass.extension"></a>

#### extension

```python
def extension(inv: Inventory,
              filter_boundaries: bool = True,
              as_names: bool = False) -> tuple[Segment, ...] | tuple[str, ...]
```

Return the materialized extension of this natural class over an
inventory.

**Arguments**:

- `inv` - The inventory to evaluate the natural class over.
- `filter_boundaries` - If True (default), BOS and EOS pseudo-segments
  are excluded from the results.
- `as_names` - If True, return inventory names instead of segments.
  

**Returns**:

  A tuple of matching segments (default) or matching names when
  `as_names=True`.

<a id="logical_phonology.natural_class.NaturalClass.subintensions"></a>

#### subintensions

```python
def subintensions(include_self: bool = False,
                  include_universal: bool = False,
                  max_features: int = 8) -> Iterator["NaturalClass"]
```

Yield natural classes formed from subsets of this class's features.

By default, excludes the original class and the empty (universal)
class. The number of yielded classes grows as 2^n where n is the
number of features.

**Arguments**:

- `include_self` - If True, include the full specification.
- `include_universal` - If True, include the empty specification.
- `max_features` - Maximum number of features allowed for generation.
  

**Yields**:

  NaturalClass objects built from subset feature specifications.
  

**Raises**:

- `CombinatoricExplosionError` - If the number of features exceeds
  `max_features`.

<a id="logical_phonology.natural_class.NaturalClass.__contains__"></a>

#### \_\_contains\_\_

```python
def __contains__(s: Segment) -> bool
```

Return True if the segment belongs to this natural class.

A segment belongs to a natural class if its feature bundle contains
all the feature-value pairs specified by the class. Also available
via the `in` operator.

**Arguments**:

- `s` - The segment to test for membership.
  

**Returns**:

  True if the segment belongs to this natural class, False otherwise.

<a id="logical_phonology.natural_class.NaturalClass.__hash__"></a>

#### \_\_hash\_\_

```python
def __hash__() -> int
```

Hash based on the feature specification.

<a id="logical_phonology.natural_class.NaturalClass.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Return a canonical bracketed representation of this natural class.

Features are sorted alphabetically and formatted as
``[{+F1,-F2}]``.

<a id="logical_phonology.natural_class.NaturalClass.__or__"></a>

#### \_\_or\_\_

```python
def __or__(other: NaturalClass | NaturalClassUnion) -> NaturalClassUnion
```

Return a union of this natural class with another class or union.

