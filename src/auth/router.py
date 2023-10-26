from fastapi import APIRouter, Depends

from src.auth.schemas import LoginUser
from src.auth.service import auth_service

auth_router = APIRouter(tags=['Auth'])

auth_router.add_api_route("/login", auth_service.login_user, methods=["post"])
