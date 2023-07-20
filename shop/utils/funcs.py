import os
from typing import NoReturn, List
from config.log_config import config_logging

logger = config_logging()


def title_and_strip_names(names: List[str]) -> List[str]:
    """Converts all names in the list to title case and removes whitespaces from the the start and end of the names and returns the updated list."""
    names = list(map(str.title, names))
    names = list(map(str.strip, names))

    return names


def show_divider() -> str:
    """Return a string representing a divider."""
    return "--------"


def show_help() -> str:
    """
    Provide a help message with instructions for using the shopping store.

    Returns:
        str: The help message.
    """
    message = """
For viewing the products of the store please enter: products
For adding item(s) please enter: add
For removing item(s) please enter: remove
For searching the existence of your item please enter: search
For changing the priority of an item please enter: prioritize
To see how many products you have on your basket please enter: count
For showing your basket please enter: show
For returning back to the last step please enter: back
for showing this guideline again please enter: help
For finishing and quitting our store please enter: quit

ATTENTION: PUT ',' BETWEEN ITEMS WHEN ADDING OR REMOVING.
"""
    logger.debug("User viewed help successfully.")

    return message


def guide_message() -> str:
    """Return a guide message for commands."""
    message = "\nEnter help to see a guide for commands."
    return message


def clear_screen() -> NoReturn:
    """Clear the screen."""
    os.system("cls" if os.name == "nt" else "clear")
