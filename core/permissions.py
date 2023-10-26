from abc import ABC, abstractmethod

from core.models import Base


class AbstractPermission[UserModel: Base](ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def check_permissions(self, user: UserModel) -> UserModel:
        raise NotImplementedError
