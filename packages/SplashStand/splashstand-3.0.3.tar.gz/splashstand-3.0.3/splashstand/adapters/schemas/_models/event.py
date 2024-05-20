import typing as t
from datetime import time
from uuid import UUID

from pydantic import HttpUrl
from sqlalchemy_utils import ArrowType
from sqlalchemy_utils import URLType
from sqlmodel import Field
from sqlmodel import Relationship
from . import SchemaModel
from .person import Person


class Event(SchemaModel, table=True):  # alias show
    # google required
    start_date: ArrowType = Field(sa_type=ArrowType)
    url: HttpUrl | None = Field(default=None, sa_type=URLType)
    location_id: UUID | None = Field(default=None, foreign_key="place.id")
    location: t.Optional["Place"] | None = Relationship(  # type: ignore
        back_populates="event",
        # sa_relationship_kwargs=dict(primaryjoin="Place.id==Event.location_id"),
    )
    # google recommended
    description: str | None = Field(default=None)
    end_date: ArrowType | None = Field(default=None, sa_type=ArrowType)
    time: time
    door_time: t.Optional[time] = Field(default=None)  # type: ignore
    image: HttpUrl | None = Field(default=None, sa_type=URLType)
    performer_id: UUID | None = Field(default=None, foreign_key="organization.id")
    performer: t.Optional["Organization"] | None = Relationship(  # type: ignore
        back_populates="performer_of",
        sa_relationship_kwargs=dict(primaryjoin="Organization.id==Event.performer_id"),
    )
    organizer_id: UUID | None = Field(default=None, foreign_key="person.id")
    organizer: Person | None = Relationship(
        back_populates="organizer_of",
        sa_relationship_kwargs=dict(primaryjoin="Person.id==Event.organizer_id"),
    )
    # organizer_id: UUID | None = Field(default=None, foreign_key="organization.id")
    # organizer: t.Optional["Organization"] | None = Relationship(  # type: ignore
    #     back_populates="organizer_of",
    #     sa_relationship_kwargs=dict(primaryjoin="Organization.id==Event.organizer_id"),
    # )
    recorded_in: list["CreativeWork"] | None = Relationship(  # type: ignore
        back_populates="recorded_at",
        sa_relationship_kwargs=dict(
            primaryjoin="CreativeWork.recorded_at_id==Event.id"
        ),
    )
