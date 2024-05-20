from enum import Enum


class StatusCode(int, Enum):
    Ok = 0xAA
    Undefined = 0xB0
    InternalError = 0xCF
    BadRequest = 0xFA
    AuthError = 0xFB
    HashError = 0xFE
    NotFound = 0xFC
