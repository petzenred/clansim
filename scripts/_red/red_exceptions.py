# red_exceptions.py - Custom exceptions for ClanSim.

########################################################################################################################
# Imports
########################################################################################################################


########################################################################################################################
# Classes
########################################################################################################################

class BaseClanSimException(BaseException):
    """ Base class for ClanSim exceptions. """

    message: str

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"BaseClanSimException: {self.message}"


class InvalidAgeError(BaseClanSimException):
    """ Raised when a cat's age is invalid for what you're trying to do with it. """

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"InvalidAgeException: {self.message}"


class InvalidSaveError(BaseClanSimException):
    """ Raised when the game tries to load an invalid save. """

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"InvalidSaveError: {self.message}"


class InvalidFileTypeError(BaseClanSimException):
    """ Raised when the game tries to read/write a file type that it can't parse/write. """

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"InvalidFileTypeError: {self.message}"


class InitializationError(BaseClanSimException):
    """ Raised when an object that hasn't been fully initialized is used. """

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"InitializationError: {self.message}"


