from typing import NoReturn
from shop.utils.basket import Basket
from shop.utils.funcs import (
    show_divider,
    clear_screen,
)
from config.log_config import config_logging

logger = config_logging()


def handle_count_command(basket: Basket) -> NoReturn:
    clear_screen()

    print(basket.count_items())
    logger.debug("User has seen the count of basket's item.")
    print(show_divider())
