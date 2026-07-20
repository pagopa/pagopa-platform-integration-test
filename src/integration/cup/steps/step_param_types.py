from behave import register_type
from parse import with_pattern


@with_pattern(r".*")
def parse_any_text(text):
    return text or None


register_type(AnyText=parse_any_text)
