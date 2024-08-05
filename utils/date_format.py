from datetime import datetime


def format_datetime(datetime_str):
    # Parse the ISO 8601 formatted string
    dt = datetime.fromisoformat(datetime_str)
    # Format the datetime object to the desired format
    return dt.strftime('%H-%M')

def format_date(datetime_str: str) -> str:
    """Форматирует строку даты в удобочитаемый формат."""
    dt = datetime.fromisoformat(datetime_str)
    return dt.strftime('%d.%m.%Y')  # Формат даты, например, 05.08.2024
