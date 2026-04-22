from itertools import product
from typing import Iterator

import pytest
from hypothesis import given
from hypothesis import strategies as st

import logical_phonology as lp

feature_value_strategy = st.sampled_from([lp.POS, lp.NEG])
feature_spec_strategy = st.dictionaries(
    keys=st.sampled_from(["F1", "F2"]),
    values=feature_value_strategy,
)


@pytest.fixture
def fs() -> lp.FeatureSystem:
    valid_features = frozenset(["F1", "F2"])
    return lp.FeatureSystem(valid_features)


@pytest.fixture
def inv(fs: lp.FeatureSystem) -> lp.Inventory:
    names = ["A", "B", "C", "D"]
    values = list(product([lp.POS, lp.NEG], repeat=2))
    segments = {
        name: fs.segment({"F1": f1, "F2": f2})
        for name, (f1, f2) in zip(names, values)
    }
    return fs.inventory(segments)


def test_boundary_natural_class_generation(fs: lp.FeatureSystem) -> None:
    assert fs.BOS in fs.BOS_NC
    assert fs.EOS in fs.EOS_NC


def test_alias_error() -> None:
    valid_features = frozenset(["F1", "F2"])
    fs = lp.FeatureSystem(valid_features)
    seg = fs.segment({"F1": lp.POS, "F2": lp.NEG})
    with pytest.raises(lp.AliasError) as exc_info:
        fs.inventory({"A": seg, "B": seg}, allow_aliases=False)
    assert "A" in str(exc_info.value) or "B" in str(exc_info.value)


@given(feature_spec_strategy)
def test_segment_membership(feature_spec: dict[str, lp.FeatureValue]) -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2"]))
    seg = fs.segment(feature_spec)
    inv = fs.inventory({"A": seg})
    assert seg in inv  # check segment_to_name
    assert "A" in inv  # check name_to_segment


@given(feature_spec_strategy)
def test_name_of_roundtrip(feature_spec: dict[str, lp.FeatureValue]) -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2"]))
    seg = fs.segment(feature_spec)
    inv = fs.inventory({"A": seg})
    assert inv[inv.name_of(seg)] == seg


def test_segments_lookup(inv: lp.Inventory) -> None:
    assert [inv[n] for n in ["A", "B"]] == [inv["A"], inv["B"]]


def test_segments_lookup_unknown_raises(inv: lp.Inventory) -> None:
    with pytest.raises(lp.UnknownNameError):
        inv["Z"]


def test_aliased_segment_name_of() -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2"]))
    seg = fs.segment({"F1": lp.POS, "F2": lp.NEG})
    inv = fs.inventory({"A": seg, "B": seg})
    # name_of returns canonical form for aliased segments
    assert inv.name_of(seg) == str(seg)
    # canonical form can be looked up
    assert inv[inv.name_of(seg)] == seg


def test_render(inv: lp.Inventory, fs: lp.FeatureSystem) -> None:
    word = fs.word([inv["A"], inv["B"]])
    assert inv.render(word) == "AB"


def test_render_with_boundaries(
    inv: lp.Inventory, fs: lp.FeatureSystem
) -> None:
    word = fs.add_boundaries(fs.word([inv["A"], inv["B"]]))
    assert inv.render(word) == "⋉AB⋊"


def test_render_aliased_segment(fs: lp.FeatureSystem) -> None:
    seg = fs.segment({"F1": lp.POS, "F2": lp.NEG})
    inv_alias = fs.inventory({"A": seg, "B": seg})
    word = fs.word([seg])
    assert inv_alias.render(word) == str(seg)


def test_simple_tokenize(inv: lp.Inventory) -> None:
    word = inv.tokenize("ABCD")
    assert len(word) == 4
    assert word[0] == inv["A"]
    assert word[1] == inv["B"]
    assert word[2] == inv["C"]
    assert word[3] == inv["D"]


def test_tokenize_with_boundaries(inv: lp.Inventory) -> None:
    word = inv.tokenize("⋉AB⋊")
    assert len(word) == 4
    assert word[0] == inv["⋉"]
    assert word[1] == inv["A"]
    assert word[2] == inv["B"]
    assert word[3] == inv["⋊"]


def test_tokenize_empty_string(inv: lp.Inventory) -> None:
    word = inv.tokenize("")
    assert len(word) == 0


def test_untokenizable_input(inv: lp.Inventory) -> None:
    with pytest.raises(lp.UntokenizableInputError) as exc_info:
        inv.tokenize("ABCDE")
    assert "E" in exc_info.value.input_str


