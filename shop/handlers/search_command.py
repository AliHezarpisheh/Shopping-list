from typing import NoReturn
from shop.utils.funcs import (
    search_item,
    show_divider,
    clear_screen,
)
from shop.helpers.type_hints import (
    Basket
)
from config.log_config import config_logging

logger = config_logging()


def handle_search_command(basket: Basket) -> NoReturn:
    """Handle the 'search' command by allowing the user to search for a product in the shopping basket.

    Args:
        basket (Basket): The current shopping basket.

    Returns:
        NoReturn: This function does not return any value.
    """
    clear_screen()

    item_for_search = input(
        "Enter the name of the product you're considering to search: ").title()

    if item_for_search == "Back":
        clear_screen()
    else:
        message = search_item(basket, item_for_search)
        logger.debug("User searched his/her basket.")
        print(show_divider())
        print(message)

    print(show_divider())
