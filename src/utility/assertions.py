import logging


def assert_show_message(assertion_value, message: str) -> None:
    """Assert a condition and log the assertion message on failure."""
    try:
        assert assertion_value, message
    except AssertionError as error:
        logging.error(f'[Assert Error] {error}')
        raise
