"""Lexically listed forms that override the general rules.

A :class:`Lexicon` is immutable. "Registering" an exception returns a new
lexicon, which you then pass to an :class:`~kyrgyz.inflector.Inflector`::

    lexicon = Lexicon.default().with_exception("Бишкек", case=DATIVE, form="Бишкекке")
    inflector = Inflector(lexicon=lexicon)

Only add an entry when the rules genuinely do not apply (suppletion,
irregular stems, established spellings), and record the source. Entries
are matched on the whole input, case-insensitively, after NFC normalisation.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from types import MappingProxyType

from kyrgyz.cases import Case
from kyrgyz.features import Features
from kyrgyz.word import normalize_text


@dataclass(frozen=True)
class LexicalEntry:
    """One listed form: *lemma* inflected for *features* is *form*.

    ``lemma`` and ``form`` are validated and stored in lowercase; output is
    re-cased to match the input word.
    """

    lemma: str
    features: Features
    form: str
    source: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "lemma", normalize_text(self.lemma, what="lemma").lower())
        object.__setattr__(self, "form", normalize_text(self.form, what="form").lower())
        if not isinstance(self.features, Features):
            raise TypeError(f"features must be Features, got {type(self.features).__name__}")


class Lexicon:
    """An immutable collection of :class:`LexicalEntry` objects."""

    __slots__ = ("_entries",)

    def __init__(self, entries: Iterable[LexicalEntry] = ()) -> None:
        table: dict[tuple[str, Features], LexicalEntry] = {}
        for entry in entries:
            table[(entry.lemma, entry.features)] = entry
        self._entries: MappingProxyType[tuple[str, Features], LexicalEntry] = MappingProxyType(table)

    @classmethod
    def default(cls) -> Lexicon:
        """The built-in lexicon: irregular personal pronouns (see :mod:`.pronouns`)."""
        from kyrgyz.lexicon.pronouns import PERSONAL_PRONOUNS

        return cls(PERSONAL_PRONOUNS)

    @classmethod
    def empty(cls) -> Lexicon:
        """A lexicon with no entries: every word is inflected by rule."""
        return cls()

    def lookup(self, lemma: str, features: Features) -> LexicalEntry | None:
        """Return the entry for *lemma* (any letter case) and *features*, if listed."""
        return self._entries.get((normalize_text(lemma, what="lemma").lower(), features))

    def with_entry(self, entry: LexicalEntry) -> Lexicon:
        """Return a new lexicon with *entry* added, replacing any entry for the same key."""
        return Lexicon([*self._entries.values(), entry])

    def with_exception(self, lemma: str, *, case: Case, form: str, source: str = "") -> Lexicon:
        """Return a new lexicon in which *lemma* in *case* is spelled *form*."""
        return self.with_entry(LexicalEntry(lemma, Features(case=case), form, source))

    def __iter__(self) -> Iterator[LexicalEntry]:
        return iter(self._entries.values())

    def __len__(self) -> int:
        return len(self._entries)

    def __repr__(self) -> str:
        return f"Lexicon({len(self)} entries)"
