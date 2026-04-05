from pathlib import Path

import pytest

from logical_phonology import (
    DuplicateFeaturesError,
    InvalidElementTypeError,
    InvalidTypeError,
    MissingKeyError,
    load_feature_system,
)


def test_load_feature_system_valid(tmp_path: Path) -> None:
    config = tmp_path / "features.toml"
    config.write_text('features = ["F1", "F2", "F3"]')
    result = load_feature_system(str(config))
    assert result == frozenset(["F1", "F2", "F3"])


def test_missing_features_key(tmp_path: Path) -> None:
    config = tmp_path / "features.toml"
    config.write_text('other_key = ["F1", "F2", "F3"]')
    with pytest.raises(MissingKeyError) as exc_info:
        load_feature_system(str(config))
    assert exc_info.value.key == "features"


def test_features_not_a_list(tmp_path: Path) -> None:
    config = tmp_path / "features.toml"
    config.write_text('features = "F1"')
    with pytest.raises(InvalidTypeError) as exc_info:
        load_feature_system(str(config))
    assert exc_info.value.expected is list


def test_features_contain_non_strings(tmp_path: Path) -> None:
    config = tmp_path / "features.toml"
    config.write_text('features = ["F1", 1, 3.14]')
    with pytest.raises(InvalidElementTypeError) as exc_info:
        load_feature_system(str(config))
    assert exc_info.value.expected is str
    assert 1 in exc_info.value.invalid
    assert 3.14 in exc_info.value.invalid


def test_duplicate_features(tmp_path: Path) -> None:
    config = tmp_path / "features.toml"
    config.write_text('features = ["F1", "F2", "F2"]')
    with pytest.raises(DuplicateFeaturesError) as exc_info:
        load_feature_system(str(config))
    assert "F2" in exc_info.value.duplicates
