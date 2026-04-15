# Table of Contents

* [logical\_phonology.loaders](#logical_phonology.loaders)
  * [load\_inventory\_from\_file](#logical_phonology.loaders.load_inventory_from_file)

<a id="logical_phonology.loaders"></a>

# logical\_phonology.loaders

<a id="logical_phonology.loaders.load_inventory_from_file"></a>

#### load\_inventory\_from\_file

```python
def load_inventory_from_file(
        path: Path | str,
        delimiter: str = ",",
        strict: bool = False) -> tuple[FeatureSystem, Inventory]
```

Load a feature inventory from a CSV or TSV file.

The file must have segment names in the first row and feature names in the
first column. Cell values may be '+', '-', '0', or empty for
underspecified features.

**Arguments**:

- `path` - Path to the inventory file.
- `delimiter` - Column delimiter. Defaults to ',' for CSV; use '\t' for
  TSV.
- `strict` - If True, require every data row to have the same number of
  columns as the header row.
  

**Returns**:

  A `(FeatureSystem, Inventory)` pair loaded from the file.
  

**Raises**:

- `LoadInventoryError` - If the file is malformed.
- `InventoryFileError` - If the file cannot be read or contains invalid
  structure.
- `ReservedFeatureError` - If the file defines reserved feature names.

