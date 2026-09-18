from __future__ import annotations

import pytest

from kyrgyz import Inflector, InvalidWordError, LexicalEntry, Lexicon, Source, inflect, inflect_detailed
from kyrgyz.cases import ABLATIVE, ACCUSATIVE, DATIVE, GENITIVE, LOCATIVE, Case
from kyrgyz.features import Features

IRREGULAR_PRONOUNS = [
    ("мен", GENITIVE, "менин"),
    ("мен", DATIVE, "мага"),
    ("мен", ACCUSATIVE, "мени"),
    ("сен", GENITIVE, "сенин"),
    ("сен", DATIVE, "сага"),
    ("сен", ACCUSATIVE, "сени"),
    ("ал", GENITIVE, "анын"),
    ("ал", DATIVE, "ага"),
    ("ал", ACCUSATIVE, "аны"),
    ("ал", LOCATIVE, "анда"),
    ("ал", ABLATIVE, "андан"),
]

REGULAR_PRONOUNS = [
    ("мен", LOCATIVE, "менде"),
    ("мен", ABLATIVE, "менден"),
    ("сен", LOCATIVE, "сенде"),
    ("сиз", DATIVE, "сизге"),
    ("сиз", GENITIVE, "сиздин"),
    ("биз", DATIVE, "бизге"),
    ("биз", ACCUSATIVE, "бизди"),
    ("силер", DATIVE, "силерге"),
    ("сиздер", LOCATIVE, "сиздерде"),
    ("алар", DATIVE, "аларга"),
    ("алар", GENITIVE, "алардын"),
    ("алар", ABLATIVE, "алардан"),
]


@pytest.mark.parametrize(("lemma", "case", "expected"), IRREGULAR_PRONOUNS)
def test_irregular_pronouns_come_from_the_lexicon(lemma: str, case: Case, expected: str) -> None:
    result = inflect_detailed(lemma, case=case)
    assert result.text == expected
    assert result.source is Source.LEXICON


@pytest.mark.parametrize(("lemma", "case", "expected"), REGULAR_PRONOUNS)
def test_regular_pronoun_forms_are_derived_by_rule(lemma: str, case: Case, expected: str) -> None:
    result = inflect_detailed(lemma, case=case)
    assert result.text == expected
    assert result.source is Source.RULE


@pytest.mark.parametrize(("model", "expected"), [("мен", "мага"), ("Мен", "Мага"), ("МЕН", "МАГА")])
def test_lexicon_forms_follow_input_capitalisation(model: str, expected: str) -> None:
    assert inflect(model, case=DATIVE) == expected


def test_empty_lexicon_applies_rules_only() -> None:
    inflector = Inflector(lexicon=Lexicon.empty())
    assert inflector.inflect("ал", case=ABLATIVE) == "алдан"  # the noun ал "strength"


def test_with_exception_returns_a_new_lexicon() -> None:
    base = Lexicon.default()
    extended = base.with_exception("Бишкек", case=DATIVE, form="Бишкекке", source="test")
    assert len(extended) == len(base) + 1
    assert base.lookup("Бишкек", Features(case=DATIVE)) is None
    entry = extended.lookup("БИШКЕК", Features(case=DATIVE))
    assert entry is not None
    assert (entry.lemma, entry.form, entry.source) == ("бишкек", "бишкекке", "test")


def test_custom_exception_overrides_rules() -> None:
    lexicon = Lexicon.empty().with_exception("шаар", case=LOCATIVE, form="шаарда")
    result = Inflector(lexicon=lexicon).inflect_detailed("Шаар", case=LOCATIVE)
    assert result.text == "Шаарда"
    assert result.source is Source.LEXICON


def test_later_entry_replaces_earlier_one() -> None:
    lexicon = Lexicon.empty().with_exception("ал", case=DATIVE, form="алга")
    lexicon = lexicon.with_exception("ал", case=DATIVE, form="ага")
    assert len(lexicon) == 1
    assert Inflector(lexicon=lexicon).inflect("ал", case=DATIVE) == "ага"


def test_lexicon_is_iterable_and_matches_other_cases_by_rule() -> None:
    lexicon = Lexicon.default()
    assert {entry.lemma for entry in lexicon} == {"мен", "сен", "ал"}
    assert all(entry.source for entry in lexicon)
    assert repr(lexicon) == f"Lexicon({len(lexicon)} entries)"


@pytest.mark.parametrize(("lemma", "form"), [("Bishkek", "Бишкекке"), ("Бишкек", "Bishkekke"), ("", "а")])
def test_entries_are_validated(lemma: str, form: str) -> None:
    with pytest.raises(InvalidWordError):
        LexicalEntry(lemma, Features(case=DATIVE), form)


def test_entry_features_type_is_checked() -> None:
    with pytest.raises(TypeError):
        LexicalEntry("үй", DATIVE, "үйгө")  # type: ignore[arg-type]
