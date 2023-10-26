from datetime import datetime, timedelta, UTC

from jwt import ExpiredSignatureError, PyJWTError, decode, encode

from core.config.jwt import config_token
from core.config.settings import settings
from core.jwt.base import AbstractToken
from core.errors import TokenError
from src.users.schemas import User


class TokenService(AbstractToken):
    secret_key = settings.secret_key
    algorithm = config_token.ALGORITHM
    access_token_lifetime = config_token.ACCESS_TOKEN_LIFETIME
    refresh_token_lifetime = config_token.REFRESH_TOKEN_LIFETIME
    refresh_token_rotate_min_lifetime = config_token.REFRESH_TOKEN_ROTATE_MIN_LIFETIME

    def create_tokens(self, user: User) -> dict:
        access_token = self.generate_access_token(user)
        refresh_token = self.generate_refresh_token(user)
        return {"access": access_token, "refresh": refresh_token}

    def generate_access_token(self, user: User):
        expire = datetime.now(UTC) + timedelta(minutes=self.access_token_lifetime)
        payload = {
            "token_type": "access",
            "user_id": str(user.id),
            "user_permissions": [permission.codename for permission in user.permissions],
            "exp": expire,
        }
        return self._encode_token(payload)

    def generate_refresh_token(self, user: User):
        expire = datetime.now(UTC) + timedelta(minutes=self.refresh_token_lifetime)
        payload = {
            "token_type": "refresh",
            "user_id": str(user.id),
            "user_permissions": [permission.codename for permission in user.permissions],
            "exp": expire,
        }
        return self._encode_token(payload)

    def decode_token_or_none(self, token: str) -> dict | None:
        try:
            return self._decode_token(token)
        except TokenError:
            return

    def _encode_token(self, payload: dict) -> str:
        return encode(payload, self.secret_key, self.algorithm)

    def _decode_token(self, token: str) -> dict:
        try:
            return decode(token, self.secret_key, self.algorithm)
        except ExpiredSignatureError:
            raise TokenError("Token lifetime has expired")
        except PyJWTError:
            raise TokenError("Token is invalid")


token_service = TokenService()
