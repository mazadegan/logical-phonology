import pytest

import logical_phonology as lp


@pytest.fixture
def fs() -> lp.FeatureSystem:
    valid_features = frozenset(["F1", "F2", "F3"])
    return lp.FeatureSystem(valid_features)


def test_natural_class_unknown_feature(fs: lp.FeatureSystem) -> None:
    with pytest.raises(lp.UnknownFeatureError) as exc_info:
        fs.natural_class({"F4": lp.POS})
    assert "F4" in exc_info.value.unknown


@pytest.mark.parametrize(
    "feature_spec, expected",
    [
        ({f: lp.POS for f in ["F1", "F2", "F3"]}, 1),
        ({f: lp.POS for f in ["F1", "F2"]}, 3),
        ({f: lp.POS for f in ["F1"]}, 9),
        ({}, 27),
    ],
)
def test_natural_class_size(
    feature_spec: dict[str, lp.FeatureValue],
    expected: int,
    fs: lp.FeatureSystem,
) -> None:
    nc = fs.natural_class(feature_spec)
    assert nc.size == expected


def test_equality(fs: lp.FeatureSystem) -> None:
    nc1 = fs.natural_class({"F1": lp.POS})
    nc2 = fs.natural_class({"F1": lp.POS})
    nc3 = fs.natural_class({"F1": lp.NEG})
    nc4 = fs.natural_class({"F2": lp.POS})
    assert nc1 == nc2
    assert nc1 != nc3
    assert nc1 != nc4


def test_equal_hash(fs: lp.FeatureSystem) -> None:
    nc1 = fs.natural_class({"F1": lp.POS})
    nc2 = fs.natural_class({"F1": lp.POS})
    assert hash(nc1) == hash(nc2)


def test_contains(fs: lp.FeatureSystem) -> None:
    nc1 = fs.natural_class({})
    assert fs.segment({}) in nc1
    nc2 = fs.natural_class({"F1": lp.POS})
    assert fs.segment({}) not in nc2
    assert fs.segment({"F1": lp.POS}) in nc2
    assert fs.segment({"F1": lp.POS, "F2": lp.POS}) in nc2
    assert fs.segment({"F1": lp.POS, "F2": lp.NEG}) in nc2
    nc3 = fs.natural_class({"F1": lp.POS, "F2": lp.NEG})
    assert fs.segment({"F1": lp.POS, "F2": lp.POS}) not in nc3
