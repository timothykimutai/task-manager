"""Utility functions for the task manager."""

from datetime import datetime
from typing import Optional
from colorama import Fore, Style


def colorize(text: str, color: str) -> str:
    """
    Colorize text using colorama.

    Args:
        text: Text to colorize
        color: Color to use (red, green, yellow, blue)

    Returns:
        Colorized text
    """
    colors = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
    }
    return f"{colors.get(color, Fore.WHITE)}{text}{Style.RESET_ALL}"


def format_datetime(dt: Optional[datetime], format_str: str = "%Y-%m-%d %H:%M") -> str:
    """
    Format datetime object to string.

    Args:
        dt: Datetime object to format
        format_str: Format string to use

    Returns:
        Formatted datetime string or empty string if dt is None
    """
    if dt is None:
        return ""
    return dt.strftime(format_str)


def format_priority(priority: str) -> str:
    """
    Format priority with color and symbol.

    Args:
        priority: Priority level (low, medium, high)

    Returns:
        Formatted priority string
    """
    symbols = {
        "low": "◦",
        "medium": "●",
        "high": "◉"
    }
    colors = {
        "low": "blue",
        "medium": "yellow",
        "high": "red"
    }
    symbol = symbols.get(priority, "●")
    return colorize(symbol, colors.get(priority, "white"))


def format_status(status: str) -> str:
    """
    Format status with color.

    Args:
        status: Status (pending, completed)

    Returns:
        Formatted status string
    """
    colors = {
        "pending": "yellow",
        "completed": "green"
    }
    return colorize(status, colors.get(status, "white"))


def format_category(category: Optional[str]) -> str:
    """
    Format category with color.

    Args:
        category: Category name or None

    Returns:
        Formatted category string
    """
    if not category:
        return ""
    return colorize(f"[{category}]", "cyan")


def format_reminder(reminder: Optional[datetime]) -> str:
    """
    Format reminder datetime.

    Args:
        reminder: Reminder datetime or None

    Returns:
        Formatted reminder string
    """
    if not reminder:
        return ""
    return colorize(f"⏰ {format_datetime(reminder)}", "yellow")
