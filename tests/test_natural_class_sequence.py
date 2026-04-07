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


def test_natural_class_sequence_membership(fs: lp.FeatureSystem) -> None:
    ncs = fs.natural_class_sequence(
        [fs.natural_class({"F1": lp.POS}), fs.natural_class({"F1": lp.NEG})]
    )
    w1 = fs.word([])  # length failure (too short)
    w2 = fs.word(
        [fs.segment({}), fs.segment({}), fs.segment({})]
    )  # length failure (too long)
    w3 = fs.word(
        [
            fs.segment({"F1": lp.POS}),
            fs.segment({"F1": lp.POS}),
        ]
    )  # match failure
    w4 = fs.word(
        [
            fs.segment({"F1": lp.POS}),
            fs.segment({"F1": lp.NEG}),
        ]
    )  # match success
    assert w1 not in ncs
    assert w2 not in ncs
    assert w3 not in ncs
    assert w4 in ncs


def test_empty_natural_class_sequence(fs: lp.FeatureSystem) -> None:
    ncs = fs.natural_class_sequence([])
    assert fs.word([]) in ncs


@given(feature_spec_strategy)
def test_empty_natural_class_matches_all(
    feature_spec: dict[str, lp.FeatureValue],
) -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2", "F3"]))
    nc = fs.natural_class({})
    seg = fs.segment(feature_spec)
    assert seg in nc
