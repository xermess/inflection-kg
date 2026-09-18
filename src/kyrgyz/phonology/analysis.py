"""Phonological analysis of a stem: the facts that suffix selection depends on.

A case suffix needs exactly two facts about its host:

1. the **last vowel** (for vowel harmony), and
2. the **final letter** (for assimilation of the suffix-initial consonant).

Both are read from the *last word* of the input. In Kyrgyz a case suffix
attaches to the end of the noun phrase, so in ``Ысык-Көл`` or
``Алибек Асанов`` only ``Көл`` / ``Асанов`` matter.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from kyrgyz.errors import AmbiguousWordError
from kyrgyz.phonology.alphabet import CONSONANTS, VOWEL_LETTERS, Vowel, is_voiceless
from kyrgyz.phonology.consonants import Ending

_WORD_SEPARATORS = re.compile(r"[\s-]+")


@dataclass(frozen=True)
class PhonologicalProfile:
    """The phonological state at the right edge of a (partial) word form."""

    last_vowel: Vowel
    final_letter: str

    @property
    def ending(self) -> Ending:
        """Whether the form ends in a vowel, voiced or voiceless consonant."""
        if self.final_letter in VOWEL_LETTERS:
            return Ending.VOWEL
        if is_voiceless(self.final_letter):
            return Ending.VOICELESS_CONSONANT
        return Ending.VOICED_CONSONANT

    def after(self, letter: str) -> PhonologicalProfile:
        """Return the profile of this form extended by one lowercase *letter*.

        This lets a suffix be realised left to right, and lets suffixes be
        chained (e.g. plural then case) without re-reading the whole word.
        """
        vowel = VOWEL_LETTERS.get(letter)
        return PhonologicalProfile(
            last_vowel=vowel if vowel is not None else self.last_vowel,
            final_letter=letter,
        )


def last_word(text: str) -> str:
    """Return the last space- or hyphen-separated word of *text*."""
    return _WORD_SEPARATORS.split(text.strip())[-1]


def analyze(text: str) -> PhonologicalProfile:
    """Compute the :class:`PhonologicalProfile` of a validated stem.

    *text* must already be a validated Kyrgyz word whose final letter is a
    vowel or consonant (a final ``ь``/``ъ`` must have been handled by
    :mod:`kyrgyz.phonology.transformations`).

    Raises:
        AmbiguousWordError: if the last word contains no vowel letter, so its
            vowel harmony cannot be determined from spelling (e.g. ``КТР``).
    """
    word = last_word(text).lower()
    final_letter = word[-1]
    if final_letter not in VOWEL_LETTERS and final_letter not in CONSONANTS:
        raise ValueError(f"stem {text!r} must end in a vowel or consonant letter")

    for letter in reversed(word):
        vowel = VOWEL_LETTERS.get(letter)
        if vowel is not None:
            return PhonologicalProfile(last_vowel=vowel, final_letter=final_letter)

    raise AmbiguousWordError(
        f"Cannot determine vowel harmony for {text!r}: {word!r} contains no vowel "
        "letter. If it is an abbreviation read letter by letter, pass "
        "Word(text, abbreviation=True, pronunciation=...) with its spoken form."
    )
