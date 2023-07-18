from typing import NoReturn
from shop.utils.funcs import (
    count_items,
    show_divider,
    clear_screen,
)
from shop.helpers.type_hints import Basket
from config.log_config import config_logging

logger = config_logging()


def handle_count_command(basket: Basket) -> NoReturn:
    """Handle the 'count' command by displaying the number of items in the shopping basket."""
    clear_screen()
    print(count_items(basket))
    logger.debug("User has seen the count of basket's item.")
    print(show_divider())
