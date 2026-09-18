from __future__ import annotations

import pytest

from kyrgyz.cases import Case
from kyrgyz.morphology.case import CASE_SUFFIXES, case_suffix
from kyrgyz.morphology.noun import attach
from kyrgyz.morphology.suffix import SuffixTemplate, realize
from kyrgyz.phonology.analysis import analyze


def test_every_case_has_a_template() -> None:
    assert set(CASE_SUFFIXES) == set(Case)


@pytest.mark.parametrize(
    ("case", "pattern"),
    [
        (Case.NOMINATIVE, ""),
        (Case.GENITIVE, "NIн"),
        (Case.DATIVE, "GA"),
        (Case.ACCUSATIVE, "NI"),
        (Case.LOCATIVE, "DA"),
        (Case.ABLATIVE, "DAн"),
    ],
)
def test_case_templates_match_the_grammar_notation(case: Case, pattern: str) -> None:
    assert case_suffix(case).pattern == pattern


def test_template_str() -> None:
    assert str(SuffixTemplate("GA")) == "-GA"
    assert str(SuffixTemplate("")) == "-∅"


@pytest.mark.parametrize("pattern", ["X", "ga", "G-A", "G A", "GA1"])
def test_invalid_template_symbols_are_rejected(pattern: str) -> None:
    with pytest.raises(ValueError, match="invalid symbol"):
        SuffixTemplate(pattern)


@pytest.mark.parametrize(
    ("stem", "pattern", "expected"),
    [
        ("үй", "GA", "гө"),
        ("мектеп", "GA", "ке"),
        ("апа", "NIн", "нын"),
        ("кол", "DAн", "дон"),
    ],
)
def test_realize(stem: str, pattern: str, expected: str) -> None:
    assert realize(SuffixTemplate(pattern), analyze(stem)) == expected


def test_later_symbols_harmonise_with_earlier_suffix_letters() -> None:
    # A literal vowel inside a template becomes the new harmony trigger:
    # after "кол" + "ү", the archiphoneme A is realised as ө, not о.
    assert realize(SuffixTemplate("үDA"), analyze("кол")) == "үдө"


@pytest.mark.parametrize(
    ("stem", "expected"),
    [("үй", "үйдөгү"), ("Бишкек", "Бишкектеги"), ("тоо", "тоодогу"), ("шаар", "шаардагы")],
)
def test_suffixes_can_be_chained(stem: str, expected: str) -> None:
    # Locative -DA followed by the attributive -GI ("the one in ..."): the second
    # suffix is chosen from the output of the first.
    locative = attach(stem, case_suffix(Case.LOCATIVE))
    attributive = attach(locative.stem + locative.suffix, SuffixTemplate("GI"))
    assert attributive.stem + attributive.suffix == expected


def test_empty_template_skips_analysis() -> None:
    form = attach("КТР", SuffixTemplate(""))
    assert (form.stem, form.suffix, form.profile) == ("КТР", "", None)


def test_pronunciation_replaces_spelling_for_analysis() -> None:
    form = attach("КТР", SuffixTemplate("NIн"), pronunciation="катээр")
    assert form.suffix == "дин"
