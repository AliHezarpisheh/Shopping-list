import csv
from pathlib import Path
from collections import namedtuple
from typing import NamedTuple, Type, List, NoReturn
from shop.utils.funcs import title_and_strip_names, clear_screen
from shop.helpers.exceptions import ItemDoesNotExistError
from config.log_config import config_logging

logger = config_logging()

directory = Path.cwd()
file_path = directory / "shop" / "models" / "products.csv"

with file_path.open("r") as csv_file:
    csv_reader = csv.reader(csv_file)
    # Saving first line in column_names and discarding them in csv_reader.
    column_name = next(csv_reader)
    column_name = list(map(str.lower, column_name))

    # Defining a namedtuple with field names equivalent to column_names.
    BaseProduct: NamedTuple = namedtuple("BaseProduct", column_name, rename=True)

    class Product(BaseProduct):
        """A class representing a product.

        This class inherits from BaseProduct and adds some additional functionality
        to handle products. Products are created using the __new__ method to ensure
        proper data types. They can be added to the 'all' list and their price can be
        accessed as a float using the 'float_price' property. The 'show_all' method
        displays a paginated view of all the products, and the 'get_item' method allows
        retrieving products by their names. Products can be added to the 'all' list
        using the 'add_product' method.

        Attributes:
            all (List[Product]): A list to store all the created Product instances.
        """
        all = list()

        def __new__(
            cls, id: str, name: str, price: str, category: str, quantity: str
        ) -> Type["Product"]:
            """Create a new Product instance.

            This method creates a new Product instance with the given data. It converts
            'id' and 'quantity' to integers and returns the new instance.

            Args:
                id (str): The ID of the product.
                name (str): The name of the product.
                price (str): The price of the product as a string.
                category (str): The category of the product.
                quantity (str): The quantity of the product as a string.

            Returns:
                Product: The newly created Product instance.
            """
            id = int(id)
            quantity = int(quantity)

            return super().__new__(cls, id, name, price, category, quantity)

        @property
        def float_price(self) -> float:
            """Get the product price as a float.

            This property returns the price of the product as a floating-point number
            after removing the dollar sign from the price string.

            Returns:
                float: The price of the product as a float.
            """
            removed_dollar_sing = self.price.replace("$", "")
            return float(removed_dollar_sing)

        @classmethod
        def show_all(cls) -> NoReturn:
            """Display all products in a paginated view.

            This method displays all the products stored in the 'all' list in a
            paginated view. The products are grouped into pages, with each page
            displaying up to 5 products. The user can navigate through pages using
            the 'n' (next), 'p' (previous), or 'q' (quit) commands in the console.
            """
            products_count = len(cls.all)
            total_pages = (
                products_count // 5
                if products_count % 5 == 0
                else (products_count // 5) + 1
            )

            page = 1
            while True:
                clear_screen()
                products_on_current_page = cls.all[(page - 1) * 5 : page * 5]

                for product in products_on_current_page:
                    print(f"{product.id}. {product.name}, price: {product.price} in {product.category} category.")
                print(f"Page {page}/{total_pages}\n")

                if page in range(2, total_pages):
                    next_or_previous = input("[n/p]|q for quit: ").lower()
                    if next_or_previous == "n":
                        page += 1
                    elif next_or_previous == "p":
                        page -= 1
                    elif next_or_previous == "q":
                        break
                    else:
                        continue

                elif page == 1:
                    next_or_previous = input("[n]|q for quit: ").lower()
                    if next_or_previous == "n":
                        page += 1
                    elif next_or_previous == "q":
                        break
                    else:
                        continue

                elif page == total_pages:
                    next_or_previous = input("[p]|q for quit: ").lower()
                    if next_or_previous == "p":
                        page -= 1
                    elif next_or_previous == "q":
                        break
                    else:
                        continue

        @classmethod
        def get_item(
            cls, item_names: List[str]
        ) -> List[Type["Product"]] | ItemDoesNotExistError:
            """Get products based on their names.

            Args:
                item_names (List[str]): A list of item names to search for.

            Returns:
                List[Product]: A list of products that match the given item names.

            Raises:
                ItemDoesNotExistError: If any item name does not exist in the products list.
            """
            for item in item_names:
                for product in cls.all:
                    if item == product.name:
                        break
                else:
                    logger.info(f"{item} was not defined in the products list.")
                    raise ItemDoesNotExistError(
                        f"{item} does not exist in the products(Pay attention to the spelling of words)."
                    )

            return list(filter(lambda item: item.name in item_names, cls.all))

        def add_product(self) -> NoReturn:
            """Add the product to the 'all' list."""
            self.__class__.all.append(self)

    # Storing products
    for row in csv_reader:
        row = title_and_strip_names(row)
        try:
            product = Product(*row)
            product.add_product()
        except TypeError as error:
            logger.critical(error)
            print("Error 500! Call the Administrator.")
