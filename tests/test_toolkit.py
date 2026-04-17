import pytest

import logical_phonology as lp

FS = lp.FeatureSystem(frozenset(["F", "G"]))
A = FS.segment({"F": lp.POS, "G": lp.POS})
B = FS.segment({"F": lp.POS, "G": lp.NEG})
C = FS.segment({"F": lp.NEG, "G": lp.POS})
D = FS.segment({"F": lp.NEG, "G": lp.NEG})
E = FS.segment({"F": lp.POS})
F = FS.segment({"F": lp.NEG})
G = FS.segment({"G": lp.POS})
H = FS.segment({"G": lp.NEG})
I = FS.segment({})  # noqa: E741
INV = FS.inventory({"A": A, "B": B, "C": C, "D": D})

NC_POS_F = FS.natural_class({"F": lp.POS})
NC_NEG_F = FS.natural_class({"F": lp.NEG})
NC_POS_G = FS.natural_class({"G": lp.POS})
NC_NEG_G = FS.natural_class({"G": lp.NEG})


def test_tk_unify_segments() -> None:
    tk = FS.toolkit()
    # A has +F, +G. E has only +F. Unifying A with E should give A
    # (left-biased, A already has G)
    assert tk.unify(A, E) == A
    # E has only +F. G has only +G. Unifying E with G should give A (+F, +G)
    assert tk.unify(E, G) == A
    # E has +F. F has -F. Unifying E with F should give E
    # (left-biased, E wins on F)
    assert tk.unify(E, F) == E


def test_tk_unify_words() -> None:
    tk = FS.toolkit()
    w1 = FS.word([E, G])  # +F only, +G only
    w2 = FS.word([F, H])  # -F only, -G only
    assert tk.unify(w1, w2) == FS.word([E, G])


def test_tk_subtract_segments() -> None:
    tk = FS.toolkit()
    assert tk.subtract(A, E) == G
    assert tk.subtract(B, H) == E


def test_tk_subtract_words() -> None:
    tk = FS.toolkit()
    w1 = FS.word([A, B])
    w2 = FS.word([E, H])
    assert tk.subtract(w1, w2) == FS.word([G, E])


def test_tk_union_nc_nc() -> None:
    tk = FS.toolkit()
    union = tk.union(NC_POS_F, NC_NEG_F)
    assert isinstance(union, lp.NaturalClassUnion)
    assert len(union.classes) == 2


def test_tk_union_nc_union() -> None:
    tk = FS.toolkit()
    union = tk.union(NC_POS_F, NC_NEG_F | NC_POS_G)
    assert len(union.classes) == 3


def test_tk_union_union_nc() -> None:
    tk = FS.toolkit()
    union = tk.union(NC_POS_F | NC_NEG_F, NC_POS_G)
    assert len(union.classes) == 3


def test_tk_union_union_union() -> None:
    tk = FS.toolkit()
    union = tk.union(NC_POS_F | NC_NEG_F, NC_POS_G | NC_NEG_G)
    assert len(union.classes) == 4


def test_tk_tier_nc() -> None:
    tk = FS.toolkit()
    word = FS.word([A, B, C, D, I])
    assert tk.tier(word, NC_POS_F) == FS.word([A, B])


def test_tk_tier_union() -> None:
    tk = FS.toolkit()
    word = FS.word([A, B, C, D, I])
    union = NC_NEG_F | NC_POS_G
    assert tk.tier(word, union) == FS.word([A, C, D])


def test_tk_natural_classes_over_count() -> None:
    tk = FS.toolkit()
    classes = list(tk.natural_classes_over(["F", "G"]))
    assert len(classes) == 9


def test_tk_natural_classes_over_excludes_empty() -> None:
    tk = FS.toolkit()
    classes = list(tk.natural_classes_over(["F", "G"], include_empty=False))
    assert len(classes) == 8
    assert FS.natural_class({}) not in classes


def test_tk_natural_classes_over_dedupes_and_sorts() -> None:
    tk = FS.toolkit()
    classes1 = list(tk.natural_classes_over(["G", "F", "F"]))
    classes2 = list(tk.natural_classes_over(["F", "G"]))
    assert classes1 == classes2


def test_tk_natural_classes_over_rejects_unknown_feature() -> None:
    tk = FS.toolkit()
    with pytest.raises(lp.UnknownFeatureError):
        list(tk.natural_classes_over(["F", "Z"]))


def test_tk_natural_classes_over_max_features_guard() -> None:
    tk = FS.toolkit()
    with pytest.raises(ValueError):
        list(tk.natural_classes_over(["F", "G"], max_features=1))


def test_tk_ngrams() -> None:
    tk = FS.toolkit()
    word = FS.word([A, B, C])
    result = tk.ngrams(word, 2)
    assert result == [
        (0, 2, FS.word([A, B])),
        (1, 3, FS.word([B, C])),
    ]


def test_tk_ngrams_with_boundaries() -> None:
    tk = FS.toolkit()
    word = FS.add_boundaries(FS.word([A, B]))
    result = tk.ngrams(word, 2)
    assert result == [
        (0, 2, FS.word([FS.BOS, A])),
        (1, 3, FS.word([A, B])),
        (2, 4, FS.word([B, FS.EOS])),
    ]


def test_tk_ngrams_rejects_nonpositive_n() -> None:
    tk = FS.toolkit()
    with pytest.raises(ValueError):
        tk.ngrams(FS.word([A, B]), 0)


def test_tk_intersect_segments() -> None:
    tk = FS.toolkit()
    assert tk.intersect(A, B) == E
    assert tk.intersect(A, D) == I


def test_tk_intersect_words() -> None:
    tk = FS.toolkit()
    w1 = FS.word([A, B])
    w2 = FS.word([B, C])
    assert tk.intersect(w1, w2) == FS.word([E, I])


def test_tk_project_segment() -> None:
    tk = FS.toolkit()
    assert tk.project(A, frozenset(["F"])) == E


def test_tk_project_word() -> None:
    tk = FS.toolkit()
    word = FS.word([A, B])
    assert tk.project(word, frozenset(["F"])) == FS.word([E, E])


def test_tk_project_accepts_list() -> None:
    tk = FS.toolkit()
    word = FS.word([A, B])
    assert tk.project(word, ["F"]) == FS.word([E, E])


def test_tk_min_intensions_unique() -> None:
    tk = FS.toolkit()
    minimals = tk.min_intensions([A, B], INV)
    assert minimals == [NC_POS_F]


def test_tk_min_intensions_non_unique() -> None:
    tk = FS.toolkit()
    inv = FS.inventory({"A": A, "D": D})
    minimals = tk.min_intensions([A], inv)
    assert minimals == [NC_POS_F, NC_POS_G]


def test_tk_min_intensions_no_solution_with_restricted_features() -> None:
    tk = FS.toolkit()
    minimals = tk.min_intensions([A], INV, features=["F"])
    assert minimals == []


def test_tk_min_intensions_rejects_empty_segments() -> None:
    tk = FS.toolkit()
    with pytest.raises(ValueError):
        tk.min_intensions([], INV)


def test_tk_min_intensions_rejects_unknown_restriction_feature() -> None:
    tk = FS.toolkit()
    with pytest.raises(lp.UnknownFeatureError):
        tk.min_intensions([A, B], INV, features=["F", "Z"])
