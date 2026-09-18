"""Complex inflection cases and generated Kyrgyz sentences.

Part 1 prints words grouped by the rule that makes them tricky.
Part 2 fills sentence templates, inflecting each slot for the case it needs.

Usage:
    python src/complex_cases.py                     # both parts
    python src/complex_cases.py --per-template 5    # more sentences
    python src/complex_cases.py --seed 7            # a different random selection
"""

from __future__ import annotations

import argparse
import random
import string
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from kyrgyz import KyrgyzError, Word, inflect, inflect_detailed
from kyrgyz.cases import Case

# --- Part 1: complex words ----------------------------------------------------------------


@dataclass(frozen=True)
class Group:
    title: str
    why: str
    words: tuple[str | Word, ...]


GROUPS = (
    Group(
        "у does not round the low vowel",
        "after у the suffix takes а (туз → тузга), unlike after о (кол → колго)",
        ("туз", "суу", "жумуш", "булут", "кол", "Токмок"),
    ),
    Group(
        "ү and ө do round it",
        "front rounded vowels give ө/ү suffixes",
        ("үй", "түлкү", "күмүш", "Өзгөн", "көпүрө"),
    ),
    Group(
        "disharmonic words and names",
        "only the last vowel counts",
        ("мугалим", "телефон", "Кыргызстан", "Алибек", "Жаныбек"),
    ),
    Group(
        "loanwords with a written voiced final",
        "the suffix follows the spelling: педагогго, not педагогко (orthographic rules §32)",
        ("педагог", "Калининград", "Алиев", "клуб", "гараж"),
    ),
    Group(
        "я, ё, ю, э",
        "harmonise as а, о, у, е",
        ("Россия", "актёр", "самолёт", "меню", "поэт"),
    ),
    Group(
        "final soft sign",
        "ь is dropped before the suffix; flagged because the rule is not codified",
        ("медаль", "роль", "автомобиль"),
    ),
    Group(
        "compound and multi-word names",
        "the suffix attaches to the last word",
        ("Ысык-Көл", "Чолпон-Ата", "Жалал-Абад", "Кара-Балта", "Айгүл Сейитбекова"),
    ),
    Group(
        "pronouns",
        "мен, сен, ал are irregular (lexicon); the others follow the rules",
        ("мен", "сен", "ал", "биз", "сиз", "алар"),
    ),
    Group(
        "capitals and abbreviations",
        "all caps is flagged as a possible abbreviation; abbreviations take lowercase suffixes (§55)",
        (
            "БИШКЕК",
            Word("БИШКЕК", abbreviation=False),
            Word("БУУ", abbreviation=True, pronunciation="буу"),
            Word("КТР", abbreviation=True, pronunciation="катээр"),
            Word("УАК", abbreviation=True),
        ),
    ),
    Group(
        "refused input",
        "the library raises instead of guessing",
        ("КТР", "Alibek", "Кара--Балта"),
    ),
)

SHOWN_CASES = (Case.GENITIVE, Case.DATIVE, Case.ACCUSATIVE, Case.LOCATIVE, Case.ABLATIVE)


def print_table(rows: Sequence[Sequence[str]], indent: str = "   ") -> None:
    widths = [max(len(row[i]) for row in rows if i < len(row)) for i in range(max(map(len, rows)))]
    for row in rows:
        cells = (cell.ljust(width) for cell, width in zip(row, widths, strict=False))
        print(indent + "  ".join(cells).rstrip())


def describe(word: str | Word) -> str:
    if isinstance(word, str):
        return word
    tag = {True: " [abbr]", False: " [not abbr]", None: ""}[word.abbreviation]
    return word.text + tag


def print_groups() -> None:
    header = ["word", *(case.kyrgyz_name.split()[0] for case in SHOWN_CASES), "flags"]
    for group in GROUPS:
        print(f"\n## {group.title}\n   ({group.why})\n")
        rows: list[list[str]] = [header]
        errors: list[str] = []
        for word in group.words:
            label = describe(word)
            try:
                results = [inflect_detailed(word, case=case) for case in SHOWN_CASES]
            except KyrgyzError as error:
                errors.append(f"{label}: {type(error).__name__}: {error}")
                continue
            flags = sorted({u.value for result in results for u in result.uncertainties})
            rows.append([label, *(result.text for result in results), ", ".join(flags)])
        if len(rows) > 1:
            print_table(rows)
        for message in errors:
            print(f"   ✗ {message}")


# --- Part 2: sentences --------------------------------------------------------------------


class CaseFormatter(string.Formatter):
    """``str.format`` where a format spec names a case: ``"{city:dative}"``."""

    def format_field(self, value: Any, format_spec: str) -> Any:
        if format_spec:
            return inflect(value, case=Case(format_spec), strict=True)
        return super().format_field(value, format_spec)


@dataclass(frozen=True)
class Template:
    kyrgyz: str
    english: str
    slots: Mapping[str, str]
    """Slot name → vocabulary category."""


