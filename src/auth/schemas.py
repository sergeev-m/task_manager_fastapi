from pydantic import BaseModel

from src.users.schemas import EmailMixin, PasswordMixin


class LoginUser(BaseModel, EmailMixin, PasswordMixin):
    pass
