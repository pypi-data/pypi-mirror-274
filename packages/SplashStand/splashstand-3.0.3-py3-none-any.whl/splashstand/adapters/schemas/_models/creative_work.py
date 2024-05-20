from datetime import time
from datetime import timedelta
from enum import Enum
from uuid import UUID

from pydantic import HttpUrl
from sqlalchemy import Column
from sqlalchemy_utils import ArrowType
from sqlalchemy_utils import ChoiceType
from sqlalchemy_utils import URLType
from sqlmodel import Field
from sqlmodel import Relationship
from . import SchemaModel
from .event import Event
from .organization import Organization
from .person import Person
from .place import Place


class MusicAlbumProductionType(str, Enum):
    LiveAlbum = "LiveAlbum"
    StudioAlbum = "StudioAlbum"
    CompilationAlbum = "CompilationAlbum"
    DemoAlbum = "DemoAlbum"
    RemixAlbum = "RemixAlbum"
    DJMixAlbum = "DJMixAlbum"
    SoundtrackAlbum = "SoundtrackAlbum"


class MusicAlbumReleaseType(str, Enum):
    AlbumRelease = "AlbumRelease"
    BroadcastRelease = "BroadcastRelease"
    EPRelease = "EPRelease"
    SingleRelease = "SingleRelease"


