from __future__ import annotations

import pytest

from kyrgyz.phonology.alphabet import VOWEL_LETTERS, VOWEL_PHONEMES
from kyrgyz.phonology.harmony import high_vowel, low_vowel

# The complete harmony table: last stem vowel letter → (A, I).
HARMONY_TABLE = {
    "а": ("а", "ы"),
    "ы": ("а", "ы"),
    "я": ("а", "ы"),
    "о": ("о", "у"),
    "ё": ("о", "у"),
    "у": ("а", "у"),  # the у → а asymmetry
    "ю": ("а", "у"),
    "е": ("е", "и"),
    "э": ("е", "и"),
    "и": ("е", "и"),
    "ө": ("ө", "ү"),
    "ү": ("ө", "ү"),
}


def test_table_covers_every_vowel_letter() -> None:
    assert set(HARMONY_TABLE) == set(VOWEL_LETTERS)


@pytest.mark.parametrize(("letter", "expected"), HARMONY_TABLE.items())
def test_low_vowel(letter: str, expected: tuple[str, str]) -> None:
    assert low_vowel(VOWEL_LETTERS[letter]) == expected[0]


@pytest.mark.parametrize(("letter", "expected"), HARMONY_TABLE.items())
def test_high_vowel(letter: str, expected: tuple[str, str]) -> None:
    assert high_vowel(VOWEL_LETTERS[letter]) == expected[1]


@pytest.mark.parametrize("vowel", VOWEL_PHONEMES, ids=lambda v: v.letter)
def test_suffix_vowels_agree_in_backness(vowel) -> None:  # type: ignore[no-untyped-def]
    assert VOWEL_LETTERS[low_vowel(vowel)].back == vowel.back
    assert VOWEL_LETTERS[high_vowel(vowel)].back == vowel.back


@pytest.mark.parametrize("vowel", VOWEL_PHONEMES, ids=lambda v: v.letter)
def test_high_suffix_vowel_copies_rounding(vowel) -> None:  # type: ignore[no-untyped-def]
    assert VOWEL_LETTERS[high_vowel(vowel)].rounded == vowel.rounded
