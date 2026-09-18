"""The modern Kyrgyz Cyrillic alphabet and the phonological features of its letters.

All sets and mappings here use lowercase letters. The alphabet has 36 letters:
12 vowel letters, 22 consonant letters and 2 signs (ь, ъ).

Vowels
------
Kyrgyz has eight vowel phonemes, classified by three binary features::

                 unrounded        rounded
                 low   high       low   high
    back         а     ы          о     у
    front        е     и          ө     ү

The remaining vowel letters are orthographic variants that behave like one of
these eight for vowel harmony: ``э`` = е, ``я`` = [j]+а, ``ё`` = [j]+о,
``ю`` = [j]+у (Apertium-kir ``twol`` harmony tables; Абдувалиев, *Кыргыз
тилинин морфологиясы*: "кыргыз тилинде э жана е тамгалары бир эле тыбышты
билдирет").

Consonants
----------
For suffix selection only one distinction matters: whether a consonant is
voiceless (каткалаң) or not. Voiced obstruents (уяң) and sonorants (жумшак)
pattern together, including ``й`` and ``р``.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class Vowel:
    """One of the eight Kyrgyz vowel phonemes, written with its canonical letter."""

    letter: str
    back: bool
    rounded: bool
    high: bool


VOWEL_PHONEMES: tuple[Vowel, ...] = (
    Vowel("а", back=True, rounded=False, high=False),
    Vowel("ы", back=True, rounded=False, high=True),
    Vowel("о", back=True, rounded=True, high=False),
    Vowel("у", back=True, rounded=True, high=True),
    Vowel("е", back=False, rounded=False, high=False),
    Vowel("и", back=False, rounded=False, high=True),
    Vowel("ө", back=False, rounded=True, high=False),
    Vowel("ү", back=False, rounded=True, high=True),
)

_PHONEME_BY_LETTER = {vowel.letter: vowel for vowel in VOWEL_PHONEMES}

VOWEL_LETTERS: MappingProxyType[str, Vowel] = MappingProxyType(
    {
        **_PHONEME_BY_LETTER,
        "э": _PHONEME_BY_LETTER["е"],
        "я": _PHONEME_BY_LETTER["а"],
        "ё": _PHONEME_BY_LETTER["о"],
        "ю": _PHONEME_BY_LETTER["у"],
    }
)
"""Every vowel letter mapped to the phoneme that governs its harmony."""

VOICED_CONSONANTS: frozenset[str] = frozenset("бвгджзйлмнңр")
VOICELESS_CONSONANTS: frozenset[str] = frozenset("кпстфхцчшщ")
CONSONANTS: frozenset[str] = VOICED_CONSONANTS | VOICELESS_CONSONANTS

SOFT_SIGN = "ь"
HARD_SIGN = "ъ"
SIGNS: frozenset[str] = frozenset({SOFT_SIGN, HARD_SIGN})

LETTERS: frozenset[str] = frozenset(VOWEL_LETTERS) | CONSONANTS | SIGNS
"""All 36 lowercase letters of the Kyrgyz Cyrillic alphabet."""


def is_vowel(letter: str) -> bool:
    """Return True if *letter* (lowercase) is a vowel letter."""
    return letter in VOWEL_LETTERS


def is_voiceless(letter: str) -> bool:
    """Return True if *letter* (lowercase) is a voiceless consonant."""
    return letter in VOICELESS_CONSONANTS
