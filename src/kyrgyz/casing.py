"""Letter-case handling for inflected forms.

Supported behaviour:

* The stem is never re-cased; it is returned exactly as given (after NFC
  normalisation and, for a final ``ь``, its removal).
* A suffix is written in uppercase only if the last word of the input is
  "all caps": at least two letters, all uppercase (``БИШКЕК`` → ``БИШКЕККЕ``).
  Otherwise it is lowercase (``Алибек`` → ``Алибекке``, ``албек`` → ``албекке``).
* Abbreviations (``Word(..., abbreviation=True)``) always take a lowercase
  suffix, per orthographic rules §55 (``БУУга``).
* A whole-form replacement from the lexicon copies the input's pattern:
  lowercase, capitalised first letter, or all caps (``Мен`` → ``Мага``).

Mixed-case input such as ``ЖОЖдор`` is treated as not all caps.
"""

from __future__ import annotations


def is_all_caps(text: str) -> bool:
    """Return True if *text* has at least two letters and all are uppercase."""
    letters = [char for char in text if char.isalpha()]
    return len(letters) >= 2 and all(char.isupper() for char in letters)


def match_case(form: str, model: str) -> str:
    """Return lowercase *form* re-cased to follow the pattern of *model*."""
    if is_all_caps(model):
        return form.upper()
    if model[:1].isupper():
        return form[:1].upper() + form[1:]
    return form
