# Table of Contents

* [logical\_phonology.feature\_value](#logical_phonology.feature_value)
  * [FeatureValue](#logical_phonology.feature_value.FeatureValue)
    * [\_\_str\_\_](#logical_phonology.feature_value.FeatureValue.__str__)
    * [from\_str](#logical_phonology.feature_value.FeatureValue.from_str)
  * [POS](#logical_phonology.feature_value.POS)
  * [NEG](#logical_phonology.feature_value.NEG)

<a id="logical_phonology.feature_value"></a>

# logical\_phonology.feature\_value

<a id="logical_phonology.feature_value.FeatureValue"></a>

## FeatureValue Objects

```python
class FeatureValue(Enum)
```

A binary feature value in Logical Phonology.

A segment may also be underspecified for a feature, in which case
that feature is simply absent from the segment's feature bundle.

**Attributes**:

- `POS` - Positive feature value, represented as `+`.
- `NEG` - Negative feature value, represented as `-`.

<a id="logical_phonology.feature_value.FeatureValue.__str__"></a>

#### \_\_str\_\_

```python
def __str__() -> str
```

Return the string representation of the feature value.

<a id="logical_phonology.feature_value.FeatureValue.from_str"></a>

#### from\_str

```python
@classmethod
def from_str(cls, input_string: str) -> "FeatureValue"
```

Parse a string into a FeatureValue.

**Arguments**:

- `input_string` - A string representation of a feature value. Must be
  `'+'` or `'-'`.
  

**Returns**:

  The corresponding FeatureValue.
  

**Raises**:

- `InvalidFeatureValueError` - If the string is not a valid
  feature value.

<a id="logical_phonology.feature_value.POS"></a>

#### POS

Alias for `FeatureValue.POS`.

<a id="logical_phonology.feature_value.NEG"></a>

#### NEG

Alias for `FeatureValue.NEG`.

