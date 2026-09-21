"""Inflect Kyrgyz numeric values in all six cases.

Usage:
    python examples/numeric_cases.py
    python examples/numeric_cases.py 5 21 "5 000" "-12"
"""

import argparse

from kyrgyz import KyrgyzError, inflect
from kyrgyz.cases import ABLATIVE, ACCUSATIVE, DATIVE, Case

SAMPLE_VALUES = [
    "5",
    "21",
    "200",
    "5 000",
    "200 000",
    "-12",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Inflect Kyrgyz integer values for all six cases.")
    parser.add_argument(
        "values",
        nargs="*",
        default=SAMPLE_VALUES,
        help="supported integers, optionally grouped with spaces",
    )
    args = parser.parse_args()

    for index, value in enumerate(args.values):
        if index:
            print()
        print(value)
        try:
            for case in Case:
                print(f"  {case.kyrgyz_name.split()[0]:<8} {inflect(value, case=case)}")
        except KyrgyzError as error:
            print(f"  error: {error}")

    print("\nSentence examples:")
    print(
        "  Range: "
        f"{inflect('2 000', case=ABLATIVE)} "
        f"{inflect('10 000', case=DATIVE)} чейин."
    )
    print(f"  Starting point: {inflect('500', case=ABLATIVE)} баштап катталса болот.")
    print(
        "  Arithmetic: "
        f"{inflect('1', case=DATIVE)} "
        f"{inflect('1', case=ACCUSATIVE)} кошсоң, "
        f"{inflect('2')} болот."
    )


if __name__ == "__main__":
    main()
