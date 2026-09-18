from __future__ import annotations

import pytest

from kyrgyz import AmbiguousWordError, Uncertainty
from kyrgyz.phonology.alphabet import VOICED_CONSONANTS, VOICELESS_CONSONANTS, VOWEL_LETTERS
from kyrgyz.phonology.analysis import analyze, last_word
from kyrgyz.phonology.consonants import Ending
from kyrgyz.phonology.transformations import prepare_stem


@pytest.mark.parametrize(
    ("text", "last_vowel", "final", "ending"),
    [
        ("апа", "а", "а", Ending.VOWEL),
        ("Алибек", "е", "к", Ending.VOICELESS_CONSONANT),
        ("үй", "ү", "й", Ending.VOICED_CONSONANT),
        ("ТАҢ", "а", "ң", Ending.VOICED_CONSONANT),
        ("Азия", "а", "я", Ending.VOWEL),  # я is read as its vowel а
        ("бюро", "о", "о", Ending.VOWEL),
        ("поэт", "е", "т", Ending.VOICELESS_CONSONANT),
        ("Ысык-Көл", "ө", "л", Ending.VOICED_CONSONANT),
        ("Алибек Асанов", "о", "в", Ending.VOICED_CONSONANT),
    ],
)
def test_analyze(text: str, last_vowel: str, final: str, ending: Ending) -> None:
    profile = analyze(text)
    assert profile.last_vowel is VOWEL_LETTERS[last_vowel]
    assert profile.final_letter == final
    assert profile.ending is ending


@pytest.mark.parametrize("letter", sorted(VOICED_CONSONANTS))
def test_every_voiced_consonant_is_classified_voiced(letter: str) -> None:
    assert analyze("а" + letter).ending is Ending.VOICED_CONSONANT


@pytest.mark.parametrize("letter", sorted(VOICELESS_CONSONANTS))
def test_every_voiceless_consonant_is_classified_voiceless(letter: str) -> None:
    assert analyze("а" + letter).ending is Ending.VOICELESS_CONSONANT


@pytest.mark.parametrize("letter", sorted(VOWEL_LETTERS))
def test_every_vowel_letter_is_classified_vowel(letter: str) -> None:
    assert analyze("б" + letter).ending is Ending.VOWEL


def test_last_word_splits_on_hyphens_and_spaces() -> None:
    assert last_word("Чолпон-Ата") == "Ата"
    assert last_word("Алибек Асанов") == "Асанов"


@pytest.mark.parametrize("text", ["КТР", "ж", "Алибек Ж", "Ысык-Ж"])
def test_word_without_vowel_is_ambiguous(text: str) -> None:
    with pytest.raises(AmbiguousWordError, match="no vowel"):
        analyze(text)


def test_profile_after_tracks_vowels_and_final_letter() -> None:
    profile = analyze("кол").after("д").after("у")
    assert profile.final_letter == "у"
    assert profile.last_vowel is VOWEL_LETTERS["у"]
    assert profile.ending is Ending.VOWEL


def test_prepare_stem_drops_final_soft_sign_preserving_case() -> None:
    assert prepare_stem("МЕДАЛЬ").text == "МЕДАЛ"
    assert prepare_stem("медаль").uncertainties == {Uncertainty.SOFT_SIGN_DROPPED}
    assert prepare_stem("кол").text == "кол"
    assert not prepare_stem("кол").uncertainties


def test_prepare_stem_rejects_final_hard_sign() -> None:
    with pytest.raises(AmbiguousWordError, match="ъ"):
        prepare_stem("съезъ")
