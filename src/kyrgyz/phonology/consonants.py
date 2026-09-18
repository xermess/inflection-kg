"""Assimilation of suffix-initial consonants to the end of the stem.

The first consonant of a case suffix depends on how the stem ends:

==========  ===========  =====================  ====================
archiphon.  after vowel  after voiced consonant  after voiceless
==========  ===========  =====================  ====================
``G``       г            г                      к
``D``       д            д                      т
``N``       н            д                      т
==========  ===========  =====================  ====================

"Voiced" covers both sonorants (й л м н ң р) and voiced obstruents
(б в г д ж з). Voiceless: к п с т ф х ц ч ш щ.

Classification follows the *written* final letter. For loanwords this matters
when a written voiced obstruent is pronounced voiceless: orthographic rules
§32 require ``педагогго`` (not ``педагогко``), ``Калининградда``,
``Гамбургга``, ``Алиевдин``.

Sources: Абдувалиев И., *Кыргыз тилинин морфологиясы* (tables "үндүү менен /
жумшак жана уяң үнсүздөр менен / каткалаң үнсүз менен аяктаган сөздөрдө");
Kara (2003) on /n/ desonorisation after all consonants including /j/
(``айды``, ``торду``); *Кыргыз тилинин жазуу эрежелери* §32.
"""

from __future__ import annotations

from enum import Enum


class Ending(Enum):
    """How a stem ends, as far as suffix-initial consonants are concerned."""

    VOWEL = "vowel"
    VOICED_CONSONANT = "voiced_consonant"
    VOICELESS_CONSONANT = "voiceless_consonant"


def velar_onset(ending: Ending) -> str:
    """Realise ``G`` (dative -GA): г, or к after a voiceless consonant."""
    return "к" if ending is Ending.VOICELESS_CONSONANT else "г"


def dental_onset(ending: Ending) -> str:
    """Realise ``D`` (locative -DA, ablative -DAн): д, or т after a voiceless consonant."""
    return "т" if ending is Ending.VOICELESS_CONSONANT else "д"


def nasal_onset(ending: Ending) -> str:
    """Realise ``N`` (genitive -NIн, accusative -NI): н / д / т."""
    if ending is Ending.VOWEL:
        return "н"
    return "т" if ending is Ending.VOICELESS_CONSONANT else "д"
