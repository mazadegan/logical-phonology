import pytest

import logical_phonology as lp


@pytest.fixture
def fs() -> lp.FeatureSystem:
    valid_features = frozenset(["F1", "F2", "F3"])
    return lp.FeatureSystem(valid_features)


_CORRECT_LENGTH_PARAMETERS: list[
    tuple[list[dict[str, lp.FeatureValue]], int]
] = [
    ([], 0),
    ([{}], 1),
    ([{}, {}], 2),
    ([{}, {}, {}], 3),
]


@pytest.mark.parametrize("segments,expected_len", _CORRECT_LENGTH_PARAMETERS)
def test_correct_length(
    segments: list[dict[str, lp.FeatureValue]],
    expected_len: int,
    fs: lp.FeatureSystem,
) -> None:
    word = fs.word([fs.segment(s) for s in segments])
    assert len(word) == expected_len
    assert len(fs.add_boundaries(word)) == expected_len + 2


def test_correct_boundary_segments(fs: lp.FeatureSystem) -> None:
    word = fs.word([fs.segment({})])
    word_with_boundaries = fs.add_boundaries(word)
    assert word_with_boundaries[0] == fs.BOS
    assert word_with_boundaries[-1] == fs.EOS


def test_remove_boundaries(fs: lp.FeatureSystem) -> None:
    seg = fs.segment({"F1": lp.POS})
    word = fs.word([seg])
    bracketed = fs.add_boundaries(word)
    assert fs.remove_boundaries(bracketed) == word


def test_remove_boundaries_idempotent(fs: lp.FeatureSystem) -> None:
    seg = fs.segment({"F1": lp.POS})
    word = fs.word([seg])
    assert fs.remove_boundaries(word) == word


def test_remove_boundaries_empty(fs: lp.FeatureSystem) -> None:
    empty = fs.word([])
    assert fs.remove_boundaries(empty) == empty


def test_remove_boundaries_only_bos(fs: lp.FeatureSystem) -> None:
    word = fs.word([fs.BOS])
    assert fs.remove_boundaries(word) == fs.word([])


def test_remove_boundaries_only_eos(fs: lp.FeatureSystem) -> None:
    word = fs.word([fs.EOS])
    assert fs.remove_boundaries(word) == fs.word([])


def test_add_boundaries_idempotent(fs: lp.FeatureSystem) -> None:
    seg = fs.segment({"F1": lp.POS})
    word = fs.word([seg])
    bracketed = fs.add_boundaries(word)
    assert fs.add_boundaries(bracketed) == bracketed


@pytest.fixture
def seg1(fs: lp.FeatureSystem) -> lp.Segment:
    return fs.segment({"F1": lp.POS})


@pytest.fixture
def seg2(fs: lp.FeatureSystem) -> lp.Segment:
    return fs.segment({"F2": lp.NEG})


@pytest.fixture
def seg3(fs: lp.FeatureSystem) -> lp.Segment:
    return fs.segment({"F1": lp.POS, "F2": lp.NEG})


def test_word_add_word(
    fs: lp.FeatureSystem, seg1: lp.Segment, seg2: lp.Segment, seg3: lp.Segment
) -> None:
    w1 = fs.word([seg1, seg2])
    w2 = fs.word([seg3])
    assert w1 + w2 == fs.word([seg1, seg2, seg3])


def test_word_add_segment(
    fs: lp.FeatureSystem, seg1: lp.Segment, seg2: lp.Segment, seg3: lp.Segment
) -> None:
    w = fs.word([seg1, seg2])
    assert w + seg3 == fs.word([seg1, seg2, seg3])


def test_segment_add_segment(
    fs: lp.FeatureSystem, seg1: lp.Segment, seg2: lp.Segment
) -> None:
    assert seg1 + seg2 == fs.word([seg1, seg2])


def test_segment_add_word(
    fs: lp.FeatureSystem, seg1: lp.Segment, seg2: lp.Segment, seg3: lp.Segment
) -> None:
    w = fs.word([seg2, seg3])
    assert seg1 + w == fs.word([seg1, seg2, seg3])


