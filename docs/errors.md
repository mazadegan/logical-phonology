# Table of Contents

* [logical\_phonology.errors](#logical_phonology.errors)
  * [LogicalPhonologyError](#logical_phonology.errors.LogicalPhonologyError)
  * [ValidationError](#logical_phonology.errors.ValidationError)
  * [LoadInventoryError](#logical_phonology.errors.LoadInventoryError)
  * [InventoryFileError](#logical_phonology.errors.InventoryFileError)
  * [InvalidFeatureValueError](#logical_phonology.errors.InvalidFeatureValueError)
  * [UnknownFeatureError](#logical_phonology.errors.UnknownFeatureError)
  * [ReservedFeatureError](#logical_phonology.errors.ReservedFeatureError)
  * [UnificationError](#logical_phonology.errors.UnificationError)
  * [ReservedFeatureUsageError](#logical_phonology.errors.ReservedFeatureUsageError)
  * [UnknownNameError](#logical_phonology.errors.UnknownNameError)
  * [UnknownSegmentError](#logical_phonology.errors.UnknownSegmentError)
  * [AliasError](#logical_phonology.errors.AliasError)
  * [UntokenizableInputError](#logical_phonology.errors.UntokenizableInputError)
  * [AmbiguousTokenizationError](#logical_phonology.errors.AmbiguousTokenizationError)
  * [DuplicateNameError](#logical_phonology.errors.DuplicateNameError)
  * [CombinatoricExplosionError](#logical_phonology.errors.CombinatoricExplosionError)

<a id="logical_phonology.errors"></a>

# logical\_phonology.errors

<a id="logical_phonology.errors.LogicalPhonologyError"></a>

## LogicalPhonologyError Objects

```python
class LogicalPhonologyError(Exception)
```

Base exception for all logical phonology errors.

<a id="logical_phonology.errors.ValidationError"></a>

## ValidationError Objects

```python
class ValidationError(LogicalPhonologyError)
```

Base exception for validation errors.

<a id="logical_phonology.errors.LoadInventoryError"></a>

## LoadInventoryError Objects

```python
class LoadInventoryError(ValidationError)
```

Raised when an inventory file cannot be parsed or loaded.

<a id="logical_phonology.errors.InventoryFileError"></a>

## InventoryFileError Objects

```python
class InventoryFileError(LoadInventoryError)
```

Raised when an inventory file is malformed or cannot be read.

<a id="logical_phonology.errors.InvalidFeatureValueError"></a>

## InvalidFeatureValueError Objects

```python
class InvalidFeatureValueError(ValidationError)
```

Raised when a string cannot be parsed as a FeatureValue.

**Attributes**:

- `value` - The invalid string that was passed to `FeatureValue.from_str`.

<a id="logical_phonology.errors.UnknownFeatureError"></a>

## UnknownFeatureError Objects

```python
class UnknownFeatureError(ValidationError)
```

Raised when a feature name is not in the valid feature set.

**Attributes**:

- `unknown` - The set of unrecognized feature names.

<a id="logical_phonology.errors.ReservedFeatureError"></a>

## ReservedFeatureError Objects

```python
class ReservedFeatureError(ValidationError)
```

Raised when a FeatureSystem is initialized with reserved feature names.

Reserved feature names (e.g. 'BOS', 'EOS') are used internally by the
library and cannot be used in user-defined feature systems.

**Attributes**:

- `conflicts` - The set of reserved feature names that were used.

<a id="logical_phonology.errors.UnificationError"></a>

## UnificationError Objects

```python
class UnificationError(ValidationError)
```

Raised by `Segment.unify_strict` when two segments have conflicting
values for the same feature.

**Attributes**:

- `feature` - The feature name on which unification failed.
- `v1` - The value of the feature in the first segment.
- `v2` - The conflicting value of the feature in the second segment.

<a id="logical_phonology.errors.ReservedFeatureUsageError"></a>

## ReservedFeatureUsageError Objects

```python
class ReservedFeatureUsageError(ValidationError)
```

Raised when a user attempts to construct a segment using reserved
feature names such as 'BOS' or 'EOS'.

**Attributes**:

- `features` - The set of reserved feature names that were used.

<a id="logical_phonology.errors.UnknownNameError"></a>

## UnknownNameError Objects

```python
class UnknownNameError(ValidationError)
```

Raised when a name is not found in an inventory.

**Attributes**:

- `name` - The name that was not found.

<a id="logical_phonology.errors.UnknownSegmentError"></a>

## UnknownSegmentError Objects

```python
class UnknownSegmentError(ValidationError)
```

Raised when a segment is not found in an inventory.

**Attributes**:

- `segment` - The segment that was not found.

<a id="logical_phonology.errors.AliasError"></a>

## AliasError Objects

```python
class AliasError(ValidationError)
```

Raised when aliases are detected in an inventory where
`allow_aliases=False`.

**Attributes**:

- `aliased` - A dict mapping canonical segment forms to the list of
  names that refer to them.

<a id="logical_phonology.errors.UntokenizableInputError"></a>

## UntokenizableInputError Objects

```python
class UntokenizableInputError(ValidationError)
```

Raised when a string cannot be tokenized using the inventory.

**Attributes**:

- `input_str` - The input string that could not be tokenized.

<a id="logical_phonology.errors.AmbiguousTokenizationError"></a>

## AmbiguousTokenizationError Objects

```python
class AmbiguousTokenizationError(ValidationError)
```

Raised when a string has multiple valid tokenizations and
`allow_ambiguity=False`.

**Attributes**:

- `input_str` - The input string that was ambiguously tokenized.
- `tokenizations` - All possible tokenizations as a list of Words.

<a id="logical_phonology.errors.DuplicateNameError"></a>

## DuplicateNameError Objects

```python
class DuplicateNameError(ValidationError)
```

Raised when attempting to add a name to an inventory that already
exists.

**Attributes**:

- `conflicts` - The set of names that already exist in the inventory.

<a id="logical_phonology.errors.CombinatoricExplosionError"></a>

## CombinatoricExplosionError Objects

```python
class CombinatoricExplosionError(ValidationError)
```

Raised when `full_inventory()` is called with a feature set that is
too large to enumerate safely.

The number of possible segments grows as 3^n where n is the number of
features, so large feature sets can produce an intractable number of
segments.

**Attributes**:

- `max_length` - The maximum allowed feature set size.
- `actual_length` - The actual size of the feature set.

