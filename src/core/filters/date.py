from datetime import datetime
from typing import Union


__all__ = [
    "create_datetime",
    "format_datetime",
    "create_api_date",
    "format_date_pretty",
    "format_month_year",
]


def create_datetime(date_str: str) -> datetime:
    """Create a datetime object from an ISO date string."""
    return datetime.strptime(date_str.strip(), "%Y-%m-%d")


def format_datetime(date_obj: datetime) -> str:
    """Format a date as YYYY-MM-DD."""
    return date_obj.strftime("%Y-%m-%d")


def create_api_date(date_str: str) -> datetime:
    """Create a datetime object from an API response date string.

    E.g, Tue, 02 Jul 2019 00:00:00 GMT
    """
    return datetime.strptime(date_str.strip(), "%a, %d %b %Y 00:00:00 GMT")


def format_date_pretty(date_obj: datetime) -> str:
    """Pretty format a date in MM DD, YYYY."""
    return date_obj.strftime("%B %d, %Y")


def format_month_year(date: Union[str, datetime]) -> str:
    """Format a date as MM YYYY."""
    # If the date is provided as a string, conver it to a datetime obj
    if isinstance(date, str):
        # Add in a dummy day if needed
        if len(date.split("-")) == 2:
            date = f"{date}-01"
        date = create_datetime(date)
    return date.strftime("%B %Y")