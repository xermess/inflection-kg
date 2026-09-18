"""Vowel harmony (үндөштүк): choosing a suffix vowel from the preceding vowel.

Kyrgyz suffix vowels come in two archiphonemes:

* ``A`` - a low vowel: а / е / о / ө
* ``I`` - a high vowel: ы / и / у / ү

Both agree in backness with the last vowel of the stem. They differ in
rounding:

* ``I`` is rounded after any rounded vowel (о, у, ө, ү).
* ``A`` is rounded after о and after the front rounded vowels ө, ү, but
  **not** after у: ``туз`` → ``тузга``, ``кум`` → ``кумга``, while
  ``кол`` → ``колго``, ``үй`` → ``үйгө``.

Resulting table (last stem vowel → A / I)::

    а ы у (я ю)  → а / ы (у after о, у)
    о (ё)        → о / у
    е и (э)      → е / и
    ө ү          → ө / ү

Sources: Абдувалиев И., *Кыргыз тилинин морфологиясы*, case chapters
("а, ы, у → а; о → о; э, е, и → е; ө, ү → ө"); Apertium-kir ``twol`` rule
"Vowel harmony for archiphoneme {A}"; Kara (2003) paradigm ``туз`` → ``тузга``.
"""

from __future__ import annotations

from kyrgyz.phonology.alphabet import Vowel


def low_vowel(after: Vowel) -> str:
    """Realise the low archiphoneme ``A`` after the vowel *after*."""
    if after.back:
        return "о" if after.rounded and not after.high else "а"
    return "ө" if after.rounded else "е"


def high_vowel(after: Vowel) -> str:
    """Realise the high archiphoneme ``I`` after the vowel *after*."""
    if after.back:
        return "у" if after.rounded else "ы"
    return "ү" if after.rounded else "и"
