"""Full six-case paradigms.

The first table reproduces the case paradigm in Kara (2003), *Kyrgyz*,
as given in the Wikipedia article "Kyrgyz language" (section "Case").
"""

from __future__ import annotations

import pytest

from kyrgyz import inflect
from kyrgyz.cases import ABLATIVE, ACCUSATIVE, DATIVE, GENITIVE, LOCATIVE, NOMINATIVE, Case

CASE_ORDER = (NOMINATIVE, GENITIVE, DATIVE, ACCUSATIVE, LOCATIVE, ABLATIVE)

KARA_2003 = {
    "кеме": ("кеме", "кеменин", "кемеге", "кемени", "кемеде", "кемеден"),
    "аба": ("аба", "абанын", "абага", "абаны", "абада", "абадан"),
    "челек": ("челек", "челектин", "челекке", "челекти", "челекте", "челектен"),
    "кол": ("кол", "колдун", "колго", "колду", "колдо", "колдон"),
    "баш": ("баш", "баштын", "башка", "башты", "башта", "баштан"),
    "туз": ("туз", "туздун", "тузга", "тузду", "тузда", "туздан"),
    "көз": ("көз", "көздүн", "көзгө", "көздү", "көздө", "көздөн"),
}

RULE_DERIVED = {
    # vowel-final: н- for genitive/accusative
    "апа": ("апа", "апанын", "апага", "апаны", "апада", "ападан"),
    "тоо": ("тоо", "тоонун", "тоого", "тоону", "тоодо", "тоодон"),
    "суу": ("суу", "суунун", "сууга", "сууну", "сууда", "суудан"),
    "бөрү": ("бөрү", "бөрүнүн", "бөрүгө", "бөрүнү", "бөрүдө", "бөрүдөн"),
    "киши": ("киши", "кишинин", "кишиге", "кишини", "кишиде", "кишиден"),
    # й and р pattern with voiced consonants (Kara 2003: айды, торду)
    "үй": ("үй", "үйдүн", "үйгө", "үйдү", "үйдө", "үйдөн"),
    "шаар": ("шаар", "шаардын", "шаарга", "шаарды", "шаарда", "шаардан"),
    # nasals take д- in every case (no н- ablative in the plain declension)
    "адам": ("адам", "адамдын", "адамга", "адамды", "адамда", "адамдан"),
    "таң": ("таң", "таңдын", "таңга", "таңды", "таңда", "таңдан"),
    # voiceless finals
    "мектеп": ("мектеп", "мектептин", "мектепке", "мектепти", "мектепте", "мектептен"),
    "жумуш": ("жумуш", "жумуштун", "жумушка", "жумушту", "жумушта", "жумуштан"),
    "сүт": ("сүт", "сүттүн", "сүткө", "сүттү", "сүттө", "сүттөн"),
}

PROPER_NAMES = {
    "Алибек": ("Алибек", "Алибектин", "Алибекке", "Алибекти", "Алибекте", "Алибектен"),
    "Бишкек": ("Бишкек", "Бишкектин", "Бишкекке", "Бишкекти", "Бишкекте", "Бишкектен"),
    "Ош": ("Ош", "Оштун", "Ошко", "Ошту", "Ошто", "Оштон"),
    "Каракол": ("Каракол", "Караколдун", "Караколго", "Караколду", "Караколдо", "Караколдон"),
    "Нарын": ("Нарын", "Нарындын", "Нарынга", "Нарынды", "Нарында", "Нарындан"),
    "Талас": ("Талас", "Таластын", "Таласка", "Таласты", "Таласта", "Таластан"),
    "Ысык-Көл": ("Ысык-Көл", "Ысык-Көлдүн", "Ысык-Көлгө", "Ысык-Көлдү", "Ысык-Көлдө", "Ысык-Көлдөн"),
}

LOANWORDS = {
    # orthographic rules §32: "Калининградта эмес, Калининградда", "Алиевтин эмес, Алиевдин"
    "Калининград": (
        "Калининград",
        "Калининграддын",
        "Калининградга",
        "Калининградды",
        "Калининградда",
        "Калининграддан",
    ),
    "Алиев": ("Алиев", "Алиевдин", "Алиевге", "Алиевди", "Алиевде", "Алиевден"),
    "педагог": ("педагог", "педагогдун", "педагогго", "педагогду", "педагогдо", "педагогдон"),
}


def _paradigm_cases(table: dict[str, tuple[str, ...]]) -> list[tuple[str, Case, str]]:
    return [
        (word, case, form)
        for word, forms in table.items()
        for case, form in zip(CASE_ORDER, forms, strict=True)
    ]


@pytest.mark.parametrize(("word", "case", "expected"), _paradigm_cases(KARA_2003))
def test_kara_2003_paradigm(word: str, case: Case, expected: str) -> None:
    assert inflect(word, case=case) == expected


@pytest.mark.parametrize(("word", "case", "expected"), _paradigm_cases(RULE_DERIVED))
def test_rule_derived_paradigms(word: str, case: Case, expected: str) -> None:
    assert inflect(word, case=case) == expected


@pytest.mark.parametrize(("word", "case", "expected"), _paradigm_cases(PROPER_NAMES))
def test_proper_name_paradigms(word: str, case: Case, expected: str) -> None:
    assert inflect(word, case=case) == expected


@pytest.mark.parametrize(("word", "case", "expected"), _paradigm_cases(LOANWORDS))
def test_loanword_paradigms(word: str, case: Case, expected: str) -> None:
    assert inflect(word, case=case) == expected


@pytest.mark.parametrize("word", ["Алибек", "үй", "КТР", "Ж", "медаль", "мен"])
def test_nominative_returns_the_word_unchanged(word: str) -> None:
    """The nominative has a zero suffix, so no analysis is needed (even for КТР)."""
    assert inflect(word, case=NOMINATIVE) == word
    assert inflect(word) == word
