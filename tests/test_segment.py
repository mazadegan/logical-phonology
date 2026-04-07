import pytest
from hypothesis import given
from hypothesis import strategies as st

import logical_phonology as lp

feature_value_strategy = st.sampled_from([lp.POS, lp.NEG])
feature_spec_strategy = st.dictionaries(
    keys=st.sampled_from(["F1", "F2", "F3"]),
    values=feature_value_strategy,
)


@pytest.fixture
def fs() -> lp.FeatureSystem:
    valid_features = frozenset(["F1", "F2", "F3"])
    return lp.FeatureSystem(valid_features)


def test_fail_on_reserved_features() -> None:
    with pytest.raises(lp.ReservedFeatureError) as exc_info:
        lp.FeatureSystem(frozenset(["EOS"]))
    assert "EOS" in exc_info.value.conflicts


@pytest.mark.parametrize("s,expected", [("+", lp.POS), ("-", lp.NEG)])
def test_valid_feature_value(s: str, expected: lp.FeatureValue) -> None:
    assert lp.FeatureValue.from_str(s) == expected


@pytest.mark.parametrize("fv,expected", [(lp.POS, "+"), (lp.NEG, "-")])
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
    assert "F1" not in segment
    assert "F2" not in segment
    assert "F3" not in segment


@given(feature_spec_strategy)
def test_segments_always_hashable(
    feature_spec: dict[str, lp.FeatureValue],
) -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2", "F3"]))
    seg = fs.segment(feature_spec)
    assert seg in {seg}


def test_segment_equality(fs: lp.FeatureSystem) -> None:
    s1 = fs.segment({})
    s2 = fs.segment({})
    s3 = fs.segment({"F1": lp.POS})
    assert s1 == s2
    assert s1 != s3


@given(feature_spec_strategy)
def test_equal_segments_have_equal_hashes(
    feature_spec: dict[str, lp.FeatureValue],
) -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2", "F3"]))
    s1 = fs.segment(feature_spec)
    s2 = fs.segment(feature_spec)
    assert hash(s1) == hash(s2)


def test_segment_unknown_feature(fs: lp.FeatureSystem) -> None:
    with pytest.raises(lp.UnknownFeatureError) as exc_info:
        fs.segment({"Z": lp.POS})
    assert "Z" in exc_info.value.unknown


def test_reserved_segments(fs: lp.FeatureSystem) -> None:
    assert isinstance(fs.BOS, lp.Segment)
    assert isinstance(fs.EOS, lp.Segment)
    assert "BOS" in fs.BOS
    assert "EOS" in fs.EOS
    assert fs.BOS != fs.EOS
    assert fs.BOS != fs.segment({})


def test_subtract(fs: lp.FeatureSystem) -> None:
    s1 = fs.segment({"F1": lp.POS, "F2": lp.NEG})
    s2 = fs.segment({"F1": lp.POS})
    result = s1 - s2
    assert "F1" not in result
    assert "F2" in result
    assert result["F2"] == lp.NEG


def test_project(fs: lp.FeatureSystem) -> None:
    s = fs.segment({"F1": lp.POS, "F2": lp.NEG, "F3": lp.POS})
    result = s & frozenset(["F1", "F2"])
    assert "F1" in result
    assert "F2" in result
    assert "F3" not in result


def test_unify(fs: lp.FeatureSystem) -> None:
    s1 = fs.segment({"F1": lp.POS})
    s2 = fs.segment({"F2": lp.NEG})
    result = s1 | s2
    assert result["F1"] == lp.POS
    assert result["F2"] == lp.NEG


def test_unify_conflict(fs: lp.FeatureSystem) -> None:
    s1 = fs.segment({"F1": lp.POS})
    s2 = fs.segment({"F1": lp.NEG})
    result = s1 | s2
    assert result["F1"] == lp.POS  # conflict — feature value stays the same


def test_unify_strict(fs: lp.FeatureSystem) -> None:
    s1 = fs.segment({"F1": lp.POS})
    s2 = fs.segment({"F1": lp.NEG})
    with pytest.raises(lp.UnificationError) as exc_info:
        s1.unify_strict(s2)
    assert exc_info.value.feature == "F1"


@given(feature_spec_strategy, feature_spec_strategy)
def test_subtract_is_subset(
    spec1: dict[str, lp.FeatureValue],
    spec2: dict[str, lp.FeatureValue],
) -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2", "F3"]))
    s1 = fs.segment(spec1)
    s2 = fs.segment(spec2)
    result = s1 - s2
    assert all(f in s1 for f in result.features)
    assert all(f not in s2 for f in result.features)


@given(feature_spec_strategy, feature_spec_strategy)
def test_project_is_subset(
    spec1: dict[str, lp.FeatureValue],
    spec2: dict[str, lp.FeatureValue],
) -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2", "F3"]))
    s = fs.segment(spec1)
    restricted = frozenset(spec2.keys())
    result = s & restricted
    assert all(f in s for f in result.features)
    assert all(f in restricted for f in result.features)


@given(feature_spec_strategy, feature_spec_strategy)
def test_unify_contains_non_conflicting(
    spec1: dict[str, lp.FeatureValue],
    spec2: dict[str, lp.FeatureValue],
) -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2", "F3"]))
    s1 = fs.segment(spec1)
    s2 = fs.segment(spec2)
    result = s1 | s2
    # all features from s1 should be in result
    assert all(f in result for f in s1.features)
    # non-conflicting features from s2 should be in result
    for f, v in s2.features.items():
        if f not in s1.features:
            assert result[f] == v
