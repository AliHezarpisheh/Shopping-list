from typing import NoReturn
from shop.models.products import Product
from shop.utils.basket import Basket
from shop.utils.funcs import (
    title_and_strip_names,
    show_divider,
    clear_screen,
    guide_message,
)
from shop.helpers.exceptions import ItemDoesNotExistError
from config.log_config import config_logging

logger = config_logging()


def handle_add_command(basket: Basket) -> NoReturn:
    clear_screen()

    Product.show_all()
    print(show_divider())

    additional_items = input(
        "Enter the name(s) which represents the product(s) you're considering to add: "
    ).split(",")

    try:
        additional_items = title_and_strip_names(additional_items)
    except TypeError:
        logger.error(
            "Data type of the arguments were not correct. check title_and_strip_names function."
        )
        print(
            "Please try again entering the items. Be sure that you're entering valid items. Call the administrator if the issue is not solved."
        )

    if additional_items[0] == "Back":
        clear_screen()
    else:
        clear_screen()
        try:
            basket.add_items(additional_items)
        except ItemDoesNotExistError as error:
            print(error, "Type and Enter products for seeing products.")
        except Exception as error:
            logger.critical(error)
            print("Error 500! Call the Administrator.")
        print(guide_message())

    print(show_divider())
