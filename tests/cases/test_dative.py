"""Dative case (Барыш жөндөмө): -GA → -га/-ге/-го/-гө/-ка/-ке/-ко/-кө.

Expected forms are either cited in a source (noted inline) or follow from the
rules documented in :mod:`kyrgyz.phonology.harmony` and
:mod:`kyrgyz.phonology.consonants`. Each group isolates one rule.
"""

from __future__ import annotations

import pytest

from kyrgyz import inflect, inflect_detailed
from kyrgyz.cases import DATIVE


def _check(word: str, expected: str) -> None:
    assert inflect(word, case=DATIVE) == expected


# --- The examples from the specification -------------------------------------------------


@pytest.mark.parametrize(
    ("word", "expected"),
    [("Алибек", "Алибекке"), ("үй", "үйгө"), ("мектеп", "мектепке"), ("апа", "апага")],
)
def test_specification_examples(word: str, expected: str) -> None:
    _check(word, expected)


# --- Vowel harmony -----------------------------------------------------------------------


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("апа", "апага"),
        ("бала", "балага"),
        ("аба", "абага"),  # Kara (2003)
        ("кыз", "кызга"),
        ("жыл", "жылга"),
        ("алма", "алмага"),
        ("баш", "башка"),  # Kara (2003)
        ("тамак", "тамакка"),
        ("кагаз", "кагазга"),
    ],
)
def test_back_unrounded_stems_take_a(word: str, expected: str) -> None:
    _check(word, expected)


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("кол", "колго"),  # Kara (2003)
        ("тоо", "тоого"),
        ("жол", "жолго"),  # Абдувалиев: "жол, жолго"
        ("от", "отко"),
        ("тоок", "тоокко"),
        ("орок", "орокко"),
        ("оң", "оңго"),
    ],
)
def test_back_low_rounded_stems_take_o(word: str, expected: str) -> None:
    _check(word, expected)


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("туз", "тузга"),  # Kara (2003)
        ("суу", "сууга"),
        ("кум", "кумга"),
        ("уул", "уулга"),
        ("жумуш", "жумушка"),
        ("булут", "булутка"),
        ("бут", "бутка"),
        ("кулун", "кулунга"),
    ],
)
def test_u_does_not_round_a_low_suffix_vowel(word: str, expected: str) -> None:
    """The у → а asymmetry: after у the dative is -га/-ка, never -го/-ко."""
    _check(word, expected)


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("кеме", "кемеге"),  # Kara (2003)
        ("челек", "челекке"),  # Kara (2003)
        ("эне", "энеге"),
        ("жер", "жерге"),
        ("киши", "кишиге"),
        ("иш", "ишке"),
        ("тил", "тилге"),
        ("китеп", "китепке"),
        ("бий", "бийге"),
    ],
)
def test_front_unrounded_stems_take_e(word: str, expected: str) -> None:
    _check(word, expected)


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("көз", "көзгө"),  # Kara (2003)
        ("үй", "үйгө"),
        ("көл", "көлгө"),
        ("күн", "күнгө"),  # orthographic rules §38: "күңгө эмес, күнгө"
        ("түн", "түнгө"),
        ("сүт", "сүткө"),
        ("төө", "төөгө"),
        ("бөрү", "бөрүгө"),
        ("дүйнө", "дүйнөгө"),
        ("көпүрө", "көпүрөгө"),
        ("күч", "күчкө"),
        ("жүрөк", "жүрөккө"),
        ("күмүш", "күмүшкө"),
    ],
)
def test_front_rounded_stems_take_oe(word: str, expected: str) -> None:
    """Unlike у, the front rounded ү does round a following low vowel."""
    _check(word, expected)


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("мугалим", "мугалимге"),  # Абдувалиев lists these as disharmonic loans
        ("соодагер", "соодагерге"),
        ("телефон", "телефонго"),
        ("геометрия", "геометрияга"),
        ("Кыргызстан", "Кыргызстанга"),
    ],
)
def test_disharmonic_words_follow_the_last_vowel(word: str, expected: str) -> None:
    _check(word, expected)


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("Азия", "Азияга"),  # я behaves as а
        ("Россия", "Россияга"),
        ("бюро", "бюрого"),  # last vowel о
        ("меню", "менюга"),  # ю behaves as у, so low vowel а
        ("актёр", "актёрго"),  # ё behaves as о
        ("самолёт", "самолётко"),
        ("поэт", "поэтке"),  # э behaves as е
    ],
)
def test_yotated_and_e_letters(word: str, expected: str) -> None:
    _check(word, expected)