class CreativeWork(SchemaModel, table=True):
    credit_text: str | None = Field(default=None)
    date_published: ArrowType | None = Field(default=None, sa_type=ArrowType)
    schema_version: str | None = Field(default=None)
    alternative_headline: str | None = Field(default=None)
    start_offset: int = Field(default=0)
    end_offset: int | None = Field(default=None)
    # google required
    content_url: HttpUrl = Field(sa_type=URLType)
    embed_url: HttpUrl = Field(sa_type=URLType)
    # google recommended
    thumbnail_url: HttpUrl = Field(default=None, sa_type=URLType)
    copyright_notice: str | None = Field(default=None)
    content_size: str | None = Field(default=None)
    encoding_format: str | None = Field(default=None)
    caption: str | None = Field(default=None)
    width: str | None = Field(default=None)
    height: str | None = Field(default=None)
    start_time: time | None = Field(default=0)
    end_time: time | None = Field(default=None)
    duration: timedelta | None = Field(default=None)
    bitrate: str | None = Field(default=None)
    in_language: str | None = Field(default=None)
    # other
    article_body: str | None = Field(default=None)
    word_count: int | None = Field(default=None)
    num_tracks: int | None = Field(default=None)
    isrc_code: str | None = Field(default=None)

    album_production_type: str | None = Field(
        sa_column=Column(ChoiceType(MusicAlbumProductionType))
    )
    album_release_type: str | None = Field(
        sa_column=Column(ChoiceType(MusicAlbumReleaseType))
    )
    # has_part: list["CreativeWork"] | None = Relationship(
    #     back_populates="clip",
    #     # sa_relationship_kwargs=dict(
    #     #     primaryjoin="CreativeWork.id==CreativeWork.clip_id"
    #     # ),
    # )
    # clip_id: UUID | None = Field(default=None, foreign_key="creative_work.id")
    # clip: t.Optional["CreativeWork"] | None = Relationship(
    #     back_populates="has_part",
    #     sa_relationship_kwargs=dict(
    #         primaryjoin="CreativeWork.clip_id==CreativeWork.id"
    #     ),
    #     # sa_relationship_kwargs=dict(remote_side="CreativeWork.id"),
    # )
    by_artist_id: UUID | None = Field(default=None, foreign_key="organization.id")
    by_artist: Organization | None = Relationship(
        back_populates="creative_work",
        sa_relationship_kwargs=dict(
            primaryjoin="Organization.id==CreativeWork.by_artist_id"
        ),
    )
    creator_id: UUID | None = Field(default=None, foreign_key="person.id")
    creator: Person | None = Relationship(
        back_populates="creator_of",
        sa_relationship_kwargs=dict(primaryjoin="Person.id==CreativeWork.creator_id"),
    )
    producer_id: UUID | None = Field(default=None, foreign_key="person.id")
    producer: Person | None = Relationship(
        back_populates="producer_of",
        sa_relationship_kwargs=dict(primaryjoin="Person.id==CreativeWork.producer_id"),
    )
    image: HttpUrl | None = Field(default=None, sa_type=URLType)
    video: HttpUrl | None = Field(default=None, sa_type=URLType)
    audio: HttpUrl | None = Field(default=None, sa_type=URLType)

    # blog_posting_id: UUID | None = Field(default=None, foreign_key="creative_work.id")
    # blog_posting: t.Optional["CreativeWork"] | None = Relationship(
    #     back_populates="blog_post",
    #     sa_relationship_kwargs=dict(remote_side="CreativeWork.id"),
    #     # sa_relationship_kwargs=dict(
    #     #     primaryjoin="CreativeWork.id==CreativeWork.blog_posting_id"
    #     # ),
    # )
    # blog_post: list["CreativeWork"] | None = Relationship(
    #     back_populates="blog_posting",
    #     # sa_relationship_kwargs=dict(
    #     #     primaryjoin="CreativeWork.blog_posting_id==CreativeWork.id"
    #     # ),
    # )

    content_location_id: UUID | None = Field(default=None, foreign_key="place.id")
    content_location: Place | None = Relationship(
        back_populates="content_location",
        sa_relationship_kwargs=dict(
            primaryjoin="Place.id==CreativeWork.content_location_id"
        ),
    )
    created_location_id: UUID | None = Field(default=None, foreign_key="place.id")
    created_location: Place | None = Relationship(
        back_populates="created_location",
        sa_relationship_kwargs=dict(
            primaryjoin="Place.id==CreativeWork.created_location_id"
        ),
    )
    recorded_at_id: UUID | None = Field(default=None, foreign_key="event.id")
    recorded_at: Event | None = Relationship(
        back_populates="recorded_in",
        sa_relationship_kwargs=dict(
            primaryjoin="Event.id==CreativeWork.recorded_at_id"
        ),
    )

    # track: list["CreativeWork"] | None = Relationship(
    #     back_populates="in_playlist",
    #     sa_relationship_kwargs=dict(
    #         primaryjoin="CreativeWork.in_playlist_id==CreativeWork.id"
    #     ),
    # )
    # in_playlist_id: UUID | None = Field(default=None, foreign_key="creative_work.id")
    # in_playlist: t.Optional["CreativeWork"] | None = Relationship(
    #     back_populates="track",
    #     sa_relationship_kwargs=dict(
    #         primaryjoin="CreativeWork.id==CreativeWork.in_playlist_id"
    #     ),
    # )
    # release_of_id: UUID | None = Field(default=None, foreign_key="creative_work.id")
    # release_of: t.Optional["CreativeWork"] | None = Relationship(
    #     back_populates="album_release",
    #     sa_relationship_kwargs=dict(
    #         primaryjoin="CreativeWork.id==CreativeWork.release_of_id"
    #     ),
    # )
    # album_release: list["CreativeWork"] | None = Relationship(
    #     back_populates="release_of",
    #     sa_relationship_kwargs=dict(
    #         primaryjoin="CreativeWork.release_of_id==CreativeWork.id"
    #     ),
    # )

    # @hybrid_property
    # def duration(self) -> TimedeltaType:
    #     return self.end_time - self.start_time

    # @hybrid_property
    # def upload_date(self) -> ArrowType:
    #     return self.date_created

    # @hybrid_property
    # def headline(self) -> str:
    #     return self.name

    # @hybrid_property
    # def shared_content(self) -> str:
    #     return self.image.content_url

    # @hybrid_property
    # def article_section(self) -> str:
    #     return self.blog.name
