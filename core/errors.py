from pydantic.dataclasses import dataclass


# @dataclass
class CustomError(Exception):
    def __init__(self, status_code: int | None, detail):
        self.detail: str = detail
        self.status_code: int | None = status_code
        super().__init__(detail)


class AlreadyExistError(Exception):
    pass


class DBError(Exception):
    pass


class NoRowsFoundError(Exception):
    pass


class MultipleRowsFoundError(Exception):
    pass


class TokenError(Exception):
    pass
