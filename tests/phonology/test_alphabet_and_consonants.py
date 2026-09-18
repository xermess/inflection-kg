from __future__ import annotations

import pytest

from kyrgyz.phonology.alphabet import (
    CONSONANTS,
    LETTERS,
    SIGNS,
    VOICED_CONSONANTS,
    VOICELESS_CONSONANTS,
    VOWEL_LETTERS,
)
from kyrgyz.phonology.consonants import Ending, dental_onset, nasal_onset, velar_onset

KYRGYZ_ALPHABET = "абвгдеёжзийклмнңоөпрстуүфхцчшщъыьэюя"


def test_alphabet_has_the_36_kyrgyz_letters() -> None:
    assert len(KYRGYZ_ALPHABET) == 36
    assert frozenset(KYRGYZ_ALPHABET) == LETTERS


def test_letter_classes_partition_the_alphabet() -> None:
    classes = [frozenset(VOWEL_LETTERS), VOICED_CONSONANTS, VOICELESS_CONSONANTS, SIGNS]
    assert sum(len(c) for c in classes) == len(LETTERS)
    assert frozenset().union(*classes) == LETTERS
    assert VOICED_CONSONANTS | VOICELESS_CONSONANTS == CONSONANTS


@pytest.mark.parametrize("letter", "өүң")
def test_kyrgyz_specific_letters_are_single_code_points(letter: str) -> None:
    assert len(letter) == 1
    assert letter in LETTERS


@pytest.mark.parametrize(
    ("ending", "g", "d", "n"),
    [
        (Ending.VOWEL, "г", "д", "н"),
        (Ending.VOICED_CONSONANT, "г", "д", "д"),
        (Ending.VOICELESS_CONSONANT, "к", "т", "т"),
    ],
)
def test_onset_table(ending: Ending, g: str, d: str, n: str) -> None:
    assert (velar_onset(ending), dental_onset(ending), nasal_onset(ending)) == (g, d, n)
