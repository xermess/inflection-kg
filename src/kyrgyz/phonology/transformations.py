"""Changes to the stem itself when a suffix is attached.

Phase 1 needs only one such change, because every case suffix on a bare noun
begins with a consonant:

* A word-final soft sign ``ь`` (found only in Russian loanwords) is dropped:
  ``медаль`` → ``медалга``, ``автомобиль`` → ``автомобилдин``. The form
  ``автомобилдин`` is cited in Абдувалиев, *Кыргыз тилинин морфологиясы*, and
  the Apertium-kir ``twol`` rule "Soft sign deletion before suffix" encodes
  the same behaviour. Because the orthographic rules do not codify it, the
  result carries :attr:`Uncertainty.SOFT_SIGN_DROPPED`.

Future phases add alternations triggered by vowel-initial suffixes, such as
intervocalic voicing ``к → г`` and ``п → б`` (``китеп`` → ``китеби``,
orthographic rules §33).
"""

from __future__ import annotations

from dataclasses import dataclass

from kyrgyz.diagnostics import Uncertainty
from kyrgyz.errors import AmbiguousWordError
from kyrgyz.phonology.alphabet import HARD_SIGN, SOFT_SIGN


@dataclass(frozen=True)
class PreparedStem:
    """A stem ready to receive a suffix, plus any assumptions made on the way."""

    text: str
    uncertainties: frozenset[Uncertainty] = frozenset()


def prepare_stem(stem: str) -> PreparedStem:
    """Apply stem-final changes required before attaching a consonant-initial suffix.

    Letter case is preserved; ``МЕДАЛЬ`` becomes ``МЕДАЛ``.

    Raises:
        AmbiguousWordError: if the stem ends in ``ъ``, for which no suffixation
            rule is documented.
    """
    final = stem[-1].lower()
    if final == SOFT_SIGN:
        return PreparedStem(stem[:-1], frozenset({Uncertainty.SOFT_SIGN_DROPPED}))
    if final == HARD_SIGN:
        raise AmbiguousWordError(
            f"Cannot inflect {stem!r}: no documented rule attaches suffixes after a final 'ъ'."
        )
    return PreparedStem(stem)
