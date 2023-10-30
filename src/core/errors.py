# class CustomError(Exception):
#     def __init__(self, status_code: int | None = 500, detail):
#         self.status_code: int | None = status_code
#         self.detail: str = detail
#         super().__init__(detail)


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
