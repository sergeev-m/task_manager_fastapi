from typing import Annotated

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBasicCredentials, HTTPBasic, OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED

from core.jwt.token import token_service
from core.service import BaseService
from src.auth.schemas import LoginUser
from src.users.errors import ValidationError
from src.users.schemas import User, UserCreate
from src.users.service import user_service as us, UserService


oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

type Token = Annotated[str, Depends(oauth2)]  # todo проверить


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def login_user(self, model: LoginUser):
        user = await self.user_service.get_user_by_credentials(model.email)
        if user.password != model.password:
            raise ValidationError('Invalid password')
        return token_service.create_tokens(user)

    async def get_current_user(self, token: Annotated[str, Depends(oauth2)]):
        if data := token_service.decode_token_or_none(token):
            return await self.user_service.retrieve(pk=data['user_id'])
        raise HTTPException(HTTP_401_UNAUTHORIZED, 'Unauthorized')

    @staticmethod
    async def get_current_user_permissions_from_token(token: Annotated[str, Depends(oauth2)]) -> list | HTTPException:  # todo rename get_user_permissions_by_token
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
