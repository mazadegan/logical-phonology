# Table of Contents

* [logical\_phonology.natural\_class\_union](#logical_phonology.natural_class_union)
  * [NaturalClassUnion](#logical_phonology.natural_class_union.NaturalClassUnion)
    * [\_\_contains\_\_](#logical_phonology.natural_class_union.NaturalClassUnion.__contains__)
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

