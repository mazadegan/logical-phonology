import pytest

from logical_phonology import (
    FeatureValue,
    NaturalClassFactory,
    SegmentFactory,
    UnknownFeatureError,
)


@pytest.fixture
def valid_features() -> frozenset[str]:
    return frozenset(["F1", "F2", "F3"])


@pytest.fixture
def natural_class_factory(
    valid_features: frozenset[str],
) -> NaturalClassFactory:
    return NaturalClassFactory(valid_features)


@pytest.fixture
def segment_factory(valid_features: frozenset[str]) -> SegmentFactory:
    return SegmentFactory(valid_features)


def test_natural_class_unknown_feature(
    natural_class_factory: NaturalClassFactory,
) -> None:
    with pytest.raises(UnknownFeatureError) as exc_info:
        natural_class_factory.create({"F4": FeatureValue.POS})
    assert "F4" in exc_info.value.unknown


@pytest.mark.parametrize(
    "feature_spec, expected",
    [
        ({f: FeatureValue.POS for f in ["F1", "F2", "F3"]}, 1),
        ({f: FeatureValue.POS for f in ["F1", "F2"]}, 3),
        ({f: FeatureValue.POS for f in ["F1"]}, 9),
        ({}, 27),
    ],
)
def test_natural_class_size(
    feature_spec: dict[str, FeatureValue],
    expected: int,
    natural_class_factory: NaturalClassFactory,
) -> None:
    nc = natural_class_factory.create(feature_spec)
    assert nc.size == expected


def test_equality(natural_class_factory: NaturalClassFactory) -> None:
    nc1 = natural_class_factory.create({"F1": FeatureValue.POS})
    nc2 = natural_class_factory.create({"F1": FeatureValue.POS})
    nc3 = natural_class_factory.create({"F1": FeatureValue.NEG})
    nc4 = natural_class_factory.create({"F2": FeatureValue.POS})
    assert nc1 == nc2
    assert nc1 != nc3
    assert nc1 != nc4


def test_equal_hash(natural_class_factory: NaturalClassFactory) -> None:
    nc1 = natural_class_factory.create({"F1": FeatureValue.POS})
    nc2 = natural_class_factory.create({"F1": FeatureValue.POS})
    assert hash(nc1) == hash(nc2)


def test_contains(
    natural_class_factory: NaturalClassFactory, segment_factory: SegmentFactory
) -> None:
    nc1 = natural_class_factory.create({})
    assert nc1.contains(segment_factory.create({}))
    nc2 = natural_class_factory.create({"F1": FeatureValue.POS})
    assert not nc2.contains(segment_factory.create({}))
    assert nc2.contains(segment_factory.create({"F1": FeatureValue.POS}))
    assert nc2.contains(
        segment_factory.create(
            {"F1": FeatureValue.POS, "F2": FeatureValue.POS}
        )
    )
    assert nc2.contains(
        segment_factory.create(
            {"F1": FeatureValue.POS, "F2": FeatureValue.NEG}
        )
    )
    nc3 = natural_class_factory.create(
        {"F1": FeatureValue.POS, "F2": FeatureValue.NEG}
    )
    assert not nc3.contains(
        segment_factory.create(
            {
                "F1": FeatureValue.POS,
                "F2": FeatureValue.POS,
            }
        )
    )
