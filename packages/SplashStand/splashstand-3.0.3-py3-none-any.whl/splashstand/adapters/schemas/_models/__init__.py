import typing as t
from datetime import date
from datetime import time
from datetime import timedelta
from uuid import UUID

import arrow
import uuid_utils
from acb.adapters import import_adapter
from acb.debug import debug
from acb.depends import depends
from inflection import titleize
from inflection import underscore
from pydantic import BaseModel
from pydantic import HttpUrl
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import ArrowType
from sqlalchemy_utils import ChoiceType
from sqlalchemy_utils import ColorType
from sqlalchemy_utils import CountryType
from sqlalchemy_utils import CurrencyType
from sqlalchemy_utils import EmailType
from sqlalchemy_utils import LocaleType
from sqlalchemy_utils.types import PhoneNumberType
from sqlalchemy_utils.types import URLType
from sqlmodel import Field
from sqlmodel import or_
from sqlmodel import select
from sqlmodel import SQLModel

auth = depends.get(import_adapter("auth"))

data_type_map = dict(
    Boole=bool,
    Date=date,
    DateTime=ArrowType,
    Duration=timedelta,
    Time=time,
    Number=float,
    Integer=int,
    Float=float,
    Text=str,
    CssSelectorType=str,
    PronounceableText=str,
    URL=URLType,
    XPathType=str,
    choice=ChoiceType,
    email=EmailType,
    currency=CurrencyType,
    phonenumber=PhoneNumberType,
    country=CountryType,
    locale=LocaleType,
    color=ColorType,
)


def primary_key_factory() -> t.Any:
    return UUID(str(uuid_utils.uuid7()))


class ThingMixin(BaseModel, extra="allow", arbitrary_types_allowed=True):
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    url: HttpUrl | None = Field(default=None, sa_type=URLType)
    same_as: HttpUrl | None = Field(default=None, sa_type=URLType)
    visible: bool = Field(default=True, exclude=True)


class SchemaModel(SQLModel, ThingMixin):  # type: ignore
    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {"eager_defaults": True}
    id: t.Optional[UUID] = Field(default_factory=primary_key_factory, primary_key=True)
    date_created: t.Optional[ArrowType] = Field(
        default_factory=arrow.utcnow, alias="created_at", sa_type=ArrowType
    )
    date_modified: t.Optional[ArrowType] = Field(
        default_factory=arrow.utcnow,
        alias="last_edited_at",
        sa_type=ArrowType,
        sa_column_kwargs=dict(onupdate=arrow.utcnow),
    )
    maintainer: t.Optional[str] = Field(
        default_factory=lambda: auth.current_user.identity, alias="created_by"
    )
    editor: t.Optional[str] = Field(
        default_factory=lambda: auth.current_user.identity,
        sa_column_kwargs=dict(onupdate=lambda: auth.current_user.identity),
        alias="last_edited_by",
    )

    @classmethod  # type: ignore
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:  # type: ignore
        return underscore(cls.__name__)

    def __str__(self) -> str:
        return getattr(self, "name") or titleize(self.__class__.__name__)

    async def save(self) -> None:
        sql = depends.get(import_adapter("sql"))
        async with sql.get_session() as session:
            session.add(self)
            await session.commit()

    @classmethod
    async def query(cls, *args: str, _or: bool = False) -> t.Any:
        sql = depends.get(import_adapter("sql"))
        statement = select(cls)
        debug(args)
        args = [a.replace(cls.__name__, "cls") for a in args]  # type: ignore
        _args = []
        for arg in args:
            _m = []
            for m in arg.split(" "):
                if m[0].isupper() and m != cls.__name__:
                    m = m.replace(m, f"depends.get(Models).{m}")
                _m.append(m)
            _args.append(" ".join(_m))
        debug(_args)
        _queries = [eval(_arg) for _arg in _args]  # nosec
        if args:
            statement = select(cls).where(*_queries)
            if _or:
                statement = select(cls).where(or_(*_queries))
        async with sql.get_session() as session:
            await session.flush()
            result = await session.exec(statement)
            debug(type(result))
            debug(result)
            return result
            # return await session.exec(statement)
