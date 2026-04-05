import pytest

from logical_phonology import (
    FeatureValue,
    InvalidFeatureValueError,
    InvalidSegmentNameError,
    SegmentFactory,
    UnknownFeatureError,
)


@pytest.fixture
def valid_features() -> frozenset[str]:
    return frozenset(["F1", "F2", "F3"])


@pytest.fixture
def segment_factory(valid_features: frozenset[str]) -> SegmentFactory:
    return SegmentFactory(valid_features)


@pytest.mark.parametrize(
    "s,expected",
    [
        ("+", FeatureValue.POS),
        ("-", FeatureValue.NEG),
        ("0", FeatureValue.UND),
    ],
)
def test_valid_feature_value(s: str, expected: FeatureValue) -> None:
    assert FeatureValue.from_str(s) == expected


@pytest.mark.parametrize(
    "fv,expected",
    [
        (FeatureValue.POS, "+"),
        (FeatureValue.NEG, "-"),
        (FeatureValue.UND, "0"),
    ],
)
def test_valid_feature_value_string(fv: FeatureValue, expected: str) -> None:
    assert str(fv) == expected


def test_invalid_feature_value() -> None:
    with pytest.raises(InvalidFeatureValueError) as exc_info:
        FeatureValue.from_str("x")
    assert exc_info.value.value == "x"


def test_fully_underspecified_segment(segment_factory: SegmentFactory) -> None:
    segment = segment_factory.create("x", {})
    assert segment.features["F1"] is FeatureValue.UND
    assert segment.features["F2"] is FeatureValue.UND
    assert segment.features["F3"] is FeatureValue.UND


def test_segments_hashable(segment_factory: SegmentFactory) -> None:
    segment = segment_factory.create("x", {})
    assert segment in {segment}


def test_segment_equality(segment_factory: SegmentFactory) -> None:
    s1 = segment_factory.create("x", {})
    s2 = segment_factory.create("x", {})
    s3 = segment_factory.create("y", {})
    s4 = segment_factory.create(
        "x",
        {
            "F1": FeatureValue.POS,
        },
    )
    assert s1 == s2
    assert s1 != s3
    assert s1 != s4


def test_equal_segments_same_hash(segment_factory: SegmentFactory) -> None:
    s1 = segment_factory.create("x", {})
    s2 = segment_factory.create("x", {})
    assert hash(s1) == hash(s2)


def test_empty_string_invalid_segment_name(
    segment_factory: SegmentFactory,
) -> None:
    with pytest.raises(InvalidSegmentNameError) as exc_info:
        segment_factory.create("", {})
    assert exc_info.value.value == ""


def test_segment_unknown_feature(segment_factory: SegmentFactory) -> None:
    with pytest.raises(UnknownFeatureError) as exc_info:
        segment_factory.create("x", {"Z": FeatureValue.POS})
    assert "Z" in exc_info.value.unknown


def test_explicit_underspecification(segment_factory: SegmentFactory) -> None:
    segment = segment_factory.create("x", {"F1": FeatureValue.POS})
    assert segment.features["F1"] is FeatureValue.POS
    assert segment.features["F2"] is FeatureValue.UND
    assert segment.features["F3"] is FeatureValue.UND
