from rest_framework.exceptions import NotFound, ValidationError

from sharing.core.exceptions import HandlerException, HandlerObjectNotFound


def handler_errors_for_api(func):
    """catch handler exceptions and raise rest_framework errors"""

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)

        except HandlerObjectNotFound as exc:
            raise NotFound(detail=exc)
        except HandlerException as exc:
            raise ValidationError(detail=exc)

        return result

    return wrapper
