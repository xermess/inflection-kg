"""Uncertainty reporting, strict mode and abbreviations (orthographic rules §55)."""

from __future__ import annotations

import pytest

from kyrgyz import AmbiguousWordError, KyrgyzError, Uncertainty, Word, inflect, inflect_detailed
from kyrgyz.cases import DATIVE, GENITIVE, NOMINATIVE, Case


@pytest.mark.parametrize(
    ("word", "case", "expected"),
    [
        # §55: "БУУга, КУУнун, УАКтын, МАИнин, КТРдин"
        (Word("БУУ", abbreviation=True, pronunciation="буу"), DATIVE, "БУУга"),
        (Word("КУУ", abbreviation=True, pronunciation="куу"), GENITIVE, "КУУнун"),
        (Word("УАК", abbreviation=True, pronunciation="уак"), GENITIVE, "УАКтын"),
        (Word("МАИ", abbreviation=True, pronunciation="маи"), GENITIVE, "МАИнин"),
        (Word("КТР", abbreviation=True, pronunciation="катээр"), GENITIVE, "КТРдин"),
    ],
)
def test_orthographic_rules_section_55(word: Word, case: Case, expected: str) -> None:
    result = inflect_detailed(word, case=case, strict=True)
    assert result.text == expected
    assert result.is_certain


def test_abbreviation_without_pronunciation_is_read_as_a_word() -> None:
    result = inflect_detailed(Word("БУУ", abbreviation=True), case=DATIVE)
    assert result.text == "БУУга"
    assert result.uncertainties == {Uncertainty.ABBREVIATION_READING_ASSUMED}


def test_abbreviation_without_vowel_needs_a_pronunciation() -> None:
    with pytest.raises(AmbiguousWordError, match="pronunciation"):
        inflect(Word("КТР", abbreviation=True), case=GENITIVE)


@pytest.mark.parametrize("word", ["КТР", "ж", "Алибек Ж"])
def test_words_without_vowels_always_raise(word: str) -> None:
    with pytest.raises(AmbiguousWordError):
        inflect(word, case=DATIVE)


def test_all_caps_input_is_flagged_as_a_possible_abbreviation() -> None:
    result = inflect_detailed("БИШКЕК", case=DATIVE)
    assert result.text == "БИШКЕККЕ"
    assert result.uncertainties == {Uncertainty.POSSIBLE_ABBREVIATION}


def test_asserting_not_an_abbreviation_removes_the_flag() -> None:
    result = inflect_detailed(Word("БИШКЕК", abbreviation=False), case=DATIVE, strict=True)
    assert result.text == "БИШКЕККЕ"
    assert result.is_certain


@pytest.mark.parametrize(
    ("word", "uncertainty"),
    [
        ("БИШКЕК", Uncertainty.POSSIBLE_ABBREVIATION),
        ("медаль", Uncertainty.SOFT_SIGN_DROPPED),
        (Word("БУУ", abbreviation=True), Uncertainty.ABBREVIATION_READING_ASSUMED),
    ],
)
def test_strict_mode_raises_on_uncertain_results(word: str | Word, uncertainty: Uncertainty) -> None:
    with pytest.raises(AmbiguousWordError) as excinfo:
        inflect(word, case=DATIVE, strict=True)
    assert excinfo.value.uncertainties == {uncertainty}
    assert uncertainty.description in str(excinfo.value)


def test_strict_mode_accepts_certain_results() -> None:
    assert inflect("Алибек", case=DATIVE, strict=True) == "Алибекке"
    assert inflect("мен", case=DATIVE, strict=True) == "мага"


def test_nominative_is_never_uncertain() -> None:
    assert inflect("БИШКЕК", case=NOMINATIVE, strict=True) == "БИШКЕК"
    assert inflect("медаль", case=NOMINATIVE, strict=True) == "медаль"


def test_several_uncertainties_are_reported_together() -> None:
    result = inflect_detailed("МЕДАЛЬ", case=DATIVE)
    assert result.text == "МЕДАЛГА"
    assert result.uncertainties == {Uncertainty.POSSIBLE_ABBREVIATION, Uncertainty.SOFT_SIGN_DROPPED}


def test_errors_share_a_base_class() -> None:
    assert issubclass(AmbiguousWordError, KyrgyzError)
    with pytest.raises(KyrgyzError):
        inflect("КТР", case=DATIVE)


def test_every_uncertainty_has_a_description() -> None:
    assert all(u.description for u in Uncertainty)
