class UnopenedConnection(Exception):
    def __init__(self) -> None:
        super().__init__("Open connection before send packets")

class ClosedConnecton(Exception):
    def __init__(self, message: str = "Connection already closed") -> None:
        super().__init__(message)

class AuthException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class ProcedureError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)