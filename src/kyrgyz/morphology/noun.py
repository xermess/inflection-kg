"""Noun inflection: attaching grammatical suffixes to a noun stem.

This module is where morphology meets phonology. It prepares the stem,
analyses it and realises the suffix, but it is unaware of letter case,
lexical exceptions and error policy, which :mod:`kyrgyz.inflector` handles.
"""

from __future__ import annotations

from dataclasses import dataclass

from kyrgyz.diagnostics import Uncertainty
from kyrgyz.features import Features
from kyrgyz.morphology.case import case_suffix
from kyrgyz.morphology.suffix import SuffixTemplate, realize
from kyrgyz.phonology.analysis import PhonologicalProfile, analyze
from kyrgyz.phonology.transformations import prepare_stem


@dataclass(frozen=True)
class SuffixedForm:
    """A stem and the lowercase suffix realised for it.

    ``profile`` is the phonological analysis the suffix was chosen from,
    or ``None`` when no suffix was needed.
    """

    stem: str
    suffix: str
    profile: PhonologicalProfile | None = None
    uncertainties: frozenset[Uncertainty] = frozenset()


def attach(
    stem: str,
    template: SuffixTemplate,
    *,
    pronunciation: str | None = None,
) -> SuffixedForm:
    """Attach one suffix *template* to *stem*.

    Args:
        stem: A validated word, in any letter case.
        template: The suffix to attach.
        pronunciation: Optional phonetic respelling used *instead of* the stem
            for the phonological analysis (e.g. for abbreviations).
    """
    if template.is_empty:
        return SuffixedForm(stem=stem, suffix="")

    prepared = prepare_stem(stem)
    profile = analyze(pronunciation if pronunciation is not None else prepared.text)
    return SuffixedForm(
        stem=prepared.text,
        suffix=realize(template, profile),
        profile=profile,
        uncertainties=prepared.uncertainties,
    )


def inflect_noun(stem: str, features: Features, *, pronunciation: str | None = None) -> SuffixedForm:
    """Inflect a noun stem for the requested *features* (currently case only)."""
    return attach(stem, case_suffix(features.case), pronunciation=pronunciation)
