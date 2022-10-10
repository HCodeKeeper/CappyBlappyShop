class EmptyCartException(Exception):
    def __init__(self, message):
        self.message = message
        super.__init__(self.message)

    __doc__ = "Called when a user tries to checkout with empty cart"