# --- Suffix-initial consonant: г after vowels and voiced consonants, к after voiceless ----


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("апа", "апага"),
        ("кеме", "кемеге"),
        ("кино", "киного"),
        ("такси", "таксиге"),
        ("кафе", "кафеге"),
        ("Москва", "Москвага"),
        ("бөрү", "бөрүгө"),
        ("суу", "сууга"),
        ("аары", "аарыга"),
    ],
)
def test_vowel_final_stems_take_g(word: str, expected: str) -> None:
    _check(word, expected)


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("бал", "балга"),  # л
        ("адам", "адамга"),  # м
        ("илим", "илимге"),
        ("тон", "тонго"),  # н
        ("таң", "таңга"),  # ң
        ("миң", "миңге"),
        ("көң", "көңгө"),
        ("шаар", "шаарга"),  # р
        ("Өмүр", "Өмүргө"),
        ("той", "тойго"),  # й
        ("бай", "байга"),
        ("кыз", "кызга"),  # з
        ("сөз", "сөзгө"),
    ],
)
def test_sonorant_and_z_final_stems_take_g(word: str, expected: str) -> None:
    _check(word, expected)


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        # Loanwords keep a written voiced final (orthographic rules §7), and the suffix
        # follows the spelling, not the devoiced pronunciation (§32).
        ("педагог", "педагогго"),  # §32: "педагогко эмес, педагогго"
        ("Гамбург", "Гамбургга"),  # §32: "Гамбургка эмес, Гамбургга"
        ("эпилог", "эпилогго"),  # §7
        ("клуб", "клубга"),  # §7
        ("герб", "гербге"),  # §7
        ("араб", "арабга"),  # §7
        ("парад", "парадга"),  # §7
        ("завод", "заводго"),
        ("Калининград", "Калининградга"),  # §32 (locative "Калининградда")
        ("гараж", "гаражга"),  # §7
        ("Париж", "Парижге"),
        ("Алиев", "Алиевге"),  # §32 (genitive "Алиевдин")
        ("Иванов", "Ивановго"),
    ],
)
def test_written_voiced_obstruent_finals_take_g(word: str, expected: str) -> None:
    _check(word, expected)


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("Алибек", "Алибекке"),  # к
        ("ак", "акка"),
        ("мектеп", "мектепке"),  # п
        ("топ", "топко"),
        ("сап", "сапка"),
        ("түп", "түпкө"),
        ("Талас", "Таласка"),  # с
        ("автобус", "автобуска"),
        ("Азамат", "Азаматка"),  # т
        ("эт", "этке"),
        ("шкаф", "шкафка"),  # ф
        ("цех", "цехке"),  # х
        ("шприц", "шприцке"),  # ц
        ("агач", "агачка"),  # ч
        ("Ош", "Ошко"),  # ш
        ("борщ", "борщко"),  # щ
    ],
)
def test_voiceless_final_stems_take_k(word: str, expected: str) -> None:
    _check(word, expected)


# --- Proper names ------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("Алибек", "Алибекке"),
        ("Бекзат", "Бекзатка"),
        ("Айбек", "Айбекке"),
        ("Нурбек", "Нурбекке"),
        ("Азамат", "Азаматка"),
        ("Эрмек", "Эрмекке"),
        ("Жаныбек", "Жаныбекке"),
        ("Айгүл", "Айгүлгө"),
        ("Жамийла", "Жамийлага"),
        ("Бишкек", "Бишкекке"),
        ("Ош", "Ошко"),
        ("Каракол", "Караколго"),
        ("Нарын", "Нарынга"),
        ("Талас", "Таласка"),
        ("Токмок", "Токмокко"),
        ("Баткен", "Баткенге"),
        ("Өзгөн", "Өзгөнгө"),
        ("Суусамыр", "Суусамырга"),
    ],
)
def test_proper_names(word: str, expected: str) -> None:
    _check(word, expected)


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("Ысык-Көл", "Ысык-Көлгө"),
        ("Кара-Балта", "Кара-Балтага"),
        ("Чолпон-Ата", "Чолпон-Атага"),
        ("Жалал-Абад", "Жалал-Абадга"),
        ("Үч-Коргон", "Үч-Коргонго"),
        ("Алибек Асанов", "Алибек Асановго"),
        ("Айгүл Сейитбекова", "Айгүл Сейитбековага"),
    ],
)
def test_compound_and_multiword_names_inflect_the_last_word(word: str, expected: str) -> None:
    _check(word, expected)


# --- Soft sign -------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("медаль", "медалга"),  # cf. Абдувалиев: «Даңк» медалы
        ("роль", "ролго"),  # cf. Абдувалиев: ролду, ролун
        ("автомобиль", "автомобилге"),  # cf. Абдувалиев: автомобилдин
    ],
)
def test_final_soft_sign_is_dropped(word: str, expected: str) -> None:
    result = inflect_detailed(word, case=DATIVE)
    assert result.text == expected
    assert result.stem == word[:-1]
    assert not result.is_certain
