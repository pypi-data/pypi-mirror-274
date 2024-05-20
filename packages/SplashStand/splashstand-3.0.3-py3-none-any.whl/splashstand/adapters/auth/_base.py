import typing as t
from abc import ABC
from abc import abstractmethod
from contextvars import ContextVar

from acb.config import Settings
from pydantic import EmailStr
from acb.adapters import AdapterBase
from pydantic import SecretStr
from sqlmodel import SQLModel
from starlette.requests import Request
from starlette.authentication import UnauthenticatedUser


class AuthBaseSettings(Settings):
    token_id: t.Optional[str] = None
    session_cookie: t.Optional[str] = None


class AuthBase(AdapterBase, ABC):
    _current_user: ContextVar[t.Any] = ContextVar(
        "current_user", default=UnauthenticatedUser()
    )

    @property
    def current_user(self) -> t.Any:
        return self._current_user.get()

    @abstractmethod
    async def authenticate(self, request: Request) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __init__(self, secret_key: SecretStr, user_model: SQLModel) -> None:
        raise NotImplementedError

    @abstractmethod
    async def init(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def login(self, request: Request) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def logout(self, request: Request) -> bool:
        raise NotImplementedError


class AuthBaseUser(ABC):
    @abstractmethod
    def has_role(self, role: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_role(self, role: str) -> str | bool | None:
        raise NotImplementedError

    @property
    @abstractmethod
    def identity(self) -> str | None:
        raise NotImplementedError

    @property
    @abstractmethod
    def display_name(self) -> str | None:
        raise NotImplementedError

    @property
    @abstractmethod
    def email(self) -> EmailStr | None:
        raise NotImplementedError

    @abstractmethod
    def is_authenticated(
        self, request: t.Optional[Request] = None, config: t.Any = None
    ) -> bool | int | str:
        raise NotImplementedError
