from enum import IntEnum, StrEnum


class GeoAPIStatus(StrEnum):
    SUCCESS = "success"
    FAIL = "fail"


class HTTPStatusCode(IntEnum):
    OK = 200
    BAD_REQUEST = 400
