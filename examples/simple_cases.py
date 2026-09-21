"""Print the six-case paradigm of Kyrgyz words.

Usage:
    python examples/simple_cases.py                  # a built-in sample of words
    python examples/simple_cases.py үй Алибек Ош     # your own words
    python examples/simple_cases.py --strict БИШКЕК  # refuse uncertain forms instead of marking them
"""

import argparse

from kyrgyz import KyrgyzError, inflect_detailed
from kyrgyz.cases import Case

SAMPLE_WORDS = [
    "Алибек",
    "Бекзат",
    "Айбек",
    "Нурбек",
    "Азамат",
    "Эрмек",
    "Бишкек",
    "Ош",
    "Каракол",
    "Нарын",
    "Талас",
    "Ысык-Көл",
    "үй",
    "мектеп",
    "апа",
    "китеп",
    "кол",
    "туз",
    "көз",
    "мен",
]


def paradigm(word: str, *, strict: bool) -> list[str]:
    """Return the word's forms in all six cases; uncertain forms end with '*'."""
    forms = []
    for case in Case:
        result = inflect_detailed(word, case=case, strict=strict)
        forms.append(result.text if result.is_certain else result.text + "*")
    return forms


def main() -> None:
    parser = argparse.ArgumentParser(description="Inflect Kyrgyz words for all six cases.")
    parser.add_argument("words", nargs="*", default=SAMPLE_WORDS, help="words to inflect")
    parser.add_argument("--strict", action="store_true", help="raise instead of marking uncertain forms")
    args = parser.parse_args()

    rows = [[case.kyrgyz_name.split()[0] for case in Case]]
    errors = []
    for word in args.words:
        try:
            rows.append(paradigm(word, strict=args.strict))
        except KyrgyzError as error:
            errors.append(f"{word}: {error}")

    widths = [max(len(row[i]) for row in rows) for i in range(len(Case))]
    for index, row in enumerate(rows):
        print("  ".join(form.ljust(width) for form, width in zip(row, widths, strict=True)).rstrip())
        if index == 0:
            print("  ".join("-" * width for width in widths))

    if any("*" in form for row in rows[1:] for form in row):
        print("\n* uncertain form; see inflect_detailed(...).uncertainties")
    for message in errors:
        print(f"\nerror: {message}")


if __name__ == "__main__":
    main()
