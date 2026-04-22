import logical_phonology as lp

FS = lp.FeatureSystem(frozenset(["F", "G"]))

A = FS.segment({"F": lp.POS, "G": lp.POS})
B = FS.segment({"F": lp.POS, "G": lp.NEG})
C = FS.segment({"F": lp.NEG, "G": lp.POS})
D = FS.segment({"F": lp.NEG, "G": lp.NEG})
U = FS.segment({})  # underspecified

INV = FS.inventory({"A": A, "B": B, "C": C, "D": D, "U": U})

NC_POS_F = FS.natural_class({"F": lp.POS})
NC_NEG_F = FS.natural_class({"F": lp.NEG})
NC_POS_G = FS.natural_class({"G": lp.POS})
NC_NEG_G = FS.natural_class({"G": lp.NEG})


### NaturalClass.__or__ ###


def test_nc_or_returns_union() -> None:
    union = NC_POS_F | NC_NEG_F
    assert isinstance(union, lp.NaturalClassUnion)


def test_nc_or_contains_both_classes() -> None:
    union = NC_POS_F | NC_NEG_F
    assert len(union.classes) == 2


def test_nc_or_union_prepends_class() -> None:
    union = NC_POS_F | (NC_NEG_F | NC_POS_G)
    assert len(union.classes) == 3
    assert union.classes[0] == NC_POS_F
    assert union.classes[1] == NC_NEG_F
    assert union.classes[2] == NC_POS_G


### NaturalClassUnion.__contains__ ###


def test_union_contains_segment_in_first_class() -> None:
    union = NC_POS_F | NC_NEG_G
    assert A in union  # A has +F


def test_union_contains_segment_in_second_class() -> None:
    union = NC_POS_F | NC_NEG_G
    assert D in union  # D has -G


def test_union_does_not_contain_unmatched_segment() -> None:
    union = NC_POS_F | NC_NEG_G
    assert C not in union  # C has -F and +G


def test_union_does_not_contain_underspecified() -> None:
    union = NC_POS_F | NC_NEG_F
    assert U not in union  # U has no F value


### NaturalClassUnion.__or__ chaining ###


def test_union_or_nc_extends() -> None:
    union = NC_POS_F | NC_NEG_F | NC_POS_G
    assert len(union.classes) == 3


def test_union_or_union_merges() -> None:
    u1 = NC_POS_F | NC_NEG_F
    u2 = NC_POS_G | NC_NEG_G
    merged = u1 | u2
    assert len(merged.classes) == 4


def test_union_str() -> None:
    union = NC_POS_F | NC_NEG_G
    assert str(union) == "[{+F}|{-G}]"


### NaturalClassSequence with union positions ###


def test_ncs_matches_at_with_union() -> None:
    union = NC_POS_F | NC_NEG_F
    ncs = lp.NaturalClassSequence((union,))
    word = FS.word([A])
    assert ncs.matches_at(word, 0)


def test_ncs_matches_at_union_false_for_underspecified() -> None:
    union = NC_POS_F | NC_NEG_F
    ncs = lp.NaturalClassSequence((union,))
    word = FS.word([U])
    assert not ncs.matches_at(word, 0)


def test_ncs_find_all_with_union() -> None:
    union = NC_POS_F | NC_NEG_F
    ncs = lp.NaturalClassSequence((union,))
    word = FS.word([A, U, C])
    assert word.find_all(ncs) == [0, 2]


def test_ncs_multi_position_with_union() -> None:
    union = NC_POS_F | NC_NEG_F
    ncs = union + NC_POS_G
    word = FS.word([A, C])  # A has +F (in union), C has +G
    assert ncs.matches_at(word, 0)


def test_over_with_union() -> None:
    union = NC_POS_F | NC_NEG_F
    ncs = lp.NaturalClassSequence((union,))
    results = list(ncs.over(INV))
    # should include all segments with +F or -F (A, B, C, D but not U)
    assert len(results) == 4


def test_union_over_and_extension() -> None:
    union = NC_POS_F | NC_NEG_G
    over = tuple(union.over(INV))
    assert all(isinstance(seg, lp.Segment) for seg in over)
    names = tuple(name for name, _ in union.extension(INV))
    assert names == ("A", "B", "D")
