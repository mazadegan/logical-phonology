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


def test_tk_unify_segments() -> None:
    tk = FS.toolkit()
    # A has +F, +G. E has only +F. Unifying A with E should give A (left-biased, A already has G)
    assert tk.unify(A, E) == A
    # E has only +F. G has only +G. Unifying E with G should give A (+F, +G)
    assert tk.unify(E, G) == A
    # E has +F. F has -F. Unifying E with F should give E (left-biased, E wins on F)
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


def test_tk_project_segment() -> None:
    tk = FS.toolkit()
    assert tk.project(A, frozenset(["F"])) == E


def test_tk_project_word() -> None:
    tk = FS.toolkit()
    word = FS.word([A, B])
    assert tk.project(word, frozenset(["F"])) == FS.word([E, E])
