"""Classes related to card endpoints
"""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, ClassVar, Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field

from metabase_tools.common import log_call
from metabase_tools.models.collection_model import Collection
from metabase_tools.models.generic_model import Item
from metabase_tools.models.user_model import User

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi


class CardItem(Item):
    """Card object class with related methods"""

    _BASE_EP: ClassVar[str] = "/card/{id}"

    description: Optional[str]
    archived: bool
    collection_position: Optional[int]
    table_id: Optional[int]
    result_metadata: Optional[list[dict[str, Any]]]
    creator: User
    database_id: Optional[int]
    enable_embedding: bool
    collection_id: Optional[int]
    query_type: Optional[str]
    creator_id: int
    updated_at: datetime
    made_public_by_id: Optional[int]
    embedding_params: Optional[dict[str, Any]]
    cache_ttl: Optional[str]
    dataset_query: dict[str, Any]
    display: str
    last_edit_info: Optional[dict[str, Any]] = Field(alias="last-edit-info")
    visualization_settings: dict[str, Any]
    collection: Optional[Collection]
    dataset: Optional[int]
    created_at: datetime
    public_uuid: Optional[UUID]
    can_write: Optional[bool]
    dashboard_count: Optional[int]
    is_favorite: Optional[bool] = Field(alias="favorite")

    @classmethod
    def update(
        cls: type[CardItem], adapter: MetabaseApi, payload: dict[str, Any]
    ) -> CardItem:
        return super().update(adapter=adapter, payload=payload)

    @classmethod
    def archive(
        cls: type[CardItem], adapter: MetabaseApi, target: int, unarchive: bool = False
    ) -> CardItem:
        return super().archive(adapter=adapter, target=target, unarchive=unarchive)

    @classmethod
    def related(
        cls: type[CardItem], adapter: MetabaseApi, targets: list[int]
    ) -> list[dict[str, Any]]:
        """Objects related to target

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (int): Card ID to pull

        Returns:
            dict: Dict with related objects for target
        """
        results = []
        for target in targets:
            new = {"card_id": target}
            result = adapter.get(endpoint=f"/card/{target}/related")
            if isinstance(result, dict):
                new |= result
            results.append(new)
        return results


class CardQueryResult(BaseModel):
    """Object for results of a card query"""

    data: dict[str, Any]
    database_id: int  #
    started_at: datetime
    json_query: dict[str, Any]
    average_execution_time: Optional[int]
    status: str
    context: str
    row_count: int
    running_time: int
