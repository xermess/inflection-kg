"""A rule-based morphological engine for Kyrgyz.

>>> from kyrgyz import inflect
>>> from kyrgyz.cases import DATIVE
>>> inflect("Алибек", case=DATIVE)
'Алибекке'
>>> inflect("үй", case=DATIVE)
'үйгө'
"""

from kyrgyz.cases import Case
from kyrgyz.diagnostics import Uncertainty
from kyrgyz.errors import AmbiguousWordError, InvalidWordError, KyrgyzError
from kyrgyz.features import Features
from kyrgyz.inflector import InflectionResult, Inflector, Source, inflect, inflect_detailed
from kyrgyz.lexicon import LexicalEntry, Lexicon
from kyrgyz.word import Word

__version__ = "0.1.0"

__all__ = [
    "AmbiguousWordError",
    "Case",
    "Features",
    "InflectionResult",
    "Inflector",
    "InvalidWordError",
    "KyrgyzError",
    "LexicalEntry",
    "Lexicon",
    "Source",
    "Uncertainty",
    "Word",
    "__version__",
    "inflect",
    "inflect_detailed",
]
