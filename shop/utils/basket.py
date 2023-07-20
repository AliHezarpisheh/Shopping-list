from typing import NoReturn, List, Union, Type
from shop.utils.decorators import apply_tax
from shop.models.products import Product
from shop.helpers.exceptions import ItemDoesNotExistError, WrongOrderError
from config.log_config import config_logging

logger = config_logging()


class Basket:
    """
    The Basket class represents a user's shopping basket.

    Attributes:
        _instance (Union[None, Type[Basket]]): Singleton instance of the Basket class.
        basket (list): List to store the products in the basket.
    """

    _instance: Union[None, Type["Basket"]] = None
    basket = list()

    def __new__(cls, *args, **kwargs) -> Type["Basket"]:
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def add_items(self, item_names: List[str]) -> NoReturn:
        """Add items to the basket.

        Parameters:
            item_names (List[str]): A list of product names to be added to the basket.

        Returns:
            NoReturn: This method does not return anything.
        """
        new_products = Product.get_item(item_names)

        for product in new_products:
            product = product._asdict()
            is_found = False

            for item in self.basket:
                if product["name"] == item["name"]:
                    is_found = True
                    item["unit"] += 1

                    logger.debug(
                        f"{item['name']} unit has been increased by 1 in user's basket."
                    )
                    print(f"{item['name']} unit has been increased by 1.")

            if not is_found:
                product["unit"] = 1
                self.basket.append(product)

                logger.debug(f"{product['name']} has been added to user's basket.")
                print(f"{product['name']} has been added to your basket!")

    def remove_items(self, item_names: List[str]) -> NoReturn:
        """
        Remove items from the basket.

        Parameters:
            item_names (List[str]): A list of product names to be removed from the basket.

        Raises:
            ItemDoesNotExistError: If one or more item names do not exist in the basket.
            WrongOrderError: If the new_index provided is out of the valid range.
        """
        item_names = [
            name
            for name in item_names
            if any(name == item_name.get("name") for item_name in self.basket)
        ]
        for item in self.basket:
            if item["name"] in item_names:
                if item["unit"] > 1:
                    item["unit"] -= 1
                    item_names.remove(item["name"])
                    print(f"{item['name']} unit has been decreased by 1.")

        self.basket = list(
            filter(lambda item: item["name"] not in item_names, self.basket)
        )

        for item in item_names:
            print(f"{item} has been deleted from your basket!")

    def change_index(
        self, item_name: str, new_index: int
    ) -> NoReturn | ItemDoesNotExistError | WrongOrderError:
        """
        Change the position of an item in the basket.

        Parameters:
            item_name (str): The name of the item to be moved.
            new_index (int): The new index to which the item will be moved (1-based index).

        Raises:
            ItemDoesNotExistError: If the specified item name does not exist in the basket.
            WrongOrderError: If the new_index provided is out of the valid range.
        """
        if (new_index > len(self.basket)) or (new_index <= 0):
            logger.info(
                f"The considered order({new_index}) does not exist in user's basket."
            )
            raise WrongOrderError(
                f"The considered order({new_index}) does not exist in basket."
            )

        for item in self.basket:
            if item["name"] == item_name:
                self.basket.remove(item)
                self.basket.insert(new_index - 1, item)

                print(f"{item['name']} has been moved to the {new_index}rd place!")
                logger.debug(
                    f"{item['name']} has been moved to the {new_index}rd place in user's basket."
                )
                break
        else:
            logger.info(
                f"{item_name} was not in customer's basket while changing index"
            )
            raise ItemDoesNotExistError(
                f"{item_name} does not exist in your basket(Pay attention to the spelling of words)."
            )

    def search_item(self, item_name: str) -> str:
        """
        Search for a specific item in the basket.

        Parameters:
            item_name (str): The name of the item to search for in the basket.

        Returns:
            str: A message indicating whether the item is in the basket or not.
        """
        message = "Your considered item is not in your basket."
        for item in self.basket:
            if item["name"] == item_name:
                message = "Your considered item is in your basket."
        logger.debug("User searched basket successfully.")

        return message

    def count_items(self) -> str:
        """
        Count the number of distinct products in the basket.

        Returns:
            str: A message with the count of distinct products in the basket, or a message indicating an empty basket.
        """
        if len(self.basket) == 0:
            message = "You have no items in your basket."
        message = f"You have {len(self.basket)} distinct product in your basket."
        message += "\nTo view more details of your basket, please enter: show"
        logger.debug("Counted successfully.")

        return message

    @apply_tax
    def show(self) -> str:
        """
        Show the contents of the basket, including prices and categories.

        Returns:
            str: A formatted string representation of the items in the basket with their prices and categories.
        """
        result = "This is your basket:"
        if len(self.basket) == 0:
            result += "\nYou have nothing in your basket! Type and Enter add for adding some products."
        for item in self.basket:
            result += f"\n-{item['name']}: {item['unit']} in your basket, price: {item['price']}, category: {item['category']}."

        return result
