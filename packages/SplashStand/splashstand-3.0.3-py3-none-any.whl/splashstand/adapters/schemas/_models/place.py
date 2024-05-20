import typing as t
from decimal import Decimal
from uuid import UUID

from phonenumbers import PhoneNumber
from pydantic import HttpUrl
from sqlalchemy_utils import PhoneNumberType
from sqlalchemy_utils import URLType
from sqlmodel import Field
from sqlmodel import Relationship
from . import SchemaModel


class Place(SchemaModel, table=True):
    # google required
    address: str
    # google recommended
    telephone: PhoneNumber | None = Field(default=None, sa_type=PhoneNumberType)
    fax_number: PhoneNumber | None = Field(default=None, sa_type=PhoneNumberType)
    image: HttpUrl | None = Field(default=None, sa_type=URLType)
    logo: HttpUrl | None = Field(default=None, sa_type=URLType)
    photo: HttpUrl | None = Field(default=None, sa_type=URLType)
    # other
    event: list["Event"] | None = Relationship(  # type: ignore
        back_populates="location",
        sa_relationship_kwargs=dict(primaryjoin="Event.location_id==Place.id"),
    )
    content_location: list["CreativeWork"] | None = Relationship(  # type: ignore
        back_populates="content_location",
        sa_relationship_kwargs=dict(
            primaryjoin="CreativeWork.content_location_id==Place.id"
        ),
    )
    created_location: list["CreativeWork"] | None = Relationship(  # type: ignore
        back_populates="created_location",
        sa_relationship_kwargs=dict(
            primaryjoin="CreativeWork.created_location_id==Place.id"
        ),
    )
    contains_place: list["Place"] | None = Relationship(
        back_populates="contained_in_place",
    )
    contained_in_place_id: UUID | None = Field(default=None, foreign_key="place.id")
    contained_in_place: t.Optional["Place"] | None = Relationship(
        back_populates="contains_place",
        sa_relationship_kwargs=dict(remote_side="Place.id"),
    )
    slogan: str | None = Field(default=None)
    latitude: Decimal | None = Field(default=None)
    longitude: Decimal | None = Field(default=None)
    has_map: HttpUrl | None = Field(default=None, sa_type=URLType)
    public_access: bool = Field(default=False)
    is_accessible_for_free: bool = Field(default=False)
    maximum_attendee_capacity: int | None = Field(default=None)
    smoking_allowed: bool = Field(default=False)
