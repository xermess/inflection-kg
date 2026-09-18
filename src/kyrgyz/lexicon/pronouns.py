"""Irregular case forms of the singular personal pronouns.

The singular pronouns мен "I", сен "you (informal)" and ал "he/she/it" have
irregular forms in some cases. Only those irregular forms are listed; all
other pronoun forms (``менде``, ``сизге``, ``аларга`` ...) follow the general
rules and are deliberately *not* listed, so that the rules stay tested.

    ======  ==========  ===========  ============
    Case    мен         сен          ал
    ======  ==========  ===========  ============
    Gen     менин       сенин        анын
    Dat     мага        сага         ага
    Acc     мени        сени         аны
    Loc     (менде)     (сенде)      анда
    Abl     (менден)    (сенден)     андан
    ======  ==========  ===========  ============

Source: Wikipedia, "Kyrgyz language", section "Pronouns" (declension table,
irregular forms marked in bold there).

Note: ``ал`` is also the imperative of the verb "take" and a rare noun; the
lexicon cannot tell homographs apart. Use ``Inflector(lexicon=Lexicon.empty())``
to inflect such words by rule.
"""

from __future__ import annotations

from kyrgyz.cases import Case
from kyrgyz.features import Features
from kyrgyz.lexicon.lexicon import LexicalEntry

_SOURCE = "Wikipedia, 'Kyrgyz language', Pronouns: declension of pronouns"

_IRREGULAR_FORMS: dict[str, dict[Case, str]] = {
    "мен": {Case.GENITIVE: "менин", Case.DATIVE: "мага", Case.ACCUSATIVE: "мени"},
    "сен": {Case.GENITIVE: "сенин", Case.DATIVE: "сага", Case.ACCUSATIVE: "сени"},
    "ал": {
        Case.GENITIVE: "анын",
        Case.DATIVE: "ага",
        Case.ACCUSATIVE: "аны",
        Case.LOCATIVE: "анда",
        Case.ABLATIVE: "андан",
    },
}

PERSONAL_PRONOUNS: tuple[LexicalEntry, ...] = tuple(
    LexicalEntry(lemma, Features(case=case), form, _SOURCE)
    for lemma, forms in _IRREGULAR_FORMS.items()
    for case, form in forms.items()
)
