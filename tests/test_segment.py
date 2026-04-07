import pytest

import logical_phonology as lp


@pytest.fixture
def fs() -> lp.FeatureSystem:
    valid_features = frozenset(["F1", "F2", "F3"])
    return lp.FeatureSystem(valid_features)


@pytest.mark.parametrize(
    "s,expected",
    [
        ("+", lp.POS),
        ("-", lp.NEG),
    ],
)
def test_valid_feature_value(s: str, expected: lp.FeatureValue) -> None:
    assert lp.FeatureValue.from_str(s) == expected


@pytest.mark.parametrize(
    "fv,expected",
    [
        (lp.POS, "+"),
        (lp.NEG, "-"),
    ],
)
def test_valid_feature_value_string(
    fv: lp.FeatureValue, expected: str
) -> None:
    assert str(fv) == expected


def test_invalid_feature_value() -> None:
    with pytest.raises(lp.InvalidFeatureValueError) as exc_info:
        lp.FeatureValue.from_str("x")
    assert exc_info.value.value == "x"


def test_fully_underspecified_segment(fs: lp.FeatureSystem) -> None:
    segment = fs.segment({})
    assert "F1" not in segment.features
    assert "F2" not in segment.features
    assert "F3" not in segment.features


def test_segments_hashable(fs: lp.FeatureSystem) -> None:
    segment = fs.segment({})
    assert segment in {segment}


def test_segment_equality(fs: lp.FeatureSystem) -> None:
    s1 = fs.segment({})
    s2 = fs.segment({})
    s3 = fs.segment({"F1": lp.POS})
    assert s1 == s2
    assert s1 != s3


def test_equal_segments_same_hash(fs: lp.FeatureSystem) -> None:
    s1 = fs.segment({})
    s2 = fs.segment({})
    assert hash(s1) == hash(s2)


def test_segment_unknown_feature(fs: lp.FeatureSystem) -> None:
    with pytest.raises(lp.UnknownFeatureError) as exc_info:
        fs.segment({"Z": lp.POS})
    assert "Z" in exc_info.value.unknown
