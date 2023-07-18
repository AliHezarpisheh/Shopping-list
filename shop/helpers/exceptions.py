class ItemDoesNotExist(ValueError):
    pass


class ProductFileDoesNotExist(FileExistsError):
    pass


class WrongOrderError(IndexError):
    pass
