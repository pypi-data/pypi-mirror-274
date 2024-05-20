from uuid import UUID

from phonenumbers import PhoneNumber
from pydantic import EmailStr
from pydantic import HttpUrl
from sqlalchemy_utils import ArrowType
from sqlalchemy_utils import EmailType
from sqlalchemy_utils import PhoneNumberType
from sqlalchemy_utils import URLType
from sqlmodel import Field
from sqlmodel import Relationship
from . import SchemaModel
from .event import Event
from .person import Person


class Organization(SchemaModel, table=True):
    # google recommended
    alternate_name: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None, sa_type=EmailType)
    telephone: PhoneNumber | None = Field(default=None, sa_type=PhoneNumberType)
    image: HttpUrl | None = Field(default=None, sa_type=URLType)
    logo: HttpUrl | None = Field(default=None, sa_type=URLType)
    address: str | None = Field(default=None)
    founding_date: ArrowType | None = Field(default=None, sa_type=ArrowType)
    genre: str | None = Field(default=None)
    # other
    member_id: UUID | None = Field(  # many to many
        default=None, foreign_key="person.id"
    )
    member: Person | None = Relationship(
        back_populates="member_of",
        # sa_relationship_kwargs=dict(primaryjoin="Person.id==Organization.member_id"),
    )
    # album: list["CreativeWork"] | None = Relationship(  # type: ignore
    #     back_populates="by_artist",
    #     sa_relationship_kwargs=dict(
    #         primaryjoin="CreativeWork.by_artist_id==Organization.id"
    #     ),
    # )
    creative_work: list["CreativeWork"] | None = Relationship(  # type: ignore
        back_populates="by_artist",
        sa_relationship_kwargs=dict(
            primaryjoin="CreativeWork.by_artist_id==Organization.id"
        ),
    )
    performer_of: list[Event] | None = Relationship(  # type: ignore
        back_populates="performer",
        sa_relationship_kwargs=dict(primaryjoin="Event.performer_id==Organization.id"),
    )
