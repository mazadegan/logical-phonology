# logical-phonology

A Python library implementing the core primitives and operations of Logical
Phonology (LP). Given a universal feature set, the library provides a 
structured way to build and manipulate the formal objects that LP is built 
on — segments, natural classes, natural class sequences, words, and segment 
inventories.

All objects are constructed through a central `FeatureSystem` instance, 
which enforces feature validity and provides a clean, consistent API for 
building LP structures.

> Logical Phonology is a formal framework for phonological computation.
> For an introduction to the theory and its literature, see the 
> [Logical Phonology Archive](https://wellformedness.com/loa/).

## Installation
```bash
pip install logical-phonology
```
## Quick Start

### Defining a Feature System

All objects in `logical-phonology` are built from a `FeatureSystem`, which 
defines the universal set of valid features for your analysis:
```python
import logical_phonology as lp

fs = lp.FeatureSystem(frozenset(["F1", "F2", "F3"]))
```

### Building Segments

Segments are feature bundles constructed through the feature system:
```python
seg1 = fs.segment({"F1": lp.POS, "F2": lp.NEG})
seg2 = fs.segment({"F1": lp.NEG})  # partial specification is allowed
seg3 = fs.segment({})              # fully underspecified segment
```

### Building an Inventory

An inventory gives names to segments, enabling tokenization and rendering. 
Here we use an example with `Syllabic`, `High`, `Low`, and 
`Back` features:
```python
fs = lp.FeatureSystem(frozenset(["Syllabic", "High", "Low", "Back"]))

inv = fs.inventory({
    "a": fs.segment({"Syllabic": lp.POS, "Low": lp.POS, "High": lp.NEG, "Back": lp.NEG}),
    "i": fs.segment({"Syllabic": lp.POS, "Low": lp.NEG, "High": lp.POS, "Back": lp.NEG}),
    "u": fs.segment({"Syllabic": lp.POS, "Low": lp.NEG, "High": lp.POS, "Back": lp.POS}),
    "p": fs.segment({"Syllabic": lp.NEG}),
    "t": fs.segment({"Syllabic": lp.NEG}),  # alias for same segment as "p"
    "k": fs.segment({"Syllabic": lp.NEG}),  # alias for same segment as "p"
})
```

Segments can be looked up by name, returning the underlying feature bundle:
```python
inv["a"]  # returns Segment({"Syllabic": POS, "Low": POS, "High": NEG, "Back": NEG})
inv["p"]  # returns Segment({"Syllabic": NEG})
```

Since `p`, `t`, and `k` all map to a segment with the same specification, 
`name_of` returns the canonical form for all of them. On the other hand, 
`a`, `i`, and `u` are fully distinguishable from every other segment:
```python
inv.name_of(inv["p"])  # returns "{-Syllabic}"
inv.name_of(inv["t"])  # returns "{-Syllabic}"
inv.name_of(inv["k"])  # returns "{-Syllabic}"
inv.name_of(inv["a"])  # returns "a"
inv.name_of(inv["i"])  # returns "i"
inv.name_of(inv["u"])  # returns "u"
```

#### Extending an Inventory

Inventories are immutable — `extend` returns a new inventory with additional 
segments:
```python
inv2 = inv.extend({
    "e": fs.segment({"Syllabic": lp.POS, "Low": lp.NEG, "High": lp.NEG, "Back": lp.NEG}),
})

"e" in inv   # False — original inventory unchanged
"e" in inv2  # True
```

### Building Words

Words are ordered sequences of segments. They can be constructed manually 
through the feature system:
```python
word = fs.word([
    fs.segment({"Syllabic": lp.NEG}), 
    fs.segment({"Syllabic": lp.POS, "Low": lp.POS, "High": lp.NEG, "Back": lp.NEG}), 
    fs.segment({"Syllabic": lp.NEG})
])
# OR, more conveniently...
word = fs.word([inv["p"], inv["a"], inv["t"]])  # "pat"
```

Or even more conveniently, words can be tokenized directly from a string using 
the inventory:
```python
word = inv.tokenize("pat")   # unspaced — uses recursive tokenization
word = inv.tokenize("p a t") # spaced — uses whitespace as delimiter
```

Rendering converts a word back to a string:
```python
inv.render(word)  # returns '{-Syllabic}a{-Syllabic}', as p and t are aliases of the same segment
```

> **Note:** If you want `render` to always produce human-readable names, 
> avoid aliases in your inventory. This can be enforced by passing 
> `allow_aliases=False` to `fs.inventory()`. See the API reference for 
> details.

#### Boundaries

Reserved boundary pseudo-segments can be added to mark the beginning and 
end of a word:
```python
bounded = fs.add_boundaries(word)  # ⋉pat⋊
inv.render(bounded)                # returns "⋉pat⋊"
```

Boundaries are pseudo-segments with reserved features — `BOS` for `⋉` and 
`EOS` for `⋊` — and can be accessed directly from the feature system or 
inventory:
```python
fs.BOS  # Segment({"BOS": POS})
fs.EOS  # Segment({"EOS": POS})
```

Bounded words can also be tokenized directly:
```python
inv.tokenize("⋉pat⋊")  # returns Word with boundaries included
```
### Natural Classes and Natural Class Sequences

A natural class is a partial feature specification that defines a set of 
segments. Natural classes are constructed through the feature system:
```python
syllabic = fs.natural_class({"Syllabic": lp.POS})   # all vowels
consonant = fs.natural_class({"Syllabic": lp.NEG})  # all consonants
universal_natural_class = fs.natural_class({})      # matches any segment
```

Membership is checked with the `in` operator:
```python
inv["a"] in syllabic   # True
inv["p"] in syllabic   # False
inv["p"] in consonant  # True
```

To iterate over all segments in a natural class, use `over()` with an 
inventory:
```python
for seg in syllabic.over(inv):
    print(inv.name_of(seg))  # prints "a", "i", "u"
```

A natural class sequence is an ordered list of natural classes, defining 
a set of words. They are useful for matching patterns like CV syllables:
```python
cv = fs.natural_class_sequence([consonant, syllabic])

inv["p"] in consonant  # True — single segment membership
inv.tokenize("pa") in cv  # True — word matches CV pattern
inv.tokenize("ap") in cv  # False — VC, not CV
```

To iterate over all words matching a sequence over an inventory of segments:
```python
for word in cv.over(inv):
    print(inv.render(word))  # prints all CV combinations
```

Natural class sequences also support substring matching via `matches_at` 
and `find_all`:
```python
word = inv.tokenize("pat")
consonant_nc = fs.natural_class_sequence([consonant])
consonant_nc.find_all(word)  # returns [0, 2] — consonants at positions 0 and 2
cv.find_all(word)  # returns [0] — CV pattern only at position 0
```

## Design Philosophy

**Single entry point.** `FeatureSystem` is the central factory object for 
the library. All LP primitives are constructed through a `FeatureSystem` 
instance, ensuring that feature validity is enforced at construction time.

> It is possible to construct objects directly without a `FeatureSystem`, 
> but this bypasses validation and is discouraged.

**Immutability.** All objects are frozen dataclasses. Once constructed, 
nothing can be mutated. This makes objects safe to use as dictionary keys 
and in sets, and ensures that operations like `subtract`, `unify`, and 
`project` return new segments rather than modifying existing ones.

**Make illegal states unrepresentable.** Reserved features cannot appear 
in user-defined segments. Unknown features are rejected at construction. 
Aliased segments receive canonical forms automatically.

**Partial specifications.** Segments can be underspecified. A segment 
need not specify every feature, and a natural class only specifies the 
features it cares about.

**Separation of concerns.** This library is purely about LP primitives 
and operations.

**Structured exceptions.** Every error carries structured attributes so 
callers can handle errors programmatically rather than parsing error 
strings.

**Zero dependencies.** The library is implemented entirely in the Python 
standard library, there are no external runtime dependencies.

## API Reference

Full API documentation is available in the [API Reference](https://github.com/mazadegan/logical-phonology/blob/main/docs/api_reference.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
