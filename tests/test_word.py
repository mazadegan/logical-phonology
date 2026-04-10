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
