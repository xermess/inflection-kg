"""Kyrgyz cardinal readings used to inflect numeric forms."""

from __future__ import annotations

import re

_NUMERIC = re.compile(r"[+-]?(?:0|[1-9]\d*)(?: \d{3})*")
_ONES = ("нөл", "бир", "эки", "үч", "төрт", "беш", "алты", "жети", "сегиз", "тогуз")
_TEENS = ("он", "жыйырма", "отуз", "кырк", "элүү", "алтымыш", "жетимиш", "сексен", "токсон")
_SCALES = ("", "миң", "миллион", "миллиард", "триллион")


def is_numeric(text: str) -> bool:
    """Return whether *text* is a supported signed, optionally grouped integer."""
    if not _NUMERIC.fullmatch(text):
        return False
    digits = text.lstrip("+-").replace(" ", "")
    return len(digits) <= len(_SCALES) * 3 and (len(digits) == 1 or not digits.startswith("0"))


def pronunciation(text: str) -> str:
    """Return the Kyrgyz cardinal reading of a supported numeric form."""
    if not is_numeric(text):
        raise ValueError(f"{text!r} is not a supported numeric form")

    sign = text[:1] if text[:1] in "+-" else ""
    digits = text.lstrip("+-").replace(" ", "")
    if set(digits) == {"0"}:
        return "нөл"

    groups: list[int] = []
    while digits:
        groups.append(int(digits[-3:]))
        digits = digits[:-3]

    words: list[str] = []
    for index in range(len(groups) - 1, -1, -1):
        group = groups[index]
        if not group:
            continue
        words.extend(_under_thousand(group, omit_one=True) if index else _under_thousand(group))
        if index:
            words.append(_SCALES[index] if index < len(_SCALES) else f"10^{index * 3}")
    return ("минус " if sign == "-" else "плюс " if sign == "+" else "") + " ".join(words)


def _under_thousand(value: int, *, omit_one: bool = False) -> list[str]:
    words: list[str] = []
    hundreds, remainder = divmod(value, 100)
    if hundreds:
        if hundreds > 1 or not omit_one:
            words.append(_ONES[hundreds])
        words.append("жүз")
    if remainder >= 10:
        tens, ones = divmod(remainder, 10)
        words.append(_TEENS[tens - 1])
        if ones:
            words.append(_ONES[ones])
    elif remainder:
        words.append(_ONES[remainder])
    return words
