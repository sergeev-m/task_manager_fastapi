from typing import Annotated

from fastapi import APIRouter, Depends
from uuid import UUID

from core.jwt.token import token_service
from src.users.schemas import UserCreate, User
from src.users.service import UserService, user_service
from src.auth.service import auth_service, AuthService, oauth2
from src.users.permissions import is_admin, is_user, is_authenticated

user_router = APIRouter(tags=['User'])
protected_router = APIRouter(tags=['Protected Router'])


protected_router.add_api_route('/user/me', auth_service.get_current_user, response_model=User)

# TODO permissions ??


@user_router.post('/user', response_model=User)
async def create_user(user: UserCreate, perm: Annotated[is_admin, Depends()]):
    return await user_service.create(user.model_dump())


@user_router.get('/user', response_model=list[User])
async def get_all():
    return await user_service.all()


@protected_router.get('/user/{pk}', response_model=User)
async def get_user_retrieve(pk: UUID, perm: Annotated[is_admin, Depends()]):
    return await user_service.get_one(id=pk)
