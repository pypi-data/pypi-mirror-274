# Random Credit Card (https://github.com/alexandrerbb/random_credit_card)
"""
Generate random but theoretically valid credit card numbers.
"""

import logging
from datetime import date
from secrets import choice, randbelow
from typing import Optional, Sequence


CC_NUMBER_PREFIXES = {"visa": "4", "mastercard": "5"}


def pick_cc_brand(
    options: Optional[Sequence[str]] = None,
) -> tuple[str, str]:
    """
    Randomly pick a credit card brand from a sequence of options or from
        default brands.

    Args:
        options (Optional[Sequence[str]], optional): An optional sequence
            of brands to pick from. Defaults to None.

    Raises:
        ValueError: No credit card number prefix is found for this card
            brand.

    Returns:
        tuple[str, str]: The brand name, the brand prefix.
    """
    if not options:
        options = list(CC_NUMBER_PREFIXES.keys())
    brand_name = choice(options)
    if not brand_name in CC_NUMBER_PREFIXES:
        raise ValueError(f"Invalid brand name {brand_name}")
    return brand_name, CC_NUMBER_PREFIXES[brand_name]


def generate_csc() -> int:
    """
    Returns:
        int: A random card security code.
    """
    return randbelow(1000)


def luhn_sum(numbers: list[int]) -> int:
    """
    Sum an integer list, weighting even number twice as much.

    Args:
        numbers (list[int]): A list of integers.

    Returns:
        int: A sum calculated with the luhn algorithm.
    """
    number_sequence = numbers.copy()
    if (to_complete := len(number_sequence) % 2) != 0:
        number_sequence.extend([0] * (2 - to_complete))
    return sum(number_sequence[1::2]) + sum(number_sequence[::2]) * 2


class ExpirationDate:
    """
    A randomly generated expiration date.
    """

    def __init__(self, expire_in_year: int = 5) -> None:
        """
        Args:
            expire_in_year (int, optional): Maximum expiration year from today.
                Defaults to 5.
        """
        self.expire_in_year = expire_in_year
        self.generate()

    def __str__(self) -> str:
        return f"{self.month:02}/{self.year}"

    def generate(self) -> None:
        """
        (Re)generate the expiration date.
        """
        today = date.today()
        self.year = today.year + randbelow(self.expire_in_year) + 1
        self.month = randbelow(12) + 1

    def to_date(self) -> date:
        """
        Returns:
            date: The expiration date.
        """
        return date(self.year, self.month, 1)


class CreditCardNumber:
    """
    A randomly generated, valid credit card number.
    """

    def __init__(
        self,
        brand_names: Optional[Sequence[str]] = None,
        number_prefixes: Optional[Sequence[str]] = None,
    ) -> None:
        """
        Args:
            brand_names (Optional[Sequence[str]], optional): Generate a credit
                card number of one of these brands. Defaults to None.
            number_prefixes (Optional[Sequence[str]], optional): Use one of
                these credit card number prefix. Defaults to None.
        """
        self.brand_names = brand_names
        self.number_prefixes = number_prefixes
        self.generate()

    def __str__(self) -> str:
        return " ".join(
            ["".join(map(str, self.card_number[x::4])) for x in range(4)]
        )

    def generate(self) -> None:
        """
        (Re)generate the card number.
        """
        if self.number_prefixes:
            brand_number_prefix = choice(self.number_prefixes)
        else:
            brand_name, brand_number_prefix = pick_cc_brand(self.brand_names)
            logging.debug("Selected %s.", brand_name)

        card_number = [
            *map(int, brand_number_prefix),
            *[randbelow(10) for i in range(15 - len(brand_number_prefix))],
        ]
        luhn_rest = luhn_sum(card_number) % 10
        control_number = 0 if luhn_rest == 0 else (10 - luhn_rest)
        card_number.append(control_number)
        self.card_number = card_number

    def to_string(self) -> str:
        """
        Returns:
            str: The credit card number as a string.
        """
        return "".join(map(str, self.card_number))


if __name__ == "__main__":
    # Run as a command line script.
    # pylint:disable=import-outside-toplevel
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--brand", choices=CC_NUMBER_PREFIXES.keys(), help="Credit card brand"
    )
    parser.add_argument("--number-prefix", help="Credit card number prefix")
    args = parser.parse_args()

    init_params = {}
    if brand := args.brand:
        init_params["brand_names"] = [brand]
    if number_prefix := args.number_prefix:
        init_params["number_prefixes"] = [number_prefix]

    cc_number = CreditCardNumber(**init_params)
    exp = ExpirationDate()
    csc = generate_csc()

    print(
        json.dumps(
            {
                "number": cc_number,
                "exp": exp,
                "csc": f"{csc:03}",
                "raw": {
                    "number": cc_number.to_string(),
                    "exp": exp.to_date().isoformat(),
                    "csc": csc,
                },
            },
            indent=2,
            default=str,
        )
    )
