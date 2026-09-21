"""Invalid input, Unicode handling and letter case."""

from __future__ import annotations

import unicodedata

import pytest

from kyrgyz import InvalidWordError, Word, inflect
from kyrgyz.cases import ABLATIVE, DATIVE, GENITIVE, LOCATIVE

# --- Invalid input -----------------------------------------------------------------------


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ("", "empty"),
        ("Alibek", "Latin"),
        ("Aлибек", "Latin"),  # Latin capital A look-alike
        ("мектeп", "Latin"),  # Latin small e look-alike
        ("Алибек1", "numerals"),
        ("Алибек!", "unsupported character"),
        ("Алибек.", "unsupported character"),
        ("кұс", "not a letter of the Kyrgyz alphabet"),  # Kazakh ұ
        ("әке", "not a letter of the Kyrgyz alphabet"),  # Kazakh ә
        ("Кара–Балта", "unsupported character"),  # en dash instead of hyphen
        ("Алибек\tАсанов", "unsupported character"),
        (" Алибек", "malformed"),
        ("Алибек ", "malformed"),
        ("Алибек  Асанов", "malformed"),
        ("Кара--Балта", "malformed"),
        ("-Алибек", "malformed"),
        ("Кара-", "malformed"),
    ],
)
def test_invalid_words_are_rejected(value: str, message: str) -> None:
    with pytest.raises(InvalidWordError, match=message):
        inflect(value, case=DATIVE)


def test_invalid_word_error_is_a_value_error() -> None:
    with pytest.raises(ValueError):
        inflect("Alibek", case=DATIVE)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("5", "5ке"),
        ("5 000", "5 000ге"),
        ("200 000", "200 000ге"),
        ("21", "21ге"),
        ("20", "20га"),
    ],
)
def test_numeric_values_use_their_kyrgyz_reading_for_suffixes(value: str, expected: str) -> None:
    assert inflect(value, case=DATIVE) == expected


def test_numeric_values_preserve_grouping_and_support_ablative() -> None:
    assert inflect("5 000", case=ABLATIVE) == "5 000ден"


@pytest.mark.parametrize("value", ["02", "5 00", "5 0000", "5.0", "-"])
def test_malformed_numeric_values_are_rejected(value: str) -> None:
    with pytest.raises(InvalidWordError):
        inflect(value, case=DATIVE)


@pytest.mark.parametrize("value", [None, 42, b"\xd2\xaf\xd0\xb9", ["үй"]])
def test_non_string_input_is_a_type_error(value: object) -> None:
    with pytest.raises(TypeError, match="must be a str"):
        inflect(value, case=DATIVE)  # type: ignore[arg-type]


@pytest.mark.parametrize("case", ["dative", 2, None])
def test_case_must_be_a_case_member(case: object) -> None:
    with pytest.raises(TypeError, match="Case"):
        inflect("үй", case=case)  # type: ignore[arg-type]


def test_features_are_keyword_only() -> None:
    with pytest.raises(TypeError):
        inflect("үй", DATIVE)  # type: ignore[misc]


# --- Unicode -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("өрүк", "өрүккө"),  # Kyrgyz-specific letters in lower and upper case
        ("ӨРҮК", "ӨРҮККӨ"),
        ("үй", "үйгө"),
        ("ҮЙ", "ҮЙГӨ"),
        ("Үй", "Үйгө"),
        ("таң", "таңга"),
        ("ТАҢ", "ТАҢГА"),
        ("кыз", "кызга"),
        ("КЫЗ", "КЫЗГА"),
        ("Өзгөн", "Өзгөнгө"),
        ("ӨЗГӨН", "ӨЗГӨНГӨ"),
    ],
)
def test_kyrgyz_specific_letters(word: str, expected: str) -> None:
    assert inflect(word, case=DATIVE) == expected


def test_decomposed_input_is_normalised_to_nfc() -> None:
    decomposed_i_kratkoe = "то\u0438\u0306"  # "той" with й as и + combining breve
    assert unicodedata.normalize("NFC", decomposed_i_kratkoe) == "той"
    assert inflect(decomposed_i_kratkoe, case=DATIVE) == "тойго"
    decomposed_yo = "акт\u0435\u0308р"  # "актёр" with ё as е + combining diaeresis
    assert inflect(decomposed_yo, case=DATIVE) == "актёрго"


def test_output_contains_only_kyrgyz_code_points() -> None:
    result = inflect("Ысык-Көл", case=GENITIVE)
    assert result == "Ысык-Көлдүн"
    assert all(unicodedata.name(c).startswith(("CYRILLIC", "HYPHEN")) for c in result)


# --- Letter case -------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("Алибек", "Алибекке"),
        ("алибек", "алибекке"),
        ("албек", "албекке"),
        ("БИШКЕК", "БИШКЕККЕ"),
        ("Бишкек", "Бишкекке"),
        ("бИШКЕК", "бИШКЕКке"),  # mixed case is not all caps
        ("А", "Ага"),  # a single capital is not "all caps"
        ("КАРА-БАЛТА", "КАРА-БАЛТАГА"),
        ("Алибек АСАНОВ", "Алибек АСАНОВГО"),
        ("АЛИБЕК Асанов", "АЛИБЕК Асановго"),
    ],
)
def test_suffix_case_follows_the_last_word(word: str, expected: str) -> None:
    assert inflect(word, case=DATIVE) == expected


def test_stem_is_never_recased() -> None:
    assert inflect("МеКтЕп", case=LOCATIVE) == "МеКтЕпте"


def test_word_metadata_is_normalised() -> None:
    word = Word("КТР", abbreviation=True, pronunciation="КАТЭЭР")
    assert word.pronunciation == "катээр"
    assert Word.coerce(word) is word
    assert Word.coerce("үй") == Word("үй")


def test_pronunciation_is_validated() -> None:
    with pytest.raises(InvalidWordError, match="pronunciation"):
        Word("КТР", pronunciation="kater")
    with pytest.raises(InvalidWordError, match="must end"):
        Word("КТР", pronunciation="катэрь")
