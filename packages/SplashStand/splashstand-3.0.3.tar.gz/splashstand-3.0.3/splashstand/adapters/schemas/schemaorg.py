import typing as t

from acb.adapters import import_adapter
from acb.depends import depends
from acb.debug import debug
from inflection import underscore
from schemaorg_lite import main as schemaorg
from ._base import SchemasBase
from ._base import SchemasBaseSettings

Cache = import_adapter("cache")


def strip_url(url: str) -> str:
    return url.strip().removeprefix("https://schema.org/")


class SchemasSettings(SchemasBaseSettings): ...


class Schema:
    cache: Cache = depends()  # type: ignore
    _name: str
    _schema: t.Optional[schemaorg.Schema] = None
    _table_name: t.Optional[str] = None
    _help: t.Optional[str] = None
    _version: t.Optional[str] = None
    _properties: t.Optional[dict[str, t.Any]] = None

    def __init__(self, name: str, /, **data: t.Any) -> None:
        super().__init__(**data)
        self._name = name
        self._table_name = underscore(name)
        self._schema = schemaorg.Schema(name)
        self._help = getattr(self._schema, "comment", None)
        self._version = self._schema.version
        self._properties = {
            underscore(k): v for k, v in self._schema._properties.items()
        }

    @property
    async def _types(self) -> t.AsyncGenerator["Schema", None]:
        sub_types = getattr(self._schema, "subTypes", None)
        types = []
        if sub_types:
            types = [strip_url(t) for t in sub_types.split(",")]
        for _type in set(types):
            schema = await self.cache.get(f"schema_{underscore(_type)}")
            if not schema:
                schema = Schema(_type)
                await self.cache.set(f"schema_{underscore(_type)}", schema)
            setattr(self, schema._table_name, schema)  # type: ignore
            yield schema
            _sub_types = {x async for x in schema._types}
            for _sub_schema in _sub_types:
                setattr(self, _sub_schema._table_name, _sub_schema)  # type: ignore
                yield _sub_schema

    @property
    def _fields(self) -> dict[str, list[str]]:
        fields = {
            field: [strip_url(u) for u in props["rangeIncludes"].split(",")]
            for field, props in self._properties.items()
        }
        return fields


class Schemas(SchemasBase):  # type: ignore
    thing: t.Optional[Schema] = None

    @depends.inject
    async def init(self, cache: Cache = depends()) -> None:  # type: ignore
        self.thing = await cache.get("schema_thing")
        if not self.thing:
            self.thing = Schema("Thing")
            await cache.set("schema_thing", self.thing)
        async for _schema in self.thing._types:
            setattr(self, _schema._table_name, _schema)  # type: ignore
        debug(self.thing._fields)


depends.set(Schemas)
