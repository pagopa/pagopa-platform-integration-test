"""Unit tests for shared data generator utilities."""

from src.utility.assertions import assert_show_message
from src.utility.data_generators import generate_ccp
from src.utility.data_generators import change_last_numeric_char
from src.utility.data_generators import generate_cart_id
from src.utility.data_generators import generate_iuv
from src.utility.data_generators import generate_nav
from src.utility.data_generators import generate_random_monetary_amount
from src.utility.data_generators import get_random_alphanumeric_string
from src.utility.data_generators import get_random_digit_string
from src.utility.datetime_utils import get_current_date
from src.utility.datetime_utils import get_current_datetime
from src.utility.datetime_utils import get_tomorrow_datetime
from src.utility.indexing import get_index_from_cardinal


def test_get_random_digit_string_returns_requested_length():
    """Return a numeric string with the expected length."""
    value = get_random_digit_string(12)
    assert len(value) == 12
    assert value.isdigit()


def test_generate_iuv_default_format_has_15_digits():
    """Generate a 15-digit IUV in default format."""
    value = generate_iuv()
    assert len(value) == 15
    assert value.isdigit()


def test_generate_iuv_18digit_format_has_prefix_348():
    """Generate an 18-digit IUV with the expected prefix."""
    value = generate_iuv(in_18digit_format=True)
    assert len(value) == 18
    assert value.startswith("348")
    assert value.isdigit()


def test_get_random_alphanumeric_string_returns_requested_length():
    """Return an alphanumeric string with the expected length."""
    value = get_random_alphanumeric_string(20)
    assert len(value) == 20
    assert all(char.isalnum() for char in value)


def test_generate_cart_id_with_iuv_includes_creditor_and_suffix():
    """Compose cart id as creditor+iuv plus a 5-digit suffix when iuv is provided."""
    value = generate_cart_id("123456789012345", "77777777777")
    assert value.startswith("77777777777123456789012345-")
    assert len(value.split("-")[-1]) == 5
    assert value.split("-")[-1].isdigit()


def test_generate_cart_id_without_iuv_returns_32_digits():
    """Return a 32-digit random identifier when iuv is not provided."""
    value = generate_cart_id(None, "77777777777")
    assert len(value) == 32
    assert value.isdigit()


def test_change_last_numeric_char_rolls_over_after_nine():
    """Roll the last numeric character from 9 to 0."""
    assert change_last_numeric_char("ABC129") == "ABC120"


def test_generate_random_monetary_amount_is_rounded_and_in_range():
    """Return a random amount with two decimals inside the given range."""
    value = generate_random_monetary_amount(10.0, 11.0)
    assert 10.0 <= value <= 11.0
    assert round(value, 2) == value


def test_generate_ccp_returns_16_digits():
    """Generate a CCP as a 16-digit numeric string."""
    value = generate_ccp()
    assert len(value) == 16
    assert value.isdigit()


def test_generate_nav_starts_with_prefix_and_code():
    """Generate NAV including the static marker and segregation code."""
    value = generate_nav("47")
    assert value.startswith("347")
    assert value.isdigit()


def test_datetime_helpers_return_expected_shapes():
    """Return date-time and date strings using expected fixed formats."""
    assert len(get_current_datetime()) == 19
    assert len(get_tomorrow_datetime()) == 19
    assert len(get_current_date()) == 10


def test_get_index_from_cardinal_matches_known_mapping():
    """Map known cardinals to zero-based indexes and unknown to -1."""
    assert get_index_from_cardinal("first") == 0
    assert get_index_from_cardinal("third") == 2
    assert get_index_from_cardinal("fifth") == 4
    assert get_index_from_cardinal("unknown") == -1


def test_assert_show_message_raises_assertion_error_on_false():
    """Raise AssertionError when asserted condition is false."""
    raised = False
    try:
        assert_show_message(False, "failure")
    except AssertionError:
        raised = True
    assert raised is True