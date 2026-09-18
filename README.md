# kyrgyz

A rule-based **morphological engine for Kyrgyz** (кыргыз тили). Given a word and
a grammatical target such as the dative case, it produces the correct surface
form by applying Kyrgyz vowel harmony and consonant assimilation. It does not
look words up in a table of suffixes.

```python
from kyrgyz import inflect
from kyrgyz.cases import DATIVE

inflect("Алибек", case=DATIVE)  # 'Алибекке'
inflect("үй", case=DATIVE)  # 'үйгө'
inflect("мектеп", case=DATIVE)  # 'мектепке'
inflect("апа", case=DATIVE)  # 'апага'
```

This is not a translation library, and it does not simply glue `-ке` onto
strings: `туз → тузга` but `кол → колго`, `педагог → педагогго`,
`мен → мага`. Every rule is sourced; see [docs/linguistics.md](docs/linguistics.md).

* Zero runtime dependencies, standard library only
* Python ≥ 3.10, fully typed (`mypy --strict`), immutable data, no global mutable state
* Modern Cyrillic Kyrgyz orthography

## What is supported

| Area | Status |
|---|---|
| The six cases of the plain (non-possessive) declension | ✅ |
| Vowel harmony, including the у → а rounding asymmetry | ✅ |
| Suffix-initial consonant assimilation (г/к, д/т, н/д/т) | ✅ |
| Loanwords: written voiced finals (§32), я/ё/ю/э, final ь | ✅ |
| Proper names, hyphenated and multi-word names | ✅ |
| Abbreviations (orthographic rules §55) | ✅ with metadata |
| Irregular personal pronouns (мен, сен, ал) | ✅ |
| Letter-case preservation, Unicode NFC normalisation | ✅ |
| Plural, possessive, possessive declension | 🔜 Phase 3 |
| Verbs: person, tense, mood, negation, politeness | 🔜 Phase 4 |

## Installation

```bash
pip install kyrgyz            # once published to PyPI
pip install .                 # from a clone of this repository
pip install -e ".[dev]"       # development: pytest, mypy, ruff
```

## Usage

### Cases

```python
from kyrgyz import inflect
from kyrgyz.cases import Case

for case in Case:
    print(f"{case.kyrgyz_name:<15} {inflect('Бишкек', case=case)}")
```

| Case | Kyrgyz term | Suffix | Бишкек | үй | апа | кол | туз |
|---|---|---|---|---|---|---|---|
| `NOMINATIVE` | Атооч жөндөмө | -∅ | Бишкек | үй | апа | кол | туз |
| `GENITIVE` | Илик жөндөмө | -NIн | Бишкектин | үйдүн | апанын | колдун | туздун |
| `DATIVE` | Барыш жөндөмө | -GA | Бишкекке | үйгө | апага | колго | тузга |
| `ACCUSATIVE` | Табыш жөндөмө | -NI | Бишкекти | үйдү | апаны | колду | тузду |
| `LOCATIVE` | Жатыш жөндөмө | -DA | Бишкекте | үйдө | апада | колдо | тузда |
| `ABLATIVE` | Чыгыш жөндөмө | -DAн | Бишкектен | үйдөн | ападан | колдон | туздан |

Readability aliases exist: `TO = DATIVE`, `FROM = ABLATIVE`, `IN = LOCATIVE`,
`OF = GENITIVE` (`from kyrgyz.cases import TO`). They are the same objects as
the canonical members.

### Names, compounds and loanwords

```python
inflect("Ысык-Көл", case=DATIVE)  # 'Ысык-Көлгө'   suffix attaches to the last word
inflect("Алибек Асанов", case=DATIVE)  # 'Алибек Асановго'
inflect("педагог", case=DATIVE)  # 'педагогго'    orthographic rules §32
inflect("Алиев", case=GENITIVE)  # 'Алиевдин'     §32
inflect("Россия", case=DATIVE)  # 'Россияга'
inflect("мен", case=DATIVE)  # 'мага'         irregular pronoun
```

### Letter case

The stem is returned exactly as given. The suffix is uppercase only if the last
word is all caps (at least two letters, all uppercase):

```python
inflect("Алибек", case=DATIVE)  # 'Алибекке'
inflect("албек", case=DATIVE)  # 'албекке'
inflect("БИШКЕК", case=DATIVE)  # 'БИШКЕККЕ'  (flagged: could be an abbreviation)
inflect("Мен", case=DATIVE)  # 'Мага'      lexicon forms copy the input's capitalisation
```

### Abbreviations

Orthographic rules §55 say that a suffix on an abbreviation follows its
**pronunciation** and is written in **lowercase**. Supply that information with
a `Word`:

