from datetime import datetime
from typing import Any, Generic, List, Optional, Tuple, Type, TypeVar, Union
from uuid import UUID

import pymongo
from beanie import WriteRules
from beanie.odm.enums import SortDirection
from beanie.odm.queries.find import FindMany, FindOne, FindQueryProjectionType
from fastapi_exception import EntityNotFoundException

from ..dependencies.pagination import PaginationParams
from ..responses.pagination import PaginationResponse

T = TypeVar("T")


class BaseRepository(Generic[T]):
    _entity: T

    def __init__(self):
        self.projection_model: Optional[Type[FindQueryProjectionType]] = None
        self.skip_count: Optional[int] = None
        self.limit_count: Optional[int] = None
        self.sort: Optional[List[Tuple[str, SortDirection]]] = None
        self.is_ignore_cache: bool = False
        self.is_fetch_links: bool = False
        self.is_lazy_parse: bool = False
        self.limit_count: Optional[int] = None
        self.callback_options: List[Any] = []
        self.relations: List[Any] = []

    def reset(self):
        self.projection_model = None
        self.skip_count = None
        self.limit_count = None
        self.sort = None
        self.is_ignore_cache = False
        self.is_fetch_links = False
        self.is_lazy_parse = False
        self.callback_options = []
        self.relations = []

    def run_and_reset(self, result):
        self.reset()
        return result

    def skip(self, skip: int):
        self.skip_count = skip
        return self

    def limit(self, limit: int):
        self.limit_count = limit
        return self

    def fetch_links(self, is_fetch: Optional[bool] = True):
        self.is_fetch_links = is_fetch
        return self

    def fetch(self, *relations):
        self.relations = list(relations)
        return self

    def lazy_parse(self, is_lazy_parse: bool):
        self.is_lazy_parse = is_lazy_parse
        return self

    def ignore_cache(self, is_ignore_cache: bool):
        self.is_ignore_cache = is_ignore_cache
        return self

    def select(self, view_model):
        self.projection_model = view_model
        return self

    def order(self, fields: List[Tuple[str, SortDirection]]):
        if not self.sort:
            self.sort = []

        for field, direction in fields:
            self.sort.append((getattr(self._entity, field), direction))

        return self

    def order_desc(self, fields: Union[str, List[str]]):
        if not self.sort:
            self.sort = []

        if isinstance(fields, str):
            fields = [fields]

        return self.order([(field, pymongo.DESCENDING) for field in fields])

    def order_asc(self, fields: Union[str, List[str]]):
        if not self.sort:
            self.sort = []

        if isinstance(fields, str):
            fields = [fields]

        return self.order([(field, pymongo.ASCENDING) for field in fields])

    async def build_find_many_query(self, *criterion):
        return FindMany(self._entity).find_many(
            *criterion,
            projection_model=self.projection_model,
            skip=self.skip_count,
            limit=self.limit_count,
            sort=self.sort,
            fetch_links=self.is_fetch_links,
            lazy_parse=self.is_lazy_parse,
        )

    async def build_and_execute_find_one_query(self, *criterion):
        item = await FindOne(self._entity).find_one(
            *criterion,
            projection_model=self.projection_model,
            ignore_cache=self.is_ignore_cache,
            fetch_links=self.is_fetch_links,
        )

        for relation in self.relations:
            await item.fetch_link(getattr(self._entity, relation))

        return item

    async def find(self, *criterion):
        return self.run_and_reset(await self.apply_callback_and_get_many(await self.build_find_many_query(*criterion)))

    async def first_or_fail(self, *criterion):
        item = self.run_and_reset(await self.build_and_execute_find_one_query(*criterion))

        if not item:
            self.raise_not_found()

        return item

    async def find_by_id(self, entity_id: UUID):
        return await self.first_or_fail(self._entity.id == entity_id)

    async def find_one(self, *criterion):
        return self.run_and_reset(await self.build_and_execute_find_one_query(*criterion))

    async def create(self, data: dict) -> T:
        model = self._entity(**data)
        await model.save(link_rule=WriteRules.WRITE)

        return model

    async def create_if_not_exist(self, data: dict, *criterion):
        existed_model = await self.find_one(*criterion)
        if not existed_model:
            return await self.create(data)

        return existed_model

    async def inserts(self, items: list[dict]):
        models = list(map(lambda item: self._entity(**item), items))
        await self._entity.insert_many(models)

        return models

    async def first_or_create(self, data: dict):
        criterion = []
        for key, value in data.items():
            criterion.append(getattr(self._entity, key) == value)
        item = await self.find_one(*criterion)
        if item:
            return item
        return self.create(data)

    async def delete(self, *criterion):
        await self._entity.find(*criterion).delete()

    async def update_by_id(self, entity_id, data: dict):
        data = {**data, 'updated_at': datetime.now()}
        await self._entity.find_one(self._entity.id == entity_id).update({"$set": data})

    async def update(self, data: dict, *criterion):
        data = {**data, 'updated_at': datetime.now()}
        await self._entity.find(*criterion).update({"$set": data})

    async def count(self, *criterion):
        return await FindMany(self._entity).find(*criterion).count()

    async def upsert(self, data: dict, *criterion):
        existed_model = await self.find_one(*criterion)

        if not existed_model:
            return await self.create(data)
        await self.update(data, *criterion)

        return await self.find_one(*criterion)

    async def paginate(self, *criterion, pagination_params: PaginationParams) -> PaginationResponse[T]:
        page = pagination_params.page
        per_page = pagination_params.per_page

        skip_count = (page - 1) * per_page
        items = await self.skip(skip_count).limit(per_page).find(*criterion)
        total = await self.count(*criterion)

        return {'items': items, 'total': total, 'page': page, 'size': per_page}

    def raise_not_found(self):
        raise EntityNotFoundException(self._entity)

    async def exists(self, *criterion):
        return await self.count(*criterion) > 0

    async def filter(self, *criterion, limit: Optional[int] = None):
        if limit is not None:
            self.limit_count = limit
        return self.run_and_reset(await self.apply_callback_and_get_many(await self.build_find_many_query(*criterion)))

    def apply_callbacks(self, query):
        for callback in self.callback_options:
            query = callback(query)

        return query

    async def apply_callback_and_get_many(self, query):
        query = self.apply_callbacks(query)

        return await query.to_list()

    def scope_query(self, callbacks: list[Any]):
        self.callback_options = callbacks
        return self
