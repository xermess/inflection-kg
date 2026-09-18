"""Suffix templates written with archiphonemes, and their realisation.

Grammars describe Kyrgyz suffixes with archiphonemes, capital letters that
stand for a set of alternating sounds: the dative is ``-GA``, the genitive
``-NIн``. A :class:`SuffixTemplate` stores exactly that notation, and
:func:`realize` turns it into concrete letters for a given stem::

    >>> from kyrgyz.phonology import analyze
    >>> realize(SuffixTemplate("GA"), analyze("үй"))
    'гө'

Archiphonemes (uppercase Latin letters inside a template):

====  ==========================  =====================================
Code  Surface forms               Rule
====  ==========================  =====================================
A     а е о ө                     :func:`~kyrgyz.phonology.harmony.low_vowel`
I     ы и у ү                     :func:`~kyrgyz.phonology.harmony.high_vowel`
G     г к                         :func:`~kyrgyz.phonology.consonants.velar_onset`
D     д т                         :func:`~kyrgyz.phonology.consonants.dental_onset`
N     н д т                       :func:`~kyrgyz.phonology.consonants.nasal_onset`
====  ==========================  =====================================

Any other character of a template must be a lowercase Kyrgyz letter and is
copied unchanged (the ``н`` of ``-NIн``).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from types import MappingProxyType

from kyrgyz.phonology.alphabet import LETTERS
from kyrgyz.phonology.analysis import PhonologicalProfile
from kyrgyz.phonology.consonants import dental_onset, nasal_onset, velar_onset
from kyrgyz.phonology.harmony import high_vowel, low_vowel

_Resolver = Callable[[PhonologicalProfile], str]

ARCHIPHONEMES: MappingProxyType[str, _Resolver] = MappingProxyType(
    {
        "A": lambda profile: low_vowel(profile.last_vowel),
        "I": lambda profile: high_vowel(profile.last_vowel),
        "G": lambda profile: velar_onset(profile.ending),
        "D": lambda profile: dental_onset(profile.ending),
        "N": lambda profile: nasal_onset(profile.ending),
    }
)


@dataclass(frozen=True)
class SuffixTemplate:
    """An abstract suffix such as ``GA`` (dative) or ``DAн`` (ablative).

    The empty template is valid and denotes a zero suffix (the nominative).
    """

    pattern: str

    def __post_init__(self) -> None:
        for symbol in self.pattern:
            if symbol not in ARCHIPHONEMES and symbol not in LETTERS:
                raise ValueError(
                    f"invalid symbol {symbol!r} in suffix template {self.pattern!r}: "
                    f"expected one of {sorted(ARCHIPHONEMES)} or a lowercase Kyrgyz letter"
                )

    @property
    def is_empty(self) -> bool:
        """True for the zero suffix."""
        return not self.pattern

    def __str__(self) -> str:
        return f"-{self.pattern}" if self.pattern else "-∅"


def realize(template: SuffixTemplate, profile: PhonologicalProfile) -> str:
    """Spell out *template* after a stem with the given *profile*.

    Symbols are resolved left to right, and each resolved letter updates the
    profile, so a later archiphoneme harmonises with the suffix's own earlier
    letters rather than with the stem.
    """
    letters: list[str] = []
    for symbol in template.pattern:
        resolver = ARCHIPHONEMES.get(symbol)
        letter = resolver(profile) if resolver is not None else symbol
        letters.append(letter)
        profile = profile.after(letter)
    return "".join(letters)
