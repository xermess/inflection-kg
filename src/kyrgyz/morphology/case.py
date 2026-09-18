"""Case suffixes (жөндөмө мүчөлөрү) of the plain (non-possessive) declension.

==============  ================  =========  ================================
Case            Kyrgyz term       Template   Examples
==============  ================  =========  ================================
Nominative      Атооч жөндөмө     -∅         үй, апа
Genitive        Илик жөндөмө      -NIн       үйдүн, апанын, мектептин
Dative          Барыш жөндөмө     -GA        үйгө, апага, мектепке
Accusative      Табыш жөндөмө     -NI        үйдү, апаны, мектепти
Locative        Жатыш жөндөмө     -DA        үйдө, апада, мектепте
Ablative        Чыгыш жөндөмө     -DAн       үйдөн, ападан, мектептен
==============  ================  =========  ================================

These are the forms used after a bare stem (or, in later phases, after the
plural). After possessive suffixes Kyrgyz uses other allomorphs, e.g. dative
``-нА`` after the 3rd person (``үйүнө``) and ``-А`` after the 1st/2nd person
singular (``үйүмө``). Those belong to a separate "possessive declension"
table, to be added with possessive morphology.

Sources: Абдувалиев И., *Кыргыз тилинин морфологиясы* (sections "Илик
жөндөмө" ... "Чыгыш жөндөмө"); Kara (2003), case table reproduced in the
Wikipedia article "Kyrgyz language".
"""

from __future__ import annotations

from types import MappingProxyType

from kyrgyz.cases import Case
from kyrgyz.morphology.suffix import SuffixTemplate

CASE_SUFFIXES: MappingProxyType[Case, SuffixTemplate] = MappingProxyType(
    {
        Case.NOMINATIVE: SuffixTemplate(""),
        Case.GENITIVE: SuffixTemplate("NIн"),
        Case.DATIVE: SuffixTemplate("GA"),
        Case.ACCUSATIVE: SuffixTemplate("NI"),
        Case.LOCATIVE: SuffixTemplate("DA"),
        Case.ABLATIVE: SuffixTemplate("DAн"),
    }
)


def case_suffix(case: Case) -> SuffixTemplate:
    """Return the plain-declension suffix template for *case*."""
    return CASE_SUFFIXES[case]
