"""
Generate random but theoretically valid credit card numbers.
"""

from . import credit_cards

CreditCardNumber = credit_cards.CreditCardNumber
ExpirationDate = credit_cards.ExpirationDate
generate_csc = credit_cards.generate_csc
luhn_sum = credit_cards.luhn_sum