def test_ambiguous_tokenization() -> None:
    valid_features = frozenset(["F1", "F2"])
    fs = lp.FeatureSystem(valid_features)
    names = ["A", "AA", "AAA", "AAAA"]
    values = list(product([lp.POS, lp.NEG], repeat=2))
    segments = {
        name: fs.segment({"F1": f1, "F2": f2})
        for name, (f1, f2) in zip(names, values)
    }
    inv = fs.inventory(segments)
    tokenizations = inv.tokenize("AAAA", allow_ambiguity=True)
    assert len(tokenizations) == 8


def test_delimited_tokenization(inv: lp.Inventory) -> None:
    word = inv.tokenize("A B C D")
    assert len(word) == 4
    assert word[0] == inv["A"]
    assert word[1] == inv["B"]
    assert word[2] == inv["C"]
    assert word[3] == inv["D"]


def test_delimited_tokenization_multiple_spaces(inv: lp.Inventory) -> None:
    word = inv.tokenize("A  B  C")
    assert len(word) == 3
    assert word[0] == inv["A"]
    assert word[1] == inv["B"]
    assert word[2] == inv["C"]


def test_fail_delimited_tokenization_with_bad_input(inv: lp.Inventory) -> None:
    with pytest.raises(lp.UntokenizableInputError) as exc_info:
        inv.tokenize("A B C DD")
    assert "DD" in exc_info.value.input_str


def test_render_tokenize_roundtrip(
    inv: lp.Inventory, fs: lp.FeatureSystem
) -> None:
    word = fs.word([inv["A"], inv["B"], inv["C"]])
    assert inv.tokenize(inv.render(word)) == word


def test_render_tokenize_roundtrip_aliased(fs: lp.FeatureSystem) -> None:
    seg = fs.segment({"F1": lp.POS, "F2": lp.NEG})
    inv_alias = fs.inventory({"A": seg, "B": seg})
    word = fs.word([seg])
    # render produces canonical form, tokenize can parse it back
    assert inv_alias.tokenize(inv_alias.render(word)) == word


def test_over_natural_classes(inv: lp.Inventory, fs: lp.FeatureSystem) -> None:
    nc1 = fs.natural_class({})
    assert len(list(nc1.over(inv))) == 4  # boundaries filtered by default
    assert (
        len(list(nc1.over(inv, filter_boundaries=False))) == 6
    )  # includes boundaries
    nc2 = fs.natural_class({"F1": lp.POS})
    assert len(list(nc2.over(inv))) == 2
    nc3 = fs.natural_class({"F1": lp.POS, "F2": lp.POS})
    assert len(list(nc3.over(inv))) == 1  # only one segment with {+F1,+F2}


def test_over_natural_class_sequences(
    inv: lp.Inventory, fs: lp.FeatureSystem
) -> None:
    ncs1 = lp.NaturalClassSequence((fs.natural_class({}),))
    assert len(list(ncs1.over(inv))) == 4  # boundaries filtered (default)
    assert (
        len(list(ncs1.over(inv, filter_boundaries=False))) == 6
    )  # includes boundaries
    ncs2 = fs.natural_class({}) + fs.natural_class({})
    assert len(list(ncs2.over(inv))) == 16  # 4**2
    assert len(list(ncs2.over(inv, filter_boundaries=False))) == 36  # 6**2
    ncs3 = fs.natural_class({"F1": lp.POS}) + fs.natural_class({"F1": lp.POS})
    assert len(list(ncs3.over(inv))) == 4  # 2**2


def test_over_returns_iterators(
    inv: lp.Inventory, fs: lp.FeatureSystem
) -> None:
    nc = fs.natural_class({})
    ncs = lp.NaturalClassSequence((nc,))
    assert isinstance(nc.over(inv), Iterator)
    assert isinstance(ncs.over(inv), Iterator)


def test_basic_extend(inv: lp.Inventory, fs: lp.FeatureSystem) -> None:
    new_seg = fs.segment({"F1": lp.POS})
    inv2 = inv.extend({"Z": new_seg})
    assert "Z" in inv2
    assert inv2["Z"] == new_seg
    with pytest.raises(lp.UntokenizableInputError) as exc_info:
        inv.tokenize("Z")
    assert "Z" in exc_info.value.input_str
    word = inv2.tokenize("Z")
    assert word[0] == new_seg


def test_duplicate_name(inv: lp.Inventory, fs: lp.FeatureSystem) -> None:
    with pytest.raises(lp.DuplicateNameError) as exc_info:
        inv.extend({"A": fs.segment({})})
    assert "A" in exc_info.value.conflicts


def test_extend_alias_error(inv: lp.Inventory, fs: lp.FeatureSystem) -> None:
    inv_no_aliases = fs.inventory(
        {name: inv[name] for name in ["A", "B", "C", "D"]},
        allow_aliases=False,
    )
    dup_segment = inv["A"]
    with pytest.raises(lp.AliasError) as exc_info:
        inv_no_aliases.extend({"Q": dup_segment})
    assert str(dup_segment) in exc_info.value.aliased


