"""Exception hierarchy for the ``kyrgyz`` package.

Every error raised deliberately by the library derives from :class:`KyrgyzError`,
so callers can catch the whole family with a single ``except`` clause.
"""

from __future__ import annotations

from collections.abc import Iterable

from kyrgyz.diagnostics import Uncertainty


class KyrgyzError(Exception):
    """Base class for all errors raised by this library."""


class InvalidWordError(KyrgyzError, ValueError):
    """The input is not a well-formed Kyrgyz Cyrillic word.

    Raised for empty strings, digits, punctuation, Latin look-alike letters,
    letters of other Cyrillic alphabets (e.g. Kazakh ``ұ``), malformed hyphens
    or spaces, and similar problems.
    """


class AmbiguousWordError(KyrgyzError):
    """The word cannot be inflected without guessing.

    Raised when the information needed to choose a suffix is missing (for
    example, a word with no vowel letter, whose vowel harmony is unknowable
    from its spelling), and in ``strict`` mode whenever the result depends on
    an assumption listed in :attr:`uncertainties`.
    """

    def __init__(self, message: str, uncertainties: Iterable[Uncertainty] = ()) -> None:
        super().__init__(message)
        self.uncertainties: frozenset[Uncertainty] = frozenset(uncertainties)
