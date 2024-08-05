from datetime import datetime


def format_datetime(datetime_str):
    # Parse the ISO 8601 formatted string
    dt = datetime.fromisoformat(datetime_str)
    # Format the datetime object to the desired format
    return dt.strftime('%H-%M')

