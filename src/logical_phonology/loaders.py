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

    The file must have segment names in the first row and feature names in the
    first column. Cell values may be '+', '-', '0', or empty for
    underspecified features.

    Args:
        path: Path to the inventory file.
        delimiter: Column delimiter. Defaults to ',' for CSV; use '\\t' for
            TSV.
        strict: If True, require every data row to have the same number of columns as the header row.

    Returns:
        A `(FeatureSystem, Inventory)` pair loaded from the file.

    Raises:
        LoadInventoryError: If the file is malformed.
        InventoryFileError: If the file cannot be read or contains invalid
            structure.
        ReservedFeatureError: If the file defines reserved feature names.
    """  # noqa: E501
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
        raise InventoryFileError(f"'{path}' has no segment columns.")

    header = [cell.strip() for cell in rows[0]]
    if header[0] != "":
        raise InventoryFileError(f"'{path}' must have an empty top-left cell.")

    raw_segments = header[1:]
    if any(not seg for seg in raw_segments):
        raise InventoryFileError(
            f"'{path}' contains an empty segment name in the header row."
        )
    if len(set(raw_segments)) != len(raw_segments):
        raise InventoryFileError(
            f"'{path}' contains duplicate segment names in the header row."
        )

    data_rows = rows[1:]
    if not data_rows:
        raise InventoryFileError(f"'{path}' has no feature rows.")

    features: list[str] = []
    seen_features: set[str] = set()
    for row in data_rows:
        feature = row[0].strip() if row else ""
        if not feature:
            raise InventoryFileError(
                f"'{path}' contains a row with no feature name."
            )
        if feature in seen_features:
            raise InventoryFileError(
                f"'{path}' contains duplicate feature name '{feature}'."
            )
        seen_features.add(feature)
        features.append(feature)

    try:
        fs = FeatureSystem(frozenset(features))
    except ReservedFeatureError as e:
        raise LoadInventoryError(
            f"'{path}' contains reserved feature names: {e.conflicts}."
        ) from e

    if strict:
        expected_len = len(raw_segments) + 1
        for row in data_rows:
            if len(row) != expected_len:
                feature = row[0].strip() if row else ""
                raise InventoryFileError(
                    f"Row '{feature}' has {len(row) - 1} values. "
                    f"Expected {len(raw_segments)}."
                )

    segment_specs: dict[str, dict[str, FeatureValue]] = {
        seg: {} for seg in raw_segments
    }

    for row in data_rows:
        feature = row[0].strip()
        values = row[1:]
        for seg_index, seg in enumerate(raw_segments):
            val = values[seg_index].strip() if seg_index < len(values) else ""
            if val in ("", "0"):
                continue
            if val in ("+", "-"):
                segment_specs[seg][feature] = FeatureValue.from_str(val)
                continue
            raise InventoryFileError(
                f"Invalid value '{val}' for feature '{feature}' and segment "
                f"'{seg}' in '{path}'."
            )

    inventory = fs.inventory(
        {seg: fs.segment(spec) for seg, spec in segment_specs.items()}
    )
    return fs, inventory