def test_full_inventory_length(fs: lp.FeatureSystem) -> None:
    inv = fs.full_inventory()
    # 3^2 = 9 segments, + 2 boundary segments
    assert len(inv.segment_to_name) == 3 ** len(fs.valid_features) + 2


def test_full_inventory_extend_aliases(fs: lp.FeatureSystem) -> None:
    inv = fs.full_inventory()
    seg = fs.segment({"F1": lp.POS, "F2": lp.POS})
    inv2 = inv.extend({"A": seg})
    # {+F1+F2} already exists in `inv` under its canonical name.
    # Extending with inv2 should just add an alias for this segment
    assert "A" in inv2
    assert inv2["A"] == seg
    assert inv2.name_of(seg) == str(seg)  # Canonical form wins when aliased


def test_full_inventory_explosion_error() -> None:
    fs = lp.FeatureSystem(frozenset(["F1", "F2", "F3"]))
    with pytest.raises(lp.CombinatoricExplosionError) as exc_info:
        fs.full_inventory(max_feature_set_length=2)
    assert exc_info.value.max_length == 2
    assert exc_info.value.actual_length == 3


def test_len_returns_right_length(fs: lp.FeatureSystem) -> None:
    inv = fs.full_inventory()
    assert len(inv) == 3**2 + 2  # two-features, plus two boundary segments


# min_intensions

_FS = lp.FeatureSystem(frozenset(["F", "G"]))
_A = _FS.segment({"F": lp.POS, "G": lp.POS})
_B = _FS.segment({"F": lp.POS, "G": lp.NEG})
_C = _FS.segment({"F": lp.NEG, "G": lp.POS})
_D = _FS.segment({"F": lp.NEG, "G": lp.NEG})
_INV = _FS.inventory({"A": _A, "B": _B, "C": _C, "D": _D})
_NC_POS_F = _FS.natural_class({"F": lp.POS})
_NC_POS_G = _FS.natural_class({"G": lp.POS})


def test_min_intensions_unique() -> None:
    assert _INV.min_intensions([_A, _B]) == [_NC_POS_F]


def test_min_intensions_non_unique() -> None:
    inv = _FS.inventory({"A": _A, "D": _D})
    assert inv.min_intensions([_A]) == [_NC_POS_F, _NC_POS_G]


def test_min_intensions_no_solution_with_restricted_features() -> None:
    assert _INV.min_intensions([_A], features=["F"]) == []


def test_min_intensions_rejects_empty_segments() -> None:
    with pytest.raises(ValueError):
        _INV.min_intensions([])


def test_min_intensions_rejects_unknown_restriction_feature() -> None:
    with pytest.raises(lp.UnknownFeatureError):
        _INV.min_intensions([_A, _B], features=["F", "Z"])


def test_min_intensions_ignores_duplicate_target_segments() -> None:
    assert _INV.min_intensions([_A, _A, _B]) == _INV.min_intensions([_A, _B])


def test_min_intensions_empty_feature_restriction_returns_none() -> None:
    assert _INV.min_intensions([_A], features=[]) == []


# extensions_to_intensions


def test_extensions_to_intensions_basic() -> None:
    result = _INV.extensions_to_intensions(["F", "G"])
    # {+F} picks out A and B
    ext_pos_f = frozenset([_A, _B])
    assert ext_pos_f in result
    assert _FS.natural_class({"F": lp.POS}) in result[ext_pos_f].intensions


def test_extensions_to_intensions_minimal() -> None:
    result = _INV.extensions_to_intensions(["F", "G"])
    ext_pos_f = frozenset([_A, _B])
    entry = result[ext_pos_f]
    # {+F} is minimal (1 feature); {+F,+G} and {+F,-G} are longer
    assert all(
        len(nc.feature_specification) <= len(m.feature_specification)
        for nc in entry.intensions
        for m in entry.minimal_intensions
    )


def test_extensions_to_intensions_excludes_empty_extension() -> None:
    result = _INV.extensions_to_intensions(["F", "G"])
    assert all(len(ext) > 0 for ext in result)


def test_extensions_to_intensions_defaults_to_all_features() -> None:
    result_explicit = _INV.extensions_to_intensions(["F", "G"])
    result_default = _INV.extensions_to_intensions()
    assert result_explicit == result_default


def test_extensions_to_intensions_rejects_unknown_feature() -> None:
    with pytest.raises(lp.UnknownFeatureError):
        _INV.extensions_to_intensions(["F", "Z"])


def test_extensions_to_intensions_max_features_guard() -> None:
    with pytest.raises(ValueError):
        _INV.extensions_to_intensions(["F", "G"], max_features=1)
