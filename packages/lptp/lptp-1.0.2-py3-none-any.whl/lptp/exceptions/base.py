import lptp.types


class RequestError(Exception):
    def __init__(self,  text: str = "", status_code: "lptp.types.StatusCode" = None) -> None:
        super().__init__(text)
        if not status_code: status_code = lptp.types.StatusCode.BadRequest
        self.status_code = status_code