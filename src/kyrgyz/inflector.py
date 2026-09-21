"""The public inflection pipeline.

::

    input ─► Word (validate, NFC) ─► Features
          ─► lexicon lookup ──────────────────────────────┐
          ─► prepare stem ─► phonological analysis        │
          ─► realise suffix template ─► letter case ──────┴─► InflectionResult

:class:`Inflector` holds configuration (currently the lexicon) and is
immutable. The module-level :func:`inflect` and :func:`inflect_detailed` use a
shared default instance.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from kyrgyz.cases import Case
from kyrgyz.casing import is_all_caps, match_case
from kyrgyz.diagnostics import Uncertainty
from kyrgyz.errors import AmbiguousWordError
from kyrgyz.features import Features
from kyrgyz.lexicon.lexicon import Lexicon
from kyrgyz.morphology.noun import inflect_noun
from kyrgyz.numbers import pronunciation
from kyrgyz.phonology.analysis import PhonologicalProfile, last_word
from kyrgyz.word import Word


class Source(Enum):
    """Where an inflected form came from."""

    RULE = "rule"
    LEXICON = "lexicon"


@dataclass(frozen=True)
class InflectionResult:
    """An inflected form together with how it was derived.

    Attributes:
        text: The inflected surface form, e.g. ``"Алибекке"``.
        word: The (validated) input word.
        features: The requested grammatical features.
        stem: The part of ``text`` before the suffix. It differs from
            ``word.text`` only if the stem was changed (``медаль`` → ``медал``).
        suffix: The suffix as written in ``text`` (empty for the nominative
            and for lexicon forms).
        source: Whether the form was derived by rule or listed in the lexicon.
        profile: The phonological analysis the suffix was chosen from, or
            ``None`` if no analysis was needed.
        uncertainties: Assumptions the result depends on; empty if none.
    """

    text: str
    word: Word
    features: Features
    stem: str
    suffix: str
    source: Source
    profile: PhonologicalProfile | None = None
    uncertainties: frozenset[Uncertainty] = frozenset()

    @property
    def is_certain(self) -> bool:
        """True if the result rests on no flagged assumption."""
        return not self.uncertainties

    def __str__(self) -> str:
        return self.text


class Inflector:
    """Inflects Kyrgyz words. Immutable; safe to share between threads."""

    __slots__ = ("_lexicon",)

    def __init__(self, lexicon: Lexicon | None = None) -> None:
        """Create an inflector.

        Args:
            lexicon: Listed forms that override the rules. Defaults to
                :meth:`Lexicon.default` (irregular personal pronouns). Pass
                ``Lexicon.empty()`` to apply rules only.
        """
        self._lexicon = lexicon if lexicon is not None else Lexicon.default()

    @property
    def lexicon(self) -> Lexicon:
        """The lexicon consulted before the rules."""
        return self._lexicon

    def inflect(self, word: str | Word, *, case: Case = Case.NOMINATIVE, strict: bool = False) -> str:
        """Return *word* inflected for *case*. See :func:`kyrgyz.inflect`."""
        return self.inflect_detailed(word, case=case, strict=strict).text

    def inflect_detailed(
        self,
        word: str | Word,
        *,
        case: Case = Case.NOMINATIVE,
        strict: bool = False,
    ) -> InflectionResult:
        """Inflect *word* and return the form with its derivation and diagnostics.

        See :func:`kyrgyz.inflect_detailed`.
        """
        word = Word.coerce(word)
        features = Features(case=case)
        result = self._from_lexicon(word, features) or self._from_rules(word, features)
        if strict and result.uncertainties:
            reasons = "; ".join(sorted(u.description for u in result.uncertainties))
            raise AmbiguousWordError(
                f"{word.text!r} → {result.text!r} is not certain in strict mode: {reasons}",
                result.uncertainties,
            )
        return result

    def _from_lexicon(self, word: Word, features: Features) -> InflectionResult | None:
        entry = self._lexicon.lookup(word.text, features)
        if entry is None:
            return None
        text = match_case(entry.form, word.text)
        return InflectionResult(
            text=text,
            word=word,
            features=features,
            stem=text,
            suffix="",
            source=Source.LEXICON,
        )

    def _from_rules(self, word: Word, features: Features) -> InflectionResult:
        spoken_form = pronunciation(word.text) if word.is_numeric else word.pronunciation
        form = inflect_noun(word.text, features, pronunciation=spoken_form)
        uncertainties = set(form.uncertainties)
        suffix = form.suffix

        if suffix:
            uncertainties |= _abbreviation_uncertainties(word)
            if word.abbreviation is not True and is_all_caps(last_word(word.text)):
                suffix = suffix.upper()

        return InflectionResult(
            text=form.stem + suffix,
            word=word,
            features=features,
            stem=form.stem,
            suffix=suffix,
            source=Source.RULE,
            profile=form.profile,
            uncertainties=frozenset(uncertainties),
        )


def _abbreviation_uncertainties(word: Word) -> set[Uncertainty]:
    if word.abbreviation is True:
        return set() if word.pronunciation is not None else {Uncertainty.ABBREVIATION_READING_ASSUMED}
    if word.abbreviation is None and is_all_caps(last_word(word.text)):
        return {Uncertainty.POSSIBLE_ABBREVIATION}
    return set()


_DEFAULT_INFLECTOR = Inflector()


def inflect(word: str | Word, *, case: Case = Case.NOMINATIVE, strict: bool = False) -> str:
    """Inflect a Kyrgyz word.

    >>> from kyrgyz.cases import DATIVE
    >>> inflect("Алибек", case=DATIVE)
    'Алибекке'

    Args:
        word: A Kyrgyz Cyrillic word or name, or a :class:`Word` with metadata.
        case: The target case. Defaults to the nominative (no suffix).
        strict: If True, raise :class:`AmbiguousWordError` instead of returning
            a form that depends on an assumption (see :class:`Uncertainty`).

    Raises:
        TypeError: if *word* is not a ``str``/``Word`` or *case* not a ``Case``.
        InvalidWordError: if *word* is not well-formed Kyrgyz Cyrillic.
        AmbiguousWordError: if the suffix cannot be chosen without guessing
            (e.g. no vowel letter), or in strict mode for uncertain results.
    """
    return _DEFAULT_INFLECTOR.inflect(word, case=case, strict=strict)


def inflect_detailed(
    word: str | Word,
    *,
    case: Case = Case.NOMINATIVE,
    strict: bool = False,
) -> InflectionResult:
    """Like :func:`inflect`, but return an :class:`InflectionResult`.

    >>> from kyrgyz.cases import DATIVE
    >>> result = inflect_detailed("медаль", case=DATIVE)
    >>> result.text, result.stem, result.suffix
    ('медалга', 'медал', 'га')
    >>> sorted(u.value for u in result.uncertainties)
    ['soft_sign_dropped']
    """
    return _DEFAULT_INFLECTOR.inflect_detailed(word, case=case, strict=strict)
