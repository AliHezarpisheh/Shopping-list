from shop.utils.basket import Basket
from typing import NoReturn
from shop.utils.funcs import (
    show_divider,
    clear_screen,
)
from config.log_config import config_logging

logger = config_logging()


def handle_search_command(basket: Basket) -> NoReturn:
    clear_screen()

    item_for_search = input(
        "Enter the name of the product you're considering to search: "
    ).title()

    if item_for_search == "Back":
        clear_screen()
    else:
        message = basket.search_item(item_for_search)
        logger.debug("User searched his/her basket.")
        print(show_divider())
        print(message)

    print(show_divider())
