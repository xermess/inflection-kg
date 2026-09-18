"""Diagnostics attached to inflection results.

An :class:`Uncertainty` marks a result that is the library's best reading of
the rules but rests on an assumption the spelling alone cannot confirm. The
default API still returns such results (and exposes the flags through
``inflect_detailed``); ``strict=True`` turns them into errors instead.
"""

from __future__ import annotations

from enum import Enum


class Uncertainty(Enum):
    """A reason why an inflected form may not be the intended one."""

    POSSIBLE_ABBREVIATION = "possible_abbreviation"
    """The input is written in capitals and may be an abbreviation.

    Orthographic rules §55 require suffixes on abbreviations to follow their
    *pronunciation* and to be written in lowercase (``БУУга``). An all-caps
    ordinary word (``БИШКЕК``) instead takes an all-caps suffix. Pass
    ``Word(text, abbreviation=True/False)`` to resolve this.
    """

    ABBREVIATION_READING_ASSUMED = "abbreviation_reading_assumed"
    """An abbreviation was analysed as if read as an ordinary word.

    Abbreviations may be read as a word (``БУУ`` [buu]) or letter by letter
    (``КТР`` [ka-te-er]). Supply ``Word(..., pronunciation=...)`` to remove
    the assumption.
    """

    SOFT_SIGN_DROPPED = "soft_sign_dropped"
    """A word-final ``ь`` was dropped before the suffix (``медаль`` → ``медалга``).

    This follows attested usage and the Apertium Kyrgyz transducer, but it is
    not stated in the orthographic rules, and harmony after palatalised
    consonants in loanwords can vary between speakers.
    """

    @property
    def description(self) -> str:
        """A one-line human-readable explanation."""
        return _DESCRIPTIONS[self]


_DESCRIPTIONS = {
    Uncertainty.POSSIBLE_ABBREVIATION: (
        "all-caps input may be an abbreviation, whose suffix should be lowercase "
        "and follow its pronunciation (orthographic rules §55)"
    ),
    Uncertainty.ABBREVIATION_READING_ASSUMED: (
        "abbreviation was read as an ordinary word; pass a pronunciation to confirm"
    ),
    Uncertainty.SOFT_SIGN_DROPPED: (
        "final soft sign was dropped and harmony taken from the last vowel letter; "
        "this is attested usage but not codified in the orthographic rules"
    ),
}
