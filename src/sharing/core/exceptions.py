class HandlerException(Exception):
    """
    Error handling is done with exceptions. This class is the base of all exceptions raised by handlers
    """

    pass


class HandlerObjectNotFound(HandlerException):
    """
    Exception raised when a non-existing object is requested (when backend API replies with a 404 HTML status)
    """

    pass
