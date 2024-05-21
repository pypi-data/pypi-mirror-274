# Random Credit Card

Generate random but theoretically valid credit card numbers.

### /!\ Disclamer

This code is intended for educational / regulated testing purposes only. It is provided "as is" without any warranties. Use at your own risk and ensure compliance with applicable laws.

## Install


Random Credit Card can be installed from [PyPI]().

```sh
python3 -m pip install random-credit-card
```

## Use as a script

If package is installed

```
python3 -m random_credit_card.credit_cards
```

Or download and run [credit_cards.py](random_credit_card/credit_cards.py).

```sh
python3 credit_cards.py
```



## Use as a Python module

```py
from random_credit_card import CreditCardNumber, ExpirationDate, generate_csc

...
number = CreditCardNumber() # Randomly generated
exp = ExpirationDate() # Randomly generated
code = generate_csc() # Randomly generated
```
