from enum import Enum

from phonenumbers import PhoneNumber
from pydantic import EmailStr
from pydantic import HttpUrl
from sqlalchemy import Column
from sqlalchemy_utils import ChoiceType
from sqlalchemy_utils import EmailType
from sqlalchemy_utils import PhoneNumberType
from sqlalchemy_utils import URLType
from sqlmodel import Field
from sqlmodel import Relationship
from . import SchemaModel


class Roles(str, Enum):
    admin = "admin"
    owner = "owner"
    editor = "editor"
    contributor = "contributor"
    user = "user"


# class Roles(BaseModel):
#     class User(BaseModel):
#         ...
#
#     class Contributor(User):
#         ...
#
#     class Editor(Contributor):
#         ...
#
#     class Owner(Editor):
#         ...
#
#     class Admin(Owner):
#         ...


class Person(SchemaModel, table=True):
    # app required
    gmail: EmailStr = Field(sa_type=EmailType)
    # google recommended
    url: HttpUrl | None = Field(default=None, sa_type=URLType)
    description: str | None = Field(default=None)
    image: HttpUrl | None = Field(default=None, sa_type=URLType)
    # other
    google_uid: str | None = Field(default=None)
    job_title: str | None = Field(default=None)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    telephone: PhoneNumber | None = Field(default=None, sa_type=PhoneNumberType)
    alternate_name: str | None = Field(default=None)
    address: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None, sa_type=EmailType)
    picture: HttpUrl | None = Field(default=None, sa_type=URLType)
    role: str = Field(default="user", sa_column=Column(ChoiceType(Roles)))
    creator_of: list["CreativeWork"] | None = Relationship(  # type: ignore
        back_populates="creator",
        sa_relationship_kwargs=dict(primaryjoin="CreativeWork.creator_id==Person.id"),
    )
    member_of: list["Organization"] | None = Relationship(  # type: ignore
        back_populates="member",
        sa_relationship_kwargs=dict(primaryjoin="Organization.member_id==Person.id"),
    )
    organizer_of: list["Event"] | None = Relationship(  # type: ignore
        back_populates="organizer",
        sa_relationship_kwargs=dict(primaryjoin="Event.organizer_id==Person.id"),
    )
    producer_of: list["CreativeWork"] | None = Relationship(  # type: ignore
        back_populates="producer",
        sa_relationship_kwargs=dict(primaryjoin="CreativeWork.producer_id==Person.id"),
    )

    # @hybrid_property
    # def author(self) -> t.Any:
    #     return self.creator
