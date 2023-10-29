class CustomError(Exception):
    def __init__(self, status_code: int | None, detail):
        self.detail: str = detail
        self.status_code: int | None = status_code
        super().__init__(detail)


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
