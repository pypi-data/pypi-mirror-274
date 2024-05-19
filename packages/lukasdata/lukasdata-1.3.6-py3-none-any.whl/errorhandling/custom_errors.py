class CustomError(Exception):
    """Base class for other exceptions"""
    pass

class ValueTooHighError(CustomError):
    """Raised when the input value is too high"""
    def __init__(self, value, message="Value is too high"):
        self.value = value
        self.message = message
        super().__init__(self.message)

class ValueTooLowError(CustomError):
    """Raised when the input value is too low"""
    def __init__(self, value, message="Value is too low"):
        self.value = value
        self.message = message
        super().__init__(self.message)