def test_chained_concatenation(
    fs: lp.FeatureSystem, seg1: lp.Segment, seg2: lp.Segment, seg3: lp.Segment
) -> None:
    assert seg1 + fs.word([seg2]) + seg3 + fs.word([seg1]) == fs.word(
        [seg1, seg2, seg3, seg1]
    )


def test_word_str_empty(fs: lp.FeatureSystem) -> None:
    assert str(fs.word([])) == "<>"


def test_word_str(fs: lp.FeatureSystem) -> None:
    w = fs.word(
        [
            fs.segment({"F2": lp.NEG, "F1": lp.POS}),
            fs.segment({"F3": lp.POS}),
        ]
    )
    assert str(w) == "<{+F1,-F2} {+F3}>"


# element-wise operations

_FS2 = lp.FeatureSystem(frozenset(["F", "G"]))
_A = _FS2.segment({"F": lp.POS, "G": lp.POS})
_B = _FS2.segment({"F": lp.POS, "G": lp.NEG})
_C = _FS2.segment({"F": lp.NEG, "G": lp.POS})
_E = _FS2.segment({"F": lp.POS})
_F = _FS2.segment({"F": lp.NEG})
_G = _FS2.segment({"G": lp.POS})
_H = _FS2.segment({"G": lp.NEG})
_I = _FS2.segment({})


def test_word_unify() -> None:
    w1 = _FS2.word([_E, _G])  # +F only, +G only
    w2 = _FS2.word([_F, _H])  # -F only, -G only — conflicts keep left side
    assert w1 | w2 == _FS2.word([_E, _G])


def test_word_unify_length_mismatch() -> None:
    with pytest.raises(ValueError):
        _ = _FS2.word([_A]) | _FS2.word([_A, _B])


def test_word_subtract() -> None:
    w1 = _FS2.word([_A, _B])
    w2 = _FS2.word([_E, _H])
    assert w1 - w2 == _FS2.word([_G, _E])


def test_word_subtract_length_mismatch() -> None:
    with pytest.raises(ValueError):
        _ = _FS2.word([_A]) - _FS2.word([_A, _B])


def test_word_intersect() -> None:
    w1 = _FS2.word([_A, _B])
    w2 = _FS2.word([_B, _C])
    assert w1 & w2 == _FS2.word([_E, _I])


def test_word_intersect_length_mismatch() -> None:
    with pytest.raises(ValueError):
        _ = _FS2.word([_A]) & _FS2.word([_A, _B])


_NC_POS_F = _FS2.natural_class({"F": lp.POS})
_NC_NEG_F = _FS2.natural_class({"F": lp.NEG})
_NC_POS_G = _FS2.natural_class({"G": lp.POS})


def test_word_tier_nc() -> None:
    word = _FS2.word([_A, _B, _C, _I])
    assert word.tier(_NC_POS_F) == _FS2.word([_A, _B])


def test_word_tier_union() -> None:
    word = _FS2.word([_A, _B, _C, _I])
    assert word.tier(_NC_NEG_F | _NC_POS_G) == _FS2.word([_A, _C])


def test_word_ngrams() -> None:
    word = _FS2.word([_A, _B, _C])
    assert word.ngrams(2) == [
        (0, 2, _FS2.word([_A, _B])),
        (1, 3, _FS2.word([_B, _C])),
    ]


def test_word_ngrams_with_boundaries() -> None:
    word = _FS2.add_boundaries(_FS2.word([_A, _B]))
    assert word.ngrams(2) == [
        (0, 2, _FS2.word([_FS2.BOS, _A])),
        (1, 3, _FS2.word([_A, _B])),
        (2, 4, _FS2.word([_B, _FS2.EOS])),
    ]


def test_word_ngrams_rejects_nonpositive_n() -> None:
    with pytest.raises(ValueError):
        _FS2.word([_A, _B]).ngrams(0)
