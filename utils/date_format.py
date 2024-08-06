from datetime import datetime


def format_datetime(datetime_str: str) -> str:
    dt = datetime.fromisoformat(datetime_str)
    return dt.strftime('%H-%M')


def format_date(datetime_str: str) -> str:
    dt = datetime.fromisoformat(datetime_str)
    return dt.strftime('%d.%m.%Y')
