from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic.fields import Field
from typing_extensions import Self

from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.collection import Collection
from metabase_tools.models.generic import MetabaseGeneric
from metabase_tools.models.user import User


class Card(MetabaseGeneric):
    description: Optional[str]
    archived: bool
    collection_position: Optional[int]
    table_id: Optional[int]
    result_metadata: Optional[list[dict]]
    creator: User
    database_id: Optional[int]
    enable_embedding: bool
    collection_id: Optional[int]
    query_type: Optional[str]
    creator_id: int
    updated_at: datetime
    made_public_by_id: Optional[int]
    embedding_params: Optional[dict]
    cache_ttl: Optional[str]
    dataset_query: dict
    display: str
    last_edit_info: Optional[dict] = Field(alias="last-edit-info")
    visualization_settings: dict
    collection: Optional[Collection]
    dataset: Optional[int]
    created_at: datetime
    public_uuid: Optional[UUID]

    @classmethod
    def get(
        cls, adapter: MetabaseApi, targets: Optional[list[int]] = None
    ) -> list[Self]:
        return super(Card, cls).get(adapter=adapter, endpoint="/card", targets=targets)

    @classmethod
    def post(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        return super(Card, cls).post(
            adapter=adapter, endpoint="/card", payloads=payloads
        )

    @classmethod
    def put(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        return super(Card, cls).put(
            adapter=adapter, endpoint="/card", payloads=payloads
        )

    @classmethod
    def archive(
        cls, adapter: MetabaseApi, targets: list[int], unarchive=False
    ) -> list[Self]:
        return super(Card, cls).archive(
            adapter=adapter, endpoint="/card", targets=targets, unarchive=unarchive
        )

    @classmethod
    def search(
        cls,
        adapter: MetabaseApi,
        search_params: list[dict],
        search_list: Optional[list] = None,
    ) -> list[Self]:
        return super(Card, cls).search(
            adapter=adapter,
            search_params=search_params,
            search_list=search_list,
        )
