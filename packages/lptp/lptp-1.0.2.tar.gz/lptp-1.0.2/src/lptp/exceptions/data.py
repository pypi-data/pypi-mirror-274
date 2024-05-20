from .base import RequestError
import lptp.types


class DataException(RequestError):
    def __init__(self, text: str = "") -> None:
        super().__init__(text, lptp.types.StatusCode.BadRequest)