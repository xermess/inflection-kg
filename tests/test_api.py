"""The public API surface."""

from __future__ import annotations

import dataclasses

import pytest

import kyrgyz
from kyrgyz import Features, InflectionResult, Inflector, Source, Word, cases, inflect, inflect_detailed
from kyrgyz.cases import DATIVE, Case


def test_readme_example() -> None:
    assert inflect("Алибек", case=DATIVE) == "Алибекке"


def test_aliases_are_the_canonical_members() -> None:
    assert cases.TO is Case.DATIVE
    assert cases.FROM is Case.ABLATIVE
    assert cases.IN is Case.LOCATIVE
    assert cases.OF is Case.GENITIVE
    assert inflect("үй", case=cases.TO) == "үйгө"


@pytest.mark.parametrize(
    ("case", "name"),
    [
        (Case.NOMINATIVE, "Атооч жөндөмө"),
        (Case.GENITIVE, "Илик жөндөмө"),
        (Case.DATIVE, "Барыш жөндөмө"),
        (Case.ACCUSATIVE, "Табыш жөндөмө"),
        (Case.LOCATIVE, "Жатыш жөндөмө"),
        (Case.ABLATIVE, "Чыгыш жөндөмө"),
    ],
)
def test_kyrgyz_case_names(case: Case, name: str) -> None:
    assert case.kyrgyz_name == name


def test_case_values_are_stable_strings() -> None:
    assert Case("dative") is Case.DATIVE


def test_detailed_result() -> None:
    result = inflect_detailed("Алибек", case=DATIVE)
    assert isinstance(result, InflectionResult)
    assert str(result) == result.text == "Алибекке"
    assert (result.stem, result.suffix, result.source) == ("Алибек", "ке", Source.RULE)
    assert result.word == Word("Алибек")
    assert result.features == Features(case=DATIVE)
    assert result.profile is not None
    assert result.profile.last_vowel.letter == "е"
    assert result.is_certain


def test_results_and_words_are_immutable() -> None:
    result = inflect_detailed("үй", case=DATIVE)
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.text = "x"  # type: ignore[misc]
    with pytest.raises(dataclasses.FrozenInstanceError):
        Word("үй").text = "x"  # type: ignore[misc]


def test_inflector_instance_matches_module_functions() -> None:
    inflector = Inflector()
    for word in ["Алибек", "үй", "мен", "Ош"]:
        assert inflector.inflect(word, case=DATIVE) == inflect(word, case=DATIVE)


def test_proper_flag_does_not_change_inflection() -> None:
    assert inflect(Word("Нарын", proper=True), case=DATIVE) == inflect("Нарын", case=DATIVE)


def test_deterministic() -> None:
    assert len({inflect("Ысык-Көл", case=DATIVE) for _ in range(100)}) == 1


def test_package_exports() -> None:
    for name in kyrgyz.__all__:
        assert hasattr(kyrgyz, name)
    assert kyrgyz.__version__
