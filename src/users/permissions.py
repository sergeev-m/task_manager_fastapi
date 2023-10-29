from fastapi import Depends, HTTPException

from core.permissions import AbstractPermission
from src.auth.service import auth_service
from src.users.models import User


class Permission(AbstractPermission):
    def __init__(self, permissions: set[str]):
        self.permissions = permissions

    # def __call__(self, user: User = Depends(auth_service.get_current_user)):
    #     return self.check_permissions(user)

    def __call__(self, data: list = Depends(auth_service.get_current_user_permissions_from_token)):
        if 'is_authenticated' in self.permissions:
            return True
        return self.check_permissions(data)

    def check_permissions(self, data: list) -> bool | HTTPException:
        for permission in data:
            if permission in self.permissions:
                return True

    # def check_permissions(self, user: User) -> User | HTTPException:
    #     for permission in user.permissions:
    #         if permission.codename in self.permissions:
    #             return user

        raise HTTPException(status_code=403, detail="User doesn't have enough rights")


is_user = Permission({"user"})
is_admin = Permission({"admin"})
is_authenticated = Permission({'is_authenticated'})


# is_authenticated = auth_service.get_current_user_permissions_from_token and auth_service.get_current_user
# is_authenticated = auth_service.get_current_user


def allow_any():
    pass

# todo доделать