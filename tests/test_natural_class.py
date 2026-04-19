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


def test_natural_class_from_segment(fs: lp.FeatureSystem) -> None:
    seg = fs.segment({"F1": lp.POS, "F2": lp.NEG})
    assert fs.natural_class_from_segment(seg) == fs.natural_class(
        {"F1": lp.POS, "F2": lp.NEG}
    )


def test_natural_class_from_boundary_segment(fs: lp.FeatureSystem) -> None:
    assert fs.natural_class_from_segment(fs.BOS) == fs.BOS_NC


def test_natural_class_from_string_feature_values(
    fs: lp.FeatureSystem,
) -> None:
    assert fs.natural_class({"F1": "+", "F2": "-"}) == fs.natural_class(
        {"F1": lp.POS, "F2": lp.NEG}
    )


def test_natural_class_from_mixed_feature_values(
    fs: lp.FeatureSystem,
) -> None:
    assert fs.natural_class({"F1": "+", "F2": lp.NEG}) == fs.natural_class(
        {"F1": lp.POS, "F2": lp.NEG}
    )


def test_natural_class_invalid_string_feature_value_raises(
    fs: lp.FeatureSystem,
) -> None:
    with pytest.raises(lp.InvalidFeatureValueError):
        fs.natural_class({"F1": "x"})  # type: ignore[dict-item]


def test_natural_class_spec_immutable(fs: lp.FeatureSystem) -> None:
    nc = fs.natural_class({"F1": lp.POS})
    with pytest.raises(TypeError):
        # mypy knows Mapping is immutable
        nc.feature_specification["F1"] = lp.NEG  # type: ignore


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


def test_natural_class_str(fs: lp.FeatureSystem) -> None:
    nc = fs.natural_class({"F2": lp.NEG, "F1": lp.POS})
    assert str(nc) == "[{+F1,-F2}]"


def test_natural_class_str_empty(fs: lp.FeatureSystem) -> None:
    assert str(fs.natural_class({})) == "[{}]"


def test_natural_class_str_sorts_by_feature_name() -> None:
    fs = lp.FeatureSystem.from_features(["Front", "High", "Round"])
    nc = fs.natural_class({"High": lp.POS, "Front": lp.NEG, "Round": lp.NEG})
    assert str(nc) == "[{-Front,+High,-Round}]"


def test_natural_class_extension(fs: lp.FeatureSystem) -> None:
    inv = fs.inventory(
        {
            "A": fs.segment({"F1": lp.POS}),
            "B": fs.segment({"F1": lp.NEG}),
        }
    )
    nc = fs.natural_class({"F1": lp.POS})
    assert nc.extension(inv) == (inv["A"],)
    assert nc.extension(inv, as_names=True) == ("A",)


def test_natural_class_subintensions_default(fs: lp.FeatureSystem) -> None:
    nc = fs.natural_class({"F1": lp.POS, "F2": lp.NEG, "F3": lp.POS})
    subs = list(nc.subintensions())
    assert len(subs) == 6  # 2^3 - universal - self
    assert fs.natural_class({}) not in subs
    assert nc not in subs


def test_natural_class_subintensions_inclusion_flags(
    fs: lp.FeatureSystem,
) -> None:
    nc = fs.natural_class({"F1": lp.POS, "F2": lp.NEG, "F3": lp.POS})
    assert len(list(nc.subintensions(include_universal=True))) == 7
    assert len(list(nc.subintensions(include_self=True))) == 7
    assert (
        len(
            list(
                nc.subintensions(
                    include_universal=True, include_self=True
                )
            )
        )
        == 8
    )


def test_natural_class_subintensions_max_features_guard(
    fs: lp.FeatureSystem,
) -> None:
    nc = fs.natural_class({"F1": lp.POS, "F2": lp.NEG})
    with pytest.raises(lp.CombinatoricExplosionError):
        list(nc.subintensions(max_features=1))
