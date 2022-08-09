from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic.fields import Field
from typing_extensions import Self

from ..metabase import MetabaseApi
from .collection import Collection
from .generic import MetabaseGeneric
from .user import User


class Card(MetabaseGeneric):
    description: None
    archived: bool
    collection_position: None
    table_id: None
    result_metadata: list[dict]
    creator: User
    database_id: int
    enable_embedding: bool
    collection_id: Optional[int]
    query_type: str
    name: str
    creator_id: int
    updated_at: datetime
    made_public_by_id: None
    embedding_params: None
    cache_ttl: None
    dataset_query: dict
    id: int
    display: str
    last_edit_info: dict = Field(alias='last-edit-info')
    visualization_settings: dict
    collection: Optional[Collection]
    dataset: bool
    created_at: datetime
    public_uuid: Optional[UUID]

    @classmethod
    def get(cls, adapter: MetabaseApi, targets: Optional[int | list[int]] = None) -> Self | list[Self]:
        return super(Card, cls).get(adapter=adapter, endpoint='/card', targets=targets)

    @classmethod
    def post(cls, adapter: MetabaseApi, payloads: dict | list[dict]) -> Self | list[Self]:
        return super(Card, cls).post(adapter=adapter, endpoint='/card', payloads=payloads)
