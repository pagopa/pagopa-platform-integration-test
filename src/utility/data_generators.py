import random
import string
import time


def get_random_digit_string(length: int) -> str:
    """Return a random numeric string with the requested length."""
    return ''.join(random.choice(string.digits) for _ in range(length))


def get_random_alphanumeric_string(length: int) -> str:
    """Return a random alphanumeric string with the requested length."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def generate_iuv(in_18digit_format: bool = False) -> str:
    """Generate an IUV in 15-digit or prefixed 18-digit format."""
    if in_18digit_format:
        return '348' + get_random_digit_string(15)
    return get_random_digit_string(15)


def generate_random_monetary_amount(min_value: float, max_value: float) -> float:
    """Generate a random monetary amount rounded to 2 decimal digits."""
    random_amount = random.uniform(min_value, max_value)
    return round(random_amount, 2)


def generate_ccp() -> str:
    """Generate a random 16-digit CCP code."""
    return get_random_digit_string(16)


def generate_cart_id(iuv: str | None, creditor_institution: str) -> str:
    """Generate a cart identifier from creditor institution and IUV when provided."""
    if iuv is not None:
        return f'{creditor_institution}{iuv}-{get_random_digit_string(5)}'
    return get_random_digit_string(32)


def generate_nav(segregation_code: str) -> str:
    """Generate a NAV identifier using the segregation code and current epoch ticks."""
    return f'3{segregation_code}{int(time.time() * 100000)}'


def change_last_numeric_char(value: str) -> str:
    """Replace the last numeric character with the next digit modulo 10."""
    last_char = value[-1]
    other_char = value[:-1]
    new_last_char = str((int(last_char) + 1) % 10)
    return other_char + new_last_char