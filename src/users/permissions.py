from fastapi import Depends, HTTPException

from src.auth.service import auth_service


class Permission:
    def __init__(self, permissions: set[str]):
        self.permissions = permissions

    def __call__(self, data: list = Depends(auth_service.get_current_user_permissions_from_token)):
        return self.check_permissions(data)

    def check_permissions(self, data: list) -> bool | HTTPException:
        for permission in data:
            if permission in self.permissions:
                return True

        raise HTTPException(status_code=403, detail="User doesn't have enough rights")


is_user = Permission({"user"})
is_admin = Permission({"admin"})
is_authenticated = bool(auth_service.get_user_id_by_token)


def allow_any():
    pass
