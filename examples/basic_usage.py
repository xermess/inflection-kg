"""Basic usage of the kyrgyz inflection library.

Run from the repository root:  python examples/basic_usage.py
"""

from kyrgyz import AmbiguousWordError, Inflector, Lexicon, Word, inflect, inflect_detailed
from kyrgyz.cases import DATIVE, GENITIVE, LOCATIVE, TO, Case

# 1. The dative ("to ...")
for name in ["Алибек", "Бекзат", "Айгүл", "үй", "мектеп", "апа", "Ош", "Ысык-Көл"]:
    print(f"{name:>10} → {inflect(name, case=DATIVE)}")

# 2. A full paradigm
print()
for case in Case:
    print(f"{case.kyrgyz_name:<15} {inflect('Бишкек', case=case)}")

# 3. Aliases read naturally in application code
print()
print(f"Билдирүү {inflect('Азамат', case=TO)} жөнөтүлдү.")  # "The notification was sent to Azamat."

# 4. Derivation details and diagnostics
print()
result = inflect_detailed("медаль", case=DATIVE)
print(result.text, "=", result.stem, "+", result.suffix, "| certain:", result.is_certain)
for uncertainty in result.uncertainties:
    print("  -", uncertainty.description)

# 5. Abbreviations (orthographic rules §55)
print()
print(inflect(Word("БУУ", abbreviation=True, pronunciation="буу"), case=DATIVE))
print(inflect(Word("КТР", abbreviation=True, pronunciation="катээр"), case=GENITIVE))

# 6. Strict mode refuses to guess
try:
    inflect("БИШКЕК", case=LOCATIVE, strict=True)
except AmbiguousWordError as error:
    print("\nstrict:", error)

# 7. Custom lexical exceptions without global state.
# The demonstrative бул "this" is irregular (буга, as in "буга чейин"); the rules alone give булга.
print()
print("rule only:", inflect("бул", case=DATIVE))
lexicon = Lexicon.default().with_exception("бул", case=DATIVE, form="буга", source="буга чейин")
print("with lexicon:", Inflector(lexicon=lexicon).inflect("бул", case=DATIVE))
