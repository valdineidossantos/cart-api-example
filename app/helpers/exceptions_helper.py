class GenericNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ProductNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class UserNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class DuplicatedItemException(Exception):
    def __init__(self, message):
        super().__init__(message)
