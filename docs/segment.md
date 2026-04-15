# Table of Contents

* [logical\_phonology.segment](#logical_phonology.segment)
  * [Segment](#logical_phonology.segment.Segment)
    * [subtract](#logical_phonology.segment.Segment.subtract)
    * [\_\_sub\_\_](#logical_phonology.segment.Segment.__sub__)
    * [unify](#logical_phonology.segment.Segment.unify)
    * [unify\_strict](#logical_phonology.segment.Segment.unify_strict)
    * [\_\_or\_\_](#logical_phonology.segment.Segment.__or__)
    * [project](#logical_phonology.segment.Segment.project)
    * [\_\_and\_\_](#logical_phonology.segment.Segment.__and__)
    * [\_\_hash\_\_](#logical_phonology.segment.Segment.__hash__)
    * [\_\_getitem\_\_](#logical_phonology.segment.Segment.__getitem__)
    * [\_\_contains\_\_](#logical_phonology.segment.Segment.__contains__)
    * [\_\_str\_\_](#logical_phonology.segment.Segment.__str__)
    * [\_\_add\_\_](#logical_phonology.segment.Segment.__add__)

<a id="logical_phonology.segment"></a>

# logical\_phonology.segment

<a id="logical_phonology.segment.Segment"></a>

## Segment Objects

```python
@dataclass(frozen=True)
class Segment()
```

An immutable feature bundle representing a phonological segment.

Use `FeatureSystem.segment()` to construct. Direct construction is
possible but bypasses feature validation.

**Attributes**:

- `features` - An immutable mapping of feature names to FeatureValues.

<a id="logical_phonology.segment.Segment.subtract"></a>

#### subtract

```python
def subtract(other: "Segment") -> "Segment"
```

A \ B = {cF | cF ∈ A ∧ cF ∉ B}

Returns a new segment containing all valued features from this segment
that do not appear with the same value in `other`. Features with
conflicting values are kept. Also available as the `-` operator.

**Arguments**:

- `other` - The segment whose features are subtracted.
  

**Returns**:

  A new Segment with the result of the subtraction.

<a id="logical_phonology.segment.Segment.__sub__"></a>

#### \_\_sub\_\_

```python
def __sub__(other: "Segment") -> "Segment"
```

Subtract another segment's features from this one. See ``subtract``.

<a id="logical_phonology.segment.Segment.unify"></a>

#### unify

```python
def unify(other: "Segment") -> "Segment"
```

A ⊔ B = A ∪ {cF | cF ∈ B ∧ ¬cF ∉ A}

Returns a new segment containing all features from this segment, plus
any features from `other` that do not conflict. Conflicting features
are silently ignored. Also available as the `|` operator.

**Arguments**:

- `other` - The segment to unify with.
  

**Returns**:

  A new Segment with the result of unification.

<a id="logical_phonology.segment.Segment.unify_strict"></a>

#### unify\_strict

```python
def unify_strict(other: "Segment") -> "Segment"
```

Same as `unify`, but raises UnificationError on conflicting features.

**Arguments**:

- `other` - The segment to unify with.
  

**Returns**:

  A new Segment with the result of unification.
  

**Raises**:

- `UnificationError` - If both segments specify conflicting values for
  the same feature.

<a id="logical_phonology.segment.Segment.__or__"></a>

#### \_\_or\_\_

```python
def __or__(other: "Segment") -> "Segment"
```

Unify this segment with another. See ``unify``.

<a id="logical_phonology.segment.Segment.project"></a>

#### project

```python
def project(restricted_feature_set: Collection[str]) -> "Segment"
```

Return a new segment containing only the specified features.

Also available as the `&` operator.

**Arguments**:

- `restricted_feature_set` - The collection of feature names to keep.
  

**Returns**:

  A new Segment containing only the features in `restricted_feature_set`.

<a id="logical_phonology.segment.Segment.__and__"></a>

#### \_\_and\_\_

```python
def __and__(restricted_feature_set: Collection[str]) -> "Segment"
```

Project this segment onto a feature set. See ``project``.

<a id="logical_phonology.segment.Segment.__hash__"></a>

#### \_\_hash\_\_

```python
def __hash__() -> int
```

Hash based on the feature bundle.

<a id="logical_phonology.segment.Segment.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(key: str) -> FeatureValue
```

Look up the value of a feature by name.

<a id="logical_phonology.segment.Segment.__contains__"></a>

#### \_\_contains\_\_

```python
def __contains__(item: str) -> bool
```

Return True if this segment has a value for the given feature name.

<a id="logical_phonology.segment.Segment.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Return the canonical string representation of the segment.

Features are sorted alphabetically and formatted as `{+F1-F2}`.
This canonical form is used as the name for aliased segments in
an Inventory.

<a id="logical_phonology.segment.Segment.__add__"></a>

#### \_\_add\_\_

```python
def __add__(other: "Segment | Word") -> "Word"
```

Concatenate this segment with another segment or word.

**Arguments**:

- `other` - A Segment or Word to append.
  

**Returns**:

  A new Word with this segment followed by the segments of other.
  

**Notes**:

  Boundaries are not checked — callers are responsible for
  ensuring BOS and EOS appear only at the edges of the final word.

