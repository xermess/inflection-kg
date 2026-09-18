"""Grammatical cases (жөндөмөлөр) of Kyrgyz.

Kyrgyz has six cases. The linguistic names are canonical; a few English
prepositional aliases are provided for readability at call sites::

    from kyrgyz.cases import DATIVE, TO   # TO is DATIVE

There is deliberately no alias for the accusative, which has no English
preposition equivalent.
"""

from __future__ import annotations

from enum import Enum


class Case(Enum):
    """A Kyrgyz grammatical case."""

    NOMINATIVE = "nominative"
    GENITIVE = "genitive"
    DATIVE = "dative"
    ACCUSATIVE = "accusative"
    LOCATIVE = "locative"
    ABLATIVE = "ablative"

    @property
    def kyrgyz_name(self) -> str:
        """The traditional Kyrgyz grammatical term, e.g. ``"Барыш жөндөмө"``."""
        return _KYRGYZ_NAMES[self]


_KYRGYZ_NAMES = {
    Case.NOMINATIVE: "Атооч жөндөмө",
    Case.GENITIVE: "Илик жөндөмө",
    Case.DATIVE: "Барыш жөндөмө",
    Case.ACCUSATIVE: "Табыш жөндөмө",
    Case.LOCATIVE: "Жатыш жөндөмө",
    Case.ABLATIVE: "Чыгыш жөндөмө",
}

NOMINATIVE = Case.NOMINATIVE
GENITIVE = Case.GENITIVE
DATIVE = Case.DATIVE
ACCUSATIVE = Case.ACCUSATIVE
LOCATIVE = Case.LOCATIVE
ABLATIVE = Case.ABLATIVE

# Readability aliases. They are the same objects as the canonical constants.
TO = DATIVE
FROM = ABLATIVE
IN = LOCATIVE
OF = GENITIVE

__all__ = [
    "ABLATIVE",
    "ACCUSATIVE",
    "DATIVE",
    "FROM",
    "GENITIVE",
    "IN",
    "LOCATIVE",
    "NOMINATIVE",
    "OF",
    "TO",
    "Case",
]
