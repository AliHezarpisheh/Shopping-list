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


def handle_remove_command(basket: Basket):
    clear_screen()

    items, _ = basket.show()
    print(items)
    print(show_divider())

    items_to_delete = input(
        "Enter the name(s) which represents the product(s) you're considering to remove: "
    ).split(",")

    try:
        items_to_delete = title_and_strip_names(items_to_delete)
    except TypeError:
        logger.error(
            "Data type of the arguments were not correct. check title_and_strip_names function."
        )
        print(
            "Please try again entering the items. Be sure that you're entering valid items. Call the administrator if the issue is not solved."
        )

    if items_to_delete[0] == "Back":
        clear_screen()
    else:
        clear_screen()
        try:
            basket.remove_items(items_to_delete)
        except ItemDoesNotExistError as error:
            print(error, "Type and Enter show for seeing your basket.")
        except Exception as error:
            logger.critical(error)
            print("Error 500! Call the Administrator.")
        print(guide_message())

    print(show_divider())
