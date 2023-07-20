class ItemDoesNotExistError(ValueError):
    """ItemDoesNotExist: Raised when an item does not exist."""
    pass


class WrongOrderError(IndexError):
    """WrongOrderError: Raised when there is an incorrect order or index."""
    pass
