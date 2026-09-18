"""Kyrgyz phonology: letter features, vowel harmony, consonant assimilation.

This layer knows nothing about grammar. It answers questions such as "which
low vowel follows ``ү``?" or "does this stem end in a voiceless consonant?".
"""

from kyrgyz.phonology.alphabet import LETTERS, VOWEL_LETTERS, Vowel
from kyrgyz.phonology.analysis import PhonologicalProfile, analyze
from kyrgyz.phonology.consonants import Ending
from kyrgyz.phonology.harmony import high_vowel, low_vowel

__all__ = [
    "LETTERS",
    "VOWEL_LETTERS",
    "Ending",
    "PhonologicalProfile",
    "Vowel",
    "analyze",
    "high_vowel",
    "low_vowel",
]
