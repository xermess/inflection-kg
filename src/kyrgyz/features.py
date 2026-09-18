"""The bundle of grammatical features requested for an inflected form.

``Features`` is the single place where the requested grammatical categories
are collected. New categories (number, possessor, person, ...) are added here
as new fields with neutral defaults, so existing call sites keep working.
"""

from __future__ import annotations

from dataclasses import dataclass

from kyrgyz.cases import Case


@dataclass(frozen=True)
class Features:
    """Grammatical features of a target word form."""

    case: Case = Case.NOMINATIVE

    def __post_init__(self) -> None:
        if not isinstance(self.case, Case):
            raise TypeError(
                f"case must be a kyrgyz.cases.Case member, got {self.case!r} ({type(self.case).__name__})"
            )
