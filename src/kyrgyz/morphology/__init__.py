"""Kyrgyz morphology: suffix inventories and how they attach to stems."""

from kyrgyz.morphology.case import CASE_SUFFIXES, case_suffix
from kyrgyz.morphology.noun import SuffixedForm, attach, inflect_noun
from kyrgyz.morphology.suffix import SuffixTemplate, realize

__all__ = [
    "CASE_SUFFIXES",
    "SuffixTemplate",
    "SuffixedForm",
    "attach",
    "case_suffix",
    "inflect_noun",
    "realize",
]
