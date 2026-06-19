import datetime


def get_current_datetime() -> str:
    """Return local date-time in ISO-like format without timezone suffix."""
    today = datetime.datetime.today().astimezone()
    return today.strftime('%Y-%m-%dT%H:%M:%S')


def get_current_date() -> str:
    """Return local date in YYYY-MM-DD format."""
    today = datetime.datetime.today().astimezone()
    return today.strftime('%Y-%m-%d')


def get_tomorrow_datetime() -> str:
    """Return local date-time for tomorrow in ISO-like format without timezone suffix."""
    today = datetime.datetime.today().astimezone()
    tomorrow = today + datetime.timedelta(days=1)
    return tomorrow.strftime('%Y-%m-%dT%H:%M:%S')
