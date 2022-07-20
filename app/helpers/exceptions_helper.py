
class BaseException(Exception):
    def __init__(self, TargetClass,message):
        self.TargetClass = TargetClass
        self.message = message

class ProductNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class UserNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
    
