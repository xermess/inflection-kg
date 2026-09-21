"""Input words: validation, Unicode normalisation and optional metadata."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from kyrgyz.errors import InvalidWordError
from kyrgyz.numbers import is_numeric
from kyrgyz.phonology.alphabet import LETTERS, SIGNS

_LOWER = "".join(sorted(LETTERS))
_ALLOWED_LETTERS = frozenset(LETTERS | {letter.upper() for letter in LETTERS})
_SEPARATORS = frozenset("- ")
# One or more words of Kyrgyz letters, joined by a single hyphen or space.
_WELL_FORMED = re.compile(rf"[{_LOWER}{_LOWER.upper()}]+(?:[- ][{_LOWER}{_LOWER.upper()}]+)*")


def normalize_text(value: object, *, what: str = "word") -> str:
    """Validate a Kyrgyz Cyrillic string and return it in Unicode NFC form.

    NFC composition matters for letters that can arrive decomposed, such as
    ``й`` (и + U+0306) and ``ё`` (е + U+0308). The letters ``ң``, ``ө`` and
    ``ү`` have no decomposition and pass through unchanged.

    Raises:
        TypeError: if *value* is not a ``str``.
        InvalidWordError: if *value* is empty or contains anything other than
            Kyrgyz letters separated by single hyphens or spaces.
    """
    if not isinstance(value, str):
        raise TypeError(f"{what} must be a str, got {type(value).__name__}")
    text = unicodedata.normalize("NFC", value)
    if not text:
        raise InvalidWordError(f"{what} must not be empty")
    if is_numeric(text):
        return text
    for char in text:
        if char not in _ALLOWED_LETTERS and char not in _SEPARATORS:
            raise InvalidWordError(f"{what} {value!r} contains {_describe(char)}")
    if not _WELL_FORMED.fullmatch(text):
        raise InvalidWordError(
            f"{what} {value!r} is malformed: hyphens and spaces may only appear singly, between letters"
        )
    return text


def _describe(char: str) -> str:
    name = unicodedata.name(char, "UNNAMED CHARACTER")
    description = f"unsupported character {char!r} (U+{ord(char):04X} {name})"
    if name.startswith("LATIN"):
        return f"{description}; Latin letters are not supported (check for look-alikes of Cyrillic letters)"
    if name.startswith("CYRILLIC"):
        return description + "; it is not a letter of the Kyrgyz alphabet"
    if char.isdigit():
        return description + "; only standalone integer numerals are supported"
    return description


@dataclass(frozen=True)
class Word:
    """A word to inflect, with optional metadata that refines its analysis.

    Plain strings passed to :func:`kyrgyz.inflect` are converted with
    ``Word(text)``; construct a ``Word`` yourself to supply metadata.

    Attributes:
        text: The word as written. It is validated and NFC-normalised.
            Multi-word names are allowed; the suffix attaches to the last word.
        proper: Whether the word is a proper noun. Currently informational:
            the orthographic rules attach case suffixes to proper nouns
            exactly as to common nouns (§32: ``Калининградда``, ``Алиевдин``).
        abbreviation: ``True`` for an initialism such as ``БУУ``, ``False`` to
            assert an all-caps word is *not* one, ``None`` (default) if unknown.
            Abbreviations take lowercase suffixes (orthographic rules §55).
        pronunciation: Optional Cyrillic respelling of how the word is read,
            used instead of ``text`` to choose the suffix. Needed for
            abbreviations read letter by letter: ``Word("КТР",
            abbreviation=True, pronunciation="катээр")`` → ``КТРдин``.
    """

    text: str
    proper: bool = False
    abbreviation: bool | None = None
    pronunciation: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "text", normalize_text(self.text))
        if self.pronunciation is not None:
            pronunciation = normalize_text(self.pronunciation, what="pronunciation").lower()
            if pronunciation[-1] in SIGNS:
                raise InvalidWordError(
                    f"pronunciation {self.pronunciation!r} must end in a vowel or consonant letter"
                )
            object.__setattr__(self, "pronunciation", pronunciation)

    @property
    def is_numeric(self) -> bool:
        """Whether this word is a supported numeric value."""
        return is_numeric(self.text)

    @classmethod
    def coerce(cls, value: str | Word) -> Word:
        """Return *value* unchanged if it is a ``Word``, otherwise ``Word(value)``."""
        return value if isinstance(value, Word) else cls(value)