```python
from kyrgyz import Word

inflect(Word("БУУ", abbreviation=True, pronunciation="буу"), case=DATIVE)  # 'БУУга'
inflect(Word("КТР", abbreviation=True, pronunciation="катээр"), case=GENITIVE)  # 'КТРдин'
```

### No silent guessing: diagnostics and strict mode

Some results depend on assumptions that the spelling cannot confirm.
`inflect_detailed` returns the form together with how it was derived and any
`Uncertainty` flags:

```python
from kyrgyz import inflect_detailed

result = inflect_detailed("медаль", case=DATIVE)
result.text, result.stem, result.suffix  # ('медалга', 'медал', 'га')
result.uncertainties  # {Uncertainty.SOFT_SIGN_DROPPED}
result.is_certain  # False
```

| Uncertainty | When |
|---|---|
| `POSSIBLE_ABBREVIATION` | all-caps input without `Word(..., abbreviation=...)` |
| `ABBREVIATION_READING_ASSUMED` | `abbreviation=True` without a `pronunciation` |
| `SOFT_SIGN_DROPPED` | loanword ending in `ь` (attested usage, not codified) |

By default `inflect` returns these best-effort forms. With `strict=True`, it
raises `AmbiguousWordError` instead:

```python
inflect("БИШКЕК", case=DATIVE, strict=True)  # raises
inflect(Word("БИШКЕК", abbreviation=False), case=DATIVE, strict=True)  # 'БИШКЕККЕ'
```

Some inputs can never be inflected safely, and these **always** raise
`AmbiguousWordError`: a last word with no vowel letter (`КТР` without a
pronunciation), or a final `ъ`.

### Errors

| Exception | Raised for |
|---|---|
| `InvalidWordError` (also a `ValueError`) | empty input, Latin letters or look-alikes, digits, punctuation, non-Kyrgyz Cyrillic (`ұ`, `ә`), stray hyphens/spaces |
| `AmbiguousWordError` | suffix cannot be chosen without guessing; strict-mode uncertainty |
| `TypeError` | a non-`str` word or a non-`Case` case |

All library errors derive from `KyrgyzError`. Input is NFC-normalised, so a
decomposed `й` (и + U+0306) or `ё` (е + U+0308) works.

### Lexical exceptions

A `Lexicon` holds listed forms that override the rules. It is immutable:
adding an entry returns a new lexicon, which you give to an `Inflector`.

```python
from kyrgyz import Inflector, Lexicon

lexicon = Lexicon.default().with_exception("бул", case=DATIVE, form="буга", source="буга чейин")
inflector = Inflector(lexicon=lexicon)
inflector.inflect("бул", case=DATIVE)  # 'буга'  (the rules alone give 'булга')
```

The default lexicon contains only the irregular forms of мен, сен and ал. Use
`Inflector(lexicon=Lexicon.empty())` to apply rules only, for example when `ал`
is the noun "strength" (`алдан`) rather than the pronoun (`андан`).

## Architecture

```
inflect("Алибек", case=DATIVE)
        │
        ▼
Word ─────────────── validate letters, NFC-normalise, metadata   (word.py)
        │
Features ─────────── the requested grammatical categories        (features.py)
        │
Lexicon lookup ───── listed irregular forms win                  (lexicon/)
        │ (not listed)
Morphology ───────── pick suffix template: DATIVE → "GA"         (morphology/case.py)
        │
Stem preparation ─── e.g. drop final ь                           (phonology/transformations.py)
        │
Phonological ─────── last vowel = е, final letter = к            (phonology/analysis.py)
analysis                (voiceless)
        │
Realisation ──────── G → к (after voiceless)                     (morphology/suffix.py,
        │            A → е (after е)                              phonology/consonants.py,
        │                                                         phonology/harmony.py)
Letter case ──────── suffix case follows the last word           (casing.py)
        │
        ▼
InflectionResult("Алибекке", stem="Алибек", suffix="ке", ...)   (inflector.py)
```

Suffixes are written the way grammars write them, as **templates of
archiphonemes**: `A` (а/е/о/ө), `I` (ы/и/у/ү), `G` (г/к), `D` (д/т),
`N` (н/д/т). The whole case system is one six-line table:

```python
Case.GENITIVE: SuffixTemplate("NIн")
Case.DATIVE: SuffixTemplate("GA")
Case.ACCUSATIVE: SuffixTemplate("NI")
Case.LOCATIVE: SuffixTemplate("DA")
Case.ABLATIVE: SuffixTemplate("DAн")
```

Each archiphoneme resolves through one small, independently tested function.
Realisation runs left to right and updates the phonological profile after each
letter, so suffixes chain naturally (for example, a future plural `-LAр`
followed by a case suffix).

