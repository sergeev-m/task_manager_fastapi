from fastapi import APIRouter

from src.auth.service import auth_service


router = APIRouter()


router.add_api_route("/login", auth_service.login_user, methods=["post"])
