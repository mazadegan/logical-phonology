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
        "ipa,F1,F2\nA,+,0\nB,-,+\n",
    )
    fs, inv = lp.load_inventory_from_file(path)

    assert fs.valid_features == frozenset(["F1", "F2"])
    assert inv["A"] == fs.segment({"F1": lp.POS})
    assert inv["B"] == fs.segment({"F1": lp.NEG, "F2": lp.POS})


def test_load_inventory_from_tsv(tmp_path: Path) -> None:
    path = write_file(
        tmp_path,
        "inventory.tsv",
        "ipa\tF1\tF2\nA\t+\t0\nB\t-\t+\n",
    )
    fs, inv = lp.load_inventory_from_file(path, delimiter="\t")

    assert fs.valid_features == frozenset(["F1", "F2"])
    assert inv["A"] == fs.segment({"F1": lp.POS})
    assert inv["B"] == fs.segment({"F1": lp.NEG, "F2": lp.POS})


def test_load_inventory_first_column_label_ignored(tmp_path: Path) -> None:
    path = write_file(
        tmp_path,
        "inventory.csv",
        "symbol,F1\nA,+\n",
    )
    fs, inv = lp.load_inventory_from_file(path)
    assert inv["A"] == fs.segment({"F1": lp.POS})


def test_load_inventory_strict_rejects_ragged_rows(tmp_path: Path) -> None:
    path = write_file(
        tmp_path,
        "ragged.csv",
        "ipa,F1,F2\nA,+\n",
    )
    with pytest.raises(lp.InventoryFileError):
        lp.load_inventory_from_file(path, strict=True)


def test_load_inventory_rejects_reserved_features(tmp_path: Path) -> None:
    path = write_file(
        tmp_path,
        "reserved.csv",
        "ipa,BOS,F1\nA,+,+\n",
    )
    with pytest.raises(lp.LoadInventoryError):
        lp.load_inventory_from_file(path)


def test_load_inventory_rejects_invalid_values(tmp_path: Path) -> None:
    path = write_file(
        tmp_path,
        "invalid.csv",
        "ipa,F1\nA,x\n",
    )
    with pytest.raises(lp.InventoryFileError):
        lp.load_inventory_from_file(path)


def test_save_roundtrip(tmp_path: Path) -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2"]))
    inv = fs.inventory({
        "A": fs.segment({"F1": lp.POS}),
        "B": fs.segment({"F1": lp.NEG, "F2": lp.POS}),
    })
    path = tmp_path / "out.csv"
    inv.save(path)
    fs2, inv2 = lp.load_inventory_from_file(path)
    assert fs2.valid_features == fs.valid_features
    assert inv2["A"] == inv["A"]
    assert inv2["B"] == inv["B"]


def test_save_writes_ipa_header(tmp_path: Path) -> None:
    fs = lp.FeatureSystem(frozenset(["F1"]))
    inv = fs.inventory({"A": fs.segment({"F1": lp.POS})})
    path = tmp_path / "out.csv"
    inv.save(path)
    first_line = path.read_text().splitlines()[0]
    assert first_line.startswith("ipa,")


def test_save_tsv(tmp_path: Path) -> None:
    fs = lp.FeatureSystem(frozenset(["F1"]))
    inv = fs.inventory({"A": fs.segment({"F1": lp.POS})})
    path = tmp_path / "out.tsv"
    inv.save(path, delimiter="\t")
    fs2, inv2 = lp.load_inventory_from_file(path, delimiter="\t")
    assert inv2["A"] == inv["A"]
