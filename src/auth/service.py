from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from passlib.hash import argon2

from src.core.jwt.token import token_service
from src.auth.schemas import LoginUser
from src.users.errors import ValidationError
from src.users.service import user_service as us, UserService


oauth2 = OAuth2PasswordBearer(tokenUrl="/login")


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def login_user(self, model: LoginUser):
        user = await self.user_service.get_user_by_credentials(model.email)
        if not argon2.verify(model.password, user.password):
            raise ValidationError('Invalid password', HTTP_400_BAD_REQUEST)
        return token_service.create_tokens(user)

    async def get_current_user(self, token: Annotated[str, Depends(oauth2)]):
        if data := token_service.decode_token_or_none(token):
            return await self.user_service.retrieve(pk=data['user_id'])
        raise HTTPException(HTTP_401_UNAUTHORIZED, 'Unauthorized')

    @staticmethod
    async def get_current_user_permissions_by_token(token: Annotated[str, Depends(oauth2)]) -> list:
        if data := token_service.decode_token_or_none(token):
            return data['user_permissions']
        raise HTTPException(HTTP_401_UNAUTHORIZED, 'Unauthorized')

    @staticmethod
    async def get_user_id_by_token(
            token: Annotated[str, Depends(oauth2)]
    ) -> list | HTTPException:
        if data := token_service.decode_token_or_none(token):
            return data['user_id']
        raise HTTPException(HTTP_401_UNAUTHORIZED, 'Unauthorized')


auth_service = AuthService(us)
