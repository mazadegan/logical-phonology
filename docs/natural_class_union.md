# Table of Contents

* [logical\_phonology.natural\_class\_union](#logical_phonology.natural_class_union)
  * [NaturalClassUnion](#logical_phonology.natural_class_union.NaturalClassUnion)
    * [\_\_contains\_\_](#logical_phonology.natural_class_union.NaturalClassUnion.__contains__)
    * [over](#logical_phonology.natural_class_union.NaturalClassUnion.over)
    * [extension](#logical_phonology.natural_class_union.NaturalClassUnion.extension)
    * [\_\_or\_\_](#logical_phonology.natural_class_union.NaturalClassUnion.__or__)
    * [\_\_str\_\_](#logical_phonology.natural_class_union.NaturalClassUnion.__str__)

<a id="logical_phonology.natural_class_union"></a>

# logical\_phonology.natural\_class\_union

<a id="logical_phonology.natural_class_union.NaturalClassUnion"></a>

## NaturalClassUnion Objects

```python
@dataclass(frozen=True)
class NaturalClassUnion()
```

<a id="logical_phonology.natural_class_union.NaturalClassUnion.__contains__"></a>

#### \_\_contains\_\_

```python
def __contains__(seg: Segment) -> bool
```

Return True if the segment belongs to any class in this union.

<a id="logical_phonology.natural_class_union.NaturalClassUnion.over"></a>

#### over

```python
def over(inv: Inventory, filter_boundaries: bool = True) -> Iterator[Segment]
```

Iterate over all segments in this union over a given inventory.

**Arguments**:

- `inv` - The inventory to evaluate the union over.
- `filter_boundaries` - If True (default), BOS and EOS pseudo-segments
  are excluded from the results.
  

**Returns**:

  An iterator over all segments in the inventory that belong to this
  union.

<a id="logical_phonology.natural_class_union.NaturalClassUnion.extension"></a>

#### extension

```python
def extension(inv: Inventory,
              filter_boundaries: bool = True,
              as_names: bool = False) -> tuple[Segment, ...] | tuple[str, ...]
```

Return the materialized extension of this union over an inventory.

**Arguments**:

- `inv` - The inventory to evaluate the union over.
- `filter_boundaries` - If True (default), BOS and EOS pseudo-segments
  are excluded from the results.
- `as_names` - If True, return inventory names instead of segments.
  

**Returns**:

  A tuple of matching segments (default) or matching names when
  `as_names=True`.

<a id="logical_phonology.natural_class_union.NaturalClassUnion.__or__"></a>

#### \_\_or\_\_

```python
def __or__(other: NaturalClass | NaturalClassUnion) -> NaturalClassUnion
```

Return a new union combining this union with another class or union.

<a id="logical_phonology.natural_class_union.NaturalClassUnion.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Return a canonical bracketed representation of this union.

