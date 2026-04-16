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


def test_matches_at(fs: lp.FeatureSystem) -> None:
    ncs1 = fs.natural_class_sequence([fs.natural_class({"F1": lp.POS})])
    ncs2 = fs.natural_class_sequence(
        [
            fs.natural_class({"F1": lp.POS}),
            fs.natural_class({"F1": lp.NEG}),
        ]
    )
    w = fs.word(
        [
            fs.segment({"F1": lp.POS}),
            fs.segment({"F1": lp.NEG}),
            fs.segment({"F1": lp.POS}),
        ]
    )
    assert ncs1.matches_at(w, 0)
    assert not ncs1.matches_at(w, 1)
    assert ncs1.matches_at(w, 2)
    assert ncs2.matches_at(w, 0)
    assert not ncs2.matches_at(w, 1)


def test_find_all(fs: lp.FeatureSystem) -> None:
    ncs1 = fs.natural_class_sequence([fs.natural_class({"F1": lp.POS})])
    ncs2 = fs.natural_class_sequence(
        [
            fs.natural_class({"F1": lp.POS}),
            fs.natural_class({"F1": lp.NEG}),
        ]
    )
    w = fs.word(
        [
            fs.segment({"F1": lp.POS}),
            fs.segment({"F1": lp.NEG}),
            fs.segment({"F1": lp.POS}),
        ]
    )
    assert ncs1.find_all(w) == [0, 2]
    assert ncs2.find_all(w) == [0]


def test_matches_at_with_boundaries(fs: lp.FeatureSystem) -> None:
    ncs = fs.natural_class_sequence(
        [fs.natural_class({"BOS": lp.POS}), fs.natural_class({"F1": lp.POS})]
    )
    w = fs.add_boundaries(
        fs.word([fs.segment({"F1": lp.POS}), fs.segment({"F1": lp.NEG})])
    )
    assert ncs.matches_at(w, 0)
    assert not ncs.matches_at(w, 1)


def test_find_all_with_boundaries(fs: lp.FeatureSystem) -> None:
    ncs1 = fs.natural_class_sequence([fs.natural_class({"EOS": lp.POS})])
    ncs2 = fs.natural_class_sequence(
        [fs.natural_class({"F1": lp.NEG}), fs.natural_class({"EOS": lp.POS})]
    )
    w = fs.add_boundaries(
        fs.word(
            [
                fs.segment({"F1": lp.POS}),
                fs.segment({"F1": lp.NEG}),
            ]
        )
    )
    assert ncs1.find_all(w) == [3]
    assert ncs2.find_all(w) == [2]


def test_find_first(fs: lp.FeatureSystem) -> None:
    ncs = fs.natural_class_sequence([fs.natural_class({"F1": lp.POS})])
    w = fs.word(
        [
            fs.segment({"F1": lp.NEG}),
            fs.segment({"F1": lp.POS}),
            fs.segment({"F1": lp.NEG}),
            fs.segment({"F1": lp.POS}),
        ]
    )
    assert ncs.find_first(w) == 1  # finds first match from start
    assert ncs.find_first(w, from_pos=2) == 3  # finds next match after pos 2
    assert ncs.find_first(w, from_pos=4) is None  # past end, no match
    assert ncs.find_first(w, from_pos=0) == 1  # from_pos=0 same as default


def test_find_last(fs: lp.FeatureSystem) -> None:
    ncs = fs.natural_class_sequence([fs.natural_class({"F1": lp.POS})])
    w = fs.word(
        [
            fs.segment({"F1": lp.NEG}),
            fs.segment({"F1": lp.POS}),
            fs.segment({"F1": lp.NEG}),
            fs.segment({"F1": lp.POS}),
        ]
    )
    assert ncs.find_last(w) == 3  # finds last match in word
    assert ncs.find_last(w, before_pos=3) == 1  # finds last match before pos 3
    assert ncs.find_last(w, before_pos=1) is None  # nothing before pos 1
    assert ncs.find_last(w, before_pos=4) == 3  # before_pos past last match


def test_find_first_no_match(fs: lp.FeatureSystem) -> None:
    ncs = fs.natural_class_sequence([fs.natural_class({"F1": lp.POS})])
    w = fs.word([fs.segment({"F1": lp.NEG}), fs.segment({"F1": lp.NEG})])
    assert ncs.find_first(w) is None
    assert ncs.find_last(w) is None


def test_find_first_longer_than_word(fs: lp.FeatureSystem) -> None:
    ncs = fs.natural_class_sequence(
        [fs.natural_class({"F1": lp.POS}), fs.natural_class({"F1": lp.POS})]
    )
    w = fs.word([fs.segment({"F1": lp.POS})])
    assert ncs.find_first(w) is None
    assert ncs.find_last(w) is None


def test_natural_class_sequence_str_single_matches_natural_class(
    fs: lp.FeatureSystem,
) -> None:
    nc = fs.natural_class({"F1": lp.POS, "F2": lp.NEG})
    ncs = fs.natural_class_sequence([nc])
    assert str(ncs) == str(nc)


def test_natural_class_sequence_str_with_union(
    fs: lp.FeatureSystem,
) -> None:
    nc1 = fs.natural_class({"F1": lp.POS})
    nc2 = fs.natural_class({"F2": lp.NEG})
    union = nc1 | nc2
    ncs = fs.natural_class_sequence([union, nc1])
    assert str(ncs) == "[{+F1}|{-F2} {+F1}]"
