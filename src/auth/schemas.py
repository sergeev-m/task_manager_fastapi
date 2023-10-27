from src.users.schemas import EmailMixin, PasswordMixin


class LoginUser(EmailMixin, PasswordMixin):
    pass
