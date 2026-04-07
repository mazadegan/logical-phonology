from itertools import product

import pytest
from hypothesis import given
from hypothesis import strategies as st

import logical_phonology as lp

feature_value_strategy = st.sampled_from([lp.POS, lp.NEG])
feature_spec_strategy = st.dictionaries(
    keys=st.sampled_from(["F1", "F2"]),
    values=feature_value_strategy,
)


@pytest.fixture
def inv() -> lp.Inventory:
    valid_features = frozenset(["F1", "F2"])
    fs = lp.FeatureSystem(valid_features)
    names = ["A", "B", "C", "D"]
    values = list(product([lp.POS, lp.NEG], repeat=2))
    segments = {
        name: fs.segment({"F1": f1, "F2": f2})
        for name, (f1, f2) in zip(names, values)
    }
    return fs.inventory(segments)


def test_alias_error() -> None:
    valid_features = frozenset(["F1", "F2"])
    fs = lp.FeatureSystem(valid_features)
    seg = fs.segment({"F1": lp.POS, "F2": lp.NEG})
    with pytest.raises(lp.AliasError) as exc_info:
        fs.inventory({"A": seg, "B": seg}, allow_aliases=False)
    assert "A" in str(exc_info.value) or "B" in str(exc_info.value)


@given(feature_spec_strategy)
def test_segment_membership(feature_spec: dict[str, lp.FeatureValue]) -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2"]))
    seg = fs.segment(feature_spec)
    inv = fs.inventory({"A": seg})
    assert seg in inv  # check segment_to_name
    assert "A" in inv  # check name_to_segment


@given(feature_spec_strategy)
def test_name_of_roundtrip(feature_spec: dict[str, lp.FeatureValue]) -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2"]))
    seg = fs.segment(feature_spec)
    inv = fs.inventory({"A": seg})
    assert inv[inv.name_of(seg)] == seg


def test_aliased_segment_name_of() -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2"]))
    seg = fs.segment({"F1": lp.POS, "F2": lp.NEG})
    inv = fs.inventory({"A": seg, "B": seg})
    # name_of returns canonical form for aliased segments
    assert inv.name_of(seg) == str(seg)
    # canonical form can be looked up
    assert inv[inv.name_of(seg)] == seg
