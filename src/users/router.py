from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED

from core.log import log
from src.users.schemas import User
from src.users.service import user_service
from src.auth.service import auth_service


router = APIRouter()


router.add_api_route(
    '/register', user_service.create_user, response_model=User, methods={'post'},
    status_code=HTTP_201_CREATED
)
router.add_api_route(
    '/about_me', auth_service.get_current_user, response_model=User, methods={'get'}
)