| Module | Responsibility |
|---|---|
| `kyrgyz.cases` | `Case` enum, constants, aliases, Kyrgyz names |
| `kyrgyz.features` | `Features`, the bundle of requested categories |
| `kyrgyz.word` | `Word`, input validation and normalisation |
| `kyrgyz.phonology` | letter features, harmony, consonant assimilation, stem analysis |
| `kyrgyz.morphology` | suffix templates, case table, attaching suffixes |
| `kyrgyz.lexicon` | immutable exception lexicon and the pronoun data |
| `kyrgyz.casing` | letter-case policy |
| `kyrgyz.inflector` | the pipeline, `InflectionResult`, public functions |
| `kyrgyz.diagnostics`, `kyrgyz.errors` | `Uncertainty` flags and exceptions |

### API design notes

* **One entry point, keyword-only features.** `inflect(word, case=...)` will grow
  `number=`, `possessor=` and so on without breaking callers, and all features
  default to neutral values.
* **No `to()`/`from_()` helpers.** `from` is a Python keyword, and a family of
  one-case functions would not extend to plural or possessive combinations.
  The `TO`/`FROM`/`IN`/`OF` aliases give the same readability.
* **Immutable lexicon instead of `register_exception()`.** A global registry
  would make results depend on import order and on other code in the process.
  `Lexicon.with_exception()` returns a new object, so behaviour stays explicit
  and thread-safe.
* **Separate modules instead of one module per case.** Every case shares the
  same machinery and differs only by its template, so one table is clearer
  than six near-empty files.

## Limitations

* **Possessive forms are not recognised.** A word that already carries a
  3rd-person possessive suffix takes different case endings
  (*Кыргыз Республикасы* → *Республикасы**на***). The library cannot yet know
  this and produces *Республикасыга*. This will be solved in Phase 3 by letting
  the caller build possessive forms (or mark them) instead of guessing.
* **Other irregular stems are not listed.** Demonstratives (бул → буга)
  and other irregular words are not in the default lexicon yet, pending sourced
  paradigms. Add them with `Lexicon.with_exception`.
* **Variant forms**: only the standard form is produced. For example, the
  colloquial ablative *кишинен* for *кишиден* is not produced.
* **Homographs** are not disambiguated: `ал` is always the pronoun unless you
  use an empty lexicon.
* **Scope of input**: Cyrillic Kyrgyz only. No Latin or Arabic script, no
  numerals (Kyrgyz writes `5-класска` with a hyphen, which is not yet
  supported), no punctuation.
* **Loanwords** follow their written form, as the orthographic rules require.
  Speakers sometimes pronounce recent loans differently.

See [docs/linguistics.md](docs/linguistics.md) for the full rule inventory and
known variation.

## Development

```bash
pip install -e ".[dev]"
pytest              # unit tests + doctests
mypy                # strict type checking
ruff check . && ruff format --check .
```

## Contributing

Contributions from linguists and developers are welcome.

1. **Cite before you code.** A new rule or exception needs an authoritative
   source: a grammar, the orthographic rules, a university textbook, or a
   corpus attestation. Add it to `docs/linguistics.md` together with the
   implementation.
2. **Prefer rules to exceptions.** Add a lexicon entry only for true
   irregularity (suppletion, irregular stems), never to make a test pass.
3. **Test each rule in isolation.** Put tests next to the layer they exercise
   (`tests/phonology`, `tests/morphology`, `tests/cases`, `tests/lexicon`), and
   note the source of cited forms inline.
4. **Keep layers separate.** Phonology must not know about grammatical
   categories. Morphology must not know about letter case or error policy.
5. **Do not guess.** If spelling cannot determine the answer, raise an error or
   add an `Uncertainty`.

## Roadmap

* **Phase 3**: plural (`-LAр`: л/д/т alternation), possessive suffixes,
  the possessive declension (`-нА`, `-нДА`, `-нАн`), stem voicing к→г / п→б
  before vowel-initial suffixes, and plural + case, possessive + case.
* **Phase 4**: verbs: person endings, tense/aspect/mood, negation, politeness.

## References

* *Кыргыз тилинин жазуу эрежелери* (Orthographic rules of the Kyrgyz language),
  §§7, 27, 32, 33, 38, 55. <https://tamgasoft.kg/en/archives/372.html>
* Абдувалиев И. *Кыргыз тилинин морфологиясы*.
  <https://arch.kyrlibnet.kg/uploads/Abduvaliev%20morfologya.pdf>
* *Кыргыз тилинин грамматикасы: морфология.* Фрунзе, 1964 (cited by Абдувалиев).
* Kara, D. S. (2003). *Kyrgyz*. Lincom Europa.
* Washington, J. N., et al. *apertium-kir*: Kyrgyz morphological transducer.
  <https://github.com/apertium/apertium-kir>
* Wikipedia, "Kyrgyz language": Case; Pronouns.
  <https://en.wikipedia.org/wiki/Kyrgyz_language>

## License

MIT. See [LICENSE](LICENSE).
