from pathlib import Path

import pytest

import logical_phonology as lp


def write_file(tmp_path: Path, name: str, content: str) -> Path:
    path = tmp_path / name
    path.write_text(content)
    return path


def test_load_inventory_from_csv(tmp_path: Path) -> None:
    path = write_file(
        tmp_path,
        "inventory.csv",
        ",A,B\nF1,+,-\nF2,0,+\n",
    )
    fs, inv = lp.load_inventory_from_file(path)

    assert fs.valid_features == frozenset(["F1", "F2"])
    assert inv["A"] == fs.segment({"F1": lp.POS})
    assert inv["B"] == fs.segment({"F1": lp.NEG, "F2": lp.POS})


def test_load_inventory_from_tsv(tmp_path: Path) -> None:
    path = write_file(
        tmp_path,
        "inventory.tsv",
        "\tA\tB\nF1\t+\t-\nF2\t0\t+\n",
    )
    fs, inv = lp.load_inventory_from_file(path, delimiter="\t")

    assert fs.valid_features == frozenset(["F1", "F2"])
    assert inv["A"] == fs.segment({"F1": lp.POS})
    assert inv["B"] == fs.segment({"F1": lp.NEG, "F2": lp.POS})


def test_load_inventory_strict_rejects_ragged_rows(tmp_path: Path) -> None:
    path = write_file(
        tmp_path,
        "ragged.csv",
        ",A,B\nF1,+,-\nF2,+\n",
    )
    with pytest.raises(lp.InventoryFileError):
        lp.load_inventory_from_file(path, strict=True)


def test_load_inventory_rejects_reserved_features(tmp_path: Path) -> None:
    path = write_file(
        tmp_path,
        "reserved.csv",
        ",A,B\nBOS,+,-\nF1,+,-\n",
    )
    with pytest.raises(lp.LoadInventoryError):
        lp.load_inventory_from_file(path)


def test_load_inventory_rejects_invalid_values(tmp_path: Path) -> None:
    path = write_file(
        tmp_path,
        "invalid.csv",
        ",A\nF1,x\n",
    )
    with pytest.raises(lp.InventoryFileError):
        lp.load_inventory_from_file(path)
