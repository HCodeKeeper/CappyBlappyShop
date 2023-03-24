class EmptyTemporalRegistrationStorage(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    __doc__ = "Raised when trying to get registration data, although user haven't sent any"


class InvalidTokenFormatException(Exception):
    def __init__(self, message=None, token: str = 'not_specified'):
        self.message = message
        if self.message is None:
            self.message = f"({token}) is of invalid format"
        super().__init__(self.message)
