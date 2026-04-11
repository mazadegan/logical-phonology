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
