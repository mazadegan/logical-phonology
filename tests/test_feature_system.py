import pytest

import logical_phonology as lp

_FS = lp.FeatureSystem(frozenset(["F", "G"]))


# enumerate_classes

def test_enumerate_classes_count() -> None:
    classes = list(_FS.enumerate_classes(["F", "G"]))
    assert len(classes) == 8  # 3^2 - 1 (empty excluded by default)


def test_enumerate_classes_include_empty() -> None:
    classes = list(_FS.enumerate_classes(["F", "G"], include_empty=True))
    assert len(classes) == 9
    assert _FS.natural_class({}) in classes


def test_enumerate_classes_excludes_empty_by_default() -> None:
    classes = list(_FS.enumerate_classes(["F", "G"]))
    assert _FS.natural_class({}) not in classes


def test_enumerate_classes_dedupes_and_sorts() -> None:
    classes1 = list(_FS.enumerate_classes(["G", "F", "F"]))
    classes2 = list(_FS.enumerate_classes(["F", "G"]))
    assert classes1 == classes2


def test_enumerate_classes_rejects_unknown_feature() -> None:
    with pytest.raises(lp.UnknownFeatureError):
        list(_FS.enumerate_classes(["F", "Z"]))


def test_enumerate_classes_max_features_guard() -> None:
    with pytest.raises(ValueError):
        list(_FS.enumerate_classes(["F", "G"], max_features=1))


def test_enumerate_classes_defaults_to_all_features() -> None:
    classes = list(_FS.enumerate_classes())
    assert len(classes) == 8  # same as passing ["F", "G"] explicitly
