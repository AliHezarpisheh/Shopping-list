import os
from typing import NoReturn


def show_divider() -> str:
    """Return a string representing a divider."""
    return "--------"


def clear_screen() -> NoReturn:
    """Clear the screen."""
    os.system("cls" if os.name == "nt" else "clear")