# Each filler is (Kyrgyz, English gloss).
VOCABULARY: Mapping[str, tuple[tuple[str, str], ...]] = {
    "person": tuple(
        (name, name)
        for name in (
            "Алибек",
            "Айгүл",
            "Бекзат",
            "Нурбек",
            "Азамат",
            "Эрмек",
            "Жамийла",
            "Өмүр",
            "Айбек",
            "Сезим",
            "Улан",
            "Гүлнара",
        )
    ),
    "city": tuple(
        (city, city)
        for city in (
            "Бишкек",
            "Ош",
            "Каракол",
            "Нарын",
            "Талас",
            "Токмок",
            "Баткен",
            "Жалал-Абад",
            "Балыкчы",
            "Чолпон-Ата",
            "Өзгөн",
            "Кара-Балта",
        )
    ),
    "venue": (
        ("мектеп", "the school"),
        ("вокзал", "the station"),
        ("аэропорт", "the airport"),
        ("базар", "the bazaar"),
        ("китепкана", "the library"),
        ("парк", "the park"),
    ),
    "thing": (
        ("китеп", "the book"),
        ("белек", "the gift"),
        ("гүл", "the flower"),
        ("ачкыч", "the key"),
        ("кат", "the letter"),
    ),
    "occupation": (
        ("мугалим", "the teacher"),
        ("дарыгер", "the doctor"),
        ("коңшу", "the neighbour"),
        ("тренер", "the coach"),
        ("айдоочу", "the driver"),
    ),
    "pronoun": (
        ("мен", "me"),
        ("сен", "you"),
        ("ал", "him/her"),
        ("биз", "us"),
        ("сиз", "you (formal)"),
        ("силер", "you (plural)"),
        ("алар", "them"),
    ),
    "amount": tuple((amount, amount) for amount in ("500", "1 200", "3 000", "15 000")),
}

TEMPLATES = (
    Template("{a} {city:dative} барды.", "{a} went to {city}.", {"a": "person", "city": "city"}),
    Template("{a} {city:ablative} келди.", "{a} came from {city}.", {"a": "person", "city": "city"}),
    Template("{a} {city:locative} жашайт.", "{a} lives in {city}.", {"a": "person", "city": "city"}),
    Template(
        "{a:genitive} үйү {city:locative}.",
        "{a}'s house is in {city}.",
        {"a": "person", "city": "city"},
    ),
    Template(
        "{a} {src:ablative} {dst:dative} учуп кетти.",
        "{a} flew from {src} to {dst}.",
        {"a": "person", "src": "city", "dst": "city"},
    ),
    Template(
        "Посылка {src:ablative} {dst:dative} жөнөтүлдү.",
        "The parcel was sent from {src} to {dst}.",
        {"src": "city", "dst": "city"},
    ),
    Template(
        "{a} {b:accusative} {city:dative} чакырды.",
        "{a} invited {b} to {city}.",
        {"a": "person", "b": "person", "city": "city"},
    ),
    Template(
        "{a} {b:dative} {thing:accusative} берди.",
        "{a} gave {thing} to {b}.",
        {"a": "person", "b": "person", "thing": "thing"},
    ),
    Template(
        "{a} {venue:locative} {b:accusative} күттү.",
        "{a} waited for {b} at {venue}.",
        {"a": "person", "b": "person", "venue": "venue"},
    ),
    Template(
        "{a} эртең {venue:dative} барат.",
        "{a} will go to {venue} tomorrow.",
        {"a": "person", "venue": "venue"},
    ),
    Template(
        "{a} {venue:ablative} {thing:accusative} алып келди.",
        "{a} brought {thing} from {venue}.",
        {"a": "person", "venue": "venue", "thing": "thing"},
    ),
    Template(
        "{a} {job:ablative} кеңеш сурады.",
        "{a} asked {job} for advice.",
        {"a": "person", "job": "occupation"},
    ),
    Template("{a} {p:dative} кат жазды.", "{a} wrote a letter to {p}.", {"a": "person", "p": "pronoun"}),
    Template("{a} {p:accusative} жакшы көрөт.", "{a} loves {p}.", {"a": "person", "p": "pronoun"}),
    Template(
        "{sum} сом {a:dative} которулду.",
        "{sum} som was transferred to {a}.",
        {"sum": "amount", "a": "person"},
    ),
)


def fill(template: Template, rng: random.Random) -> tuple[str, str]:
    """Return one (Kyrgyz, English) sentence; slots of one category get distinct fillers."""
    by_category: dict[str, list[str]] = {}
    for slot, category in template.slots.items():
        by_category.setdefault(category, []).append(slot)

    kyrgyz_values: dict[str, str] = {}
    english_values: dict[str, str] = {}
    for category, slots in by_category.items():
        for slot, (kyrgyz, english) in zip(slots, rng.sample(VOCABULARY[category], len(slots)), strict=True):
            kyrgyz_values[slot] = kyrgyz
            english_values[slot] = english

    sentence = CaseFormatter().format(template.kyrgyz, **kyrgyz_values)
    return sentence[:1].upper() + sentence[1:], template.english.format(**english_values)


def print_sentences(per_template: int, seed: int) -> None:
    rng = random.Random(seed)
    for template in TEMPLATES:
        print(f"\n   {template.kyrgyz}")
        for _ in range(per_template):
            kyrgyz, english = fill(template, rng)
            print(f"     • {kyrgyz:<48} {english}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Show complex Kyrgyz inflections and generated sentences.")
    parser.add_argument("--per-template", type=int, default=2, help="sentences per template (default 2)")
    parser.add_argument("--seed", type=int, default=0, help="random seed for word selection (default 0)")
    args = parser.parse_args()

    print("# Part 1: complex words")
    print_groups()
    print("\n# Part 2: generated sentences")
    print_sentences(args.per_template, args.seed)


if __name__ == "__main__":
    main()
