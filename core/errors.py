from pydantic.dataclasses import dataclass


@dataclass
class CustomError(Exception):
    error_message: str
    status_code: int | None = 500


class AlreadyExistError(CustomError):
    pass


class DBError(CustomError):
    pass


class NoRowsFoundError(CustomError):
    pass


class MultipleRowsFoundError(CustomError):
    pass


class TokenError(CustomError):
    pass
