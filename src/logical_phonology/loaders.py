from __future__ import annotations

import csv
from pathlib import Path

from .errors import (
    InventoryFileError,
    LoadInventoryError,
    ReservedFeatureError,
)
from .feature_system import FeatureSystem
from .feature_value import FeatureValue
from .inventory import Inventory


def load_inventory_from_file(
    path: Path | str, delimiter: str = ",", strict: bool = False
) -> tuple[FeatureSystem, Inventory]:
    """Load a feature inventory from a CSV or TSV file.

    The file must have a header row whose first cell is the symbol column
    label (e.g. 'ipa') and whose remaining cells are feature names. Each
    subsequent row has a symbol name in the first cell and feature values
    (+, -, 0, or empty for unspecified) in the remaining cells.

    Args:
        path: Path to the inventory file.
        delimiter: Column delimiter. Defaults to ',' for CSV; use '\\t' for
            TSV.
        strict: If True, require every data row to have the same number of
            columns as the header row.

    Returns:
        A `(FeatureSystem, Inventory)` pair loaded from the file.

    Raises:
        LoadInventoryError: If the file is malformed.
        InventoryFileError: If the file cannot be read or contains invalid
            structure.
        ReservedFeatureError: If the file defines reserved feature names.
    """
    path = Path(path)
    try:
        with path.open(newline="") as f:
            rows = [row for row in csv.reader(f, delimiter=delimiter) if row]
    except OSError as e:
        raise InventoryFileError(f"Cannot read '{path}': {e}") from e
    except csv.Error as e:
        raise InventoryFileError(f"Cannot parse '{path}': {e}") from e

    if not rows:
        raise InventoryFileError(f"'{path}' is empty.")
    if len(rows[0]) < 2:
        raise InventoryFileError(f"'{path}' has no feature columns.")

    header = [cell.strip() for cell in rows[0]]
    features = header[1:]

    if any(not f for f in features):
        raise InventoryFileError(
            f"'{path}' contains an empty feature name in the header row."
        )
    if len(set(features)) != len(features):
        raise InventoryFileError(
            f"'{path}' contains duplicate feature names in the header row."
        )

    data_rows = rows[1:]
    if not data_rows:
        raise InventoryFileError(f"'{path}' has no segment rows.")

    try:
        fs = FeatureSystem(frozenset(features))
    except ReservedFeatureError as e:
        raise LoadInventoryError(
            f"'{path}' contains reserved feature names: {e.conflicts}."
        ) from e

    if strict:
        expected_len = len(features) + 1
        for row in data_rows:
            if len(row) != expected_len:
                name = row[0].strip() if row else ""
                raise InventoryFileError(
                    f"Row '{name}' has {len(row) - 1} values. "
                    f"Expected {len(features)}."
                )

    seen_names: set[str] = set()
    segment_specs: dict[str, dict[str, FeatureValue]] = {}

    for row in data_rows:
        name = row[0].strip() if row else ""
        if not name:
            raise InventoryFileError(
                f"'{path}' contains a row with no symbol name."
            )
        if name in seen_names:
            raise InventoryFileError(
                f"'{path}' contains duplicate symbol name '{name}'."
            )
        seen_names.add(name)
        spec: dict[str, FeatureValue] = {}
        values = row[1:]
        for i, feature in enumerate(features):
            val = values[i].strip() if i < len(values) else ""
            if val in ("", "0"):
                continue
            if val in ("+", "-"):
                spec[feature] = FeatureValue.from_str(val)
                continue
            raise InventoryFileError(
                f"Invalid value '{val}' for feature '{feature}' and symbol "
                f"'{name}' in '{path}'."
            )
        segment_specs[name] = spec

    inventory = fs.inventory(
        {name: fs.segment(spec) for name, spec in segment_specs.items()}
    )
    return fs, inventory
