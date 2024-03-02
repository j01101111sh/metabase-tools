"""Classes related to card endpoints
"""

from __future__ import annotations

from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING, Any, ClassVar
from uuid import UUID

from packaging.version import Version
from pydantic import BaseModel, PrivateAttr
from pydantic.fields import Field

from metabase_tools.models.collection_model import CollectionItem
from metabase_tools.models.generic_model import Item, MissingParam
from metabase_tools.models.user_model import UserItem
from metabase_tools.utils.logging_utils import log_call

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = getLogger(__name__)


class CardItem(Item):
    """Card object class with related methods"""

    _BASE_EP: ClassVar[str] = "/card/{id}"

    _adapter: MetabaseApi | None = PrivateAttr(None)
    _server_version: Version | None = PrivateAttr(None)

    description: str | None
    archived: bool
    collection_position: int | None
    table_id: int | None
    result_metadata: list[dict[str, Any]] | None
    creator: UserItem
    database_id: int | None
    enable_embedding: bool
    collection_id: int | None
    query_type: str | None
    creator_id: int
    updated_at: datetime
    made_public_by_id: int | None
    embedding_params: dict[str, Any] | None
    cache_ttl: str | None
    dataset_query: dict[str, Any]
    display: str
    last_edit_info: dict[str, Any] | None = Field(alias="last-edit-info")
    visualization_settings: dict[str, Any]
    collection: CollectionItem | None
    dataset: int | None
    created_at: datetime
    public_uuid: UUID | None
    can_write: bool | None
    is_write: bool | None
    dashboard_count: int | None
    is_favorite: bool | None = Field(alias="favorite")

    average_query_time: int | None
    collection_preview: bool | None
    entity_id: str | None
    last_query_start: datetime | None
    moderation_reviews: list[Any] | None
    parameter_mappings: list[Any] | None
    parameters: list[Any] | None

    @log_call
    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        super().set_adapter(adapter=adapter)

    @log_call
    def refresh(self: CardItem) -> CardItem:
        """Returns refreshed copy of the card

        Returns:
            CardItem: self
        """
        return super().refresh()

    @log_call
    def delete(self: CardItem) -> None:
        """DEPRECATED; use archive instead"""
        raise NotImplementedError

    def _make_update(self: CardItem, **kwargs: Any) -> CardItem:
        """Makes update request

        Args:
            self (CardItem)

        Returns:
            CardItem: self
        """
        return super()._make_update(**kwargs)

    @log_call
    def update(
        self: CardItem,
        visualization_settings: None | (dict[str, str] | MissingParam) = MissingParam(),
        description: str | MissingParam | None = MissingParam(),
        archived: bool | MissingParam | None = MissingParam(),
        collection_position: int | MissingParam | None = MissingParam(),
        result_metadata: list[dict[str, str]] | MissingParam | None = MissingParam(),
        metadata_checksum: str | MissingParam | None = MissingParam(),
        enable_embedding: bool | MissingParam | None = MissingParam(),
        collection_id: int | MissingParam | None = MissingParam(),
        name: str | MissingParam | None = MissingParam(),
        embedding_params: dict[str, str] | MissingParam | None = MissingParam(),
        dataset_query: dict[str, Any] | MissingParam | None = MissingParam(),
        display: str | MissingParam | None = MissingParam(),
        **kwargs: Any,
    ) -> CardItem:
        """Updates a card using the provided parameters

        Args:
            self (CardItem)
            visualization_settings (dict[str, str], optional)
            description (str, optional)
            archived (bool, optional)
            collection_position (int, optional)
            result_metadata (list[dict[str, str]], optional)
            metadata_checksum (str, optional)
            enable_embedding (bool, optional)
            collection_id (int, optional)
            name (str, optional)
            embedding_params (dict[str, str], optional)
            dataset_query (dict[str, Any], optional)
            display (str, optional)

        Returns:
            CardItem: _description_
        """
        return self._make_update(
            visualization_settings=visualization_settings,
            description=description,
            archived=archived,
            collection_position=collection_position,
            result_metadata=result_metadata,
            metadata_checksum=metadata_checksum,
            enable_embedding=enable_embedding,
            collection_id=collection_id,
            name=name,
            embedding_params=embedding_params,
            dataset_query=dataset_query,
            display=display,
            **kwargs,
        )

    @log_call
    def archive(self: CardItem) -> CardItem:
        """Method for archiving a card

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            CardItem: Object of the relevant type
        """
        return super().archive()

    @log_call
    def unarchive(self: CardItem) -> CardItem:
        """Method for unarchiving a card

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            CardItem: Object of the relevant type
        """
        return super().unarchive()

    @log_call
    def related(self: CardItem) -> CardRelatedObjects:
        """Objects related to target

        Returns:
            CardRelatedObjects
        """
        if self._adapter:
            result = self._adapter.get(endpoint=f"/card/{self.id}/related")
            if isinstance(result, dict):
                result["card_id"] = self.id
                return CardRelatedObjects(**result)
            raise TypeError(f"Expected dict, received {type(result)}")
        raise AttributeError("Adapter not set on object")

    @log_call
    def favorite(self: CardItem) -> CardItem:
        """Mark card as favorite

        Returns:
            dict: Result of favoriting operation
        """
        if self._server_version and self._server_version >= Version("v0.40"):
            raise NotImplementedError("This function was deprecated in Metabase v0.40")
        if self._adapter:
            result = self._adapter.post(endpoint=f"/card/{self.id}/favorite")
            if isinstance(result, dict):
                return self.refresh()
            raise TypeError(f"Expected dict, received {type(result)}")
        raise AttributeError("Adapter not set on object")

    @log_call
    def unfavorite(self: CardItem) -> CardItem:
        """Unfavorite card

        Returns:
            dict: Result of unfavoriting operation
        """
        if self._server_version and self._server_version >= Version("v0.40"):
            raise NotImplementedError("This function was deprecated in Metabase v0.40")
        if self._adapter:
            result = self._adapter.delete(endpoint=f"/card/{self.id}/favorite")
            if isinstance(result, dict):
                return self.refresh()
            raise TypeError(f"Expected dict, received {type(result)}")
        raise AttributeError("Adapter not set on object")

    @log_call
    def share(self: CardItem) -> CardItem:
        """Generate publicly-accessible link for card

        Returns:
            dict: UUID to be used in public link.
        """
        if self._adapter:
            result = self._adapter.post(endpoint=f"/card/{self.id}/public_link")
            if isinstance(result, dict) and "uuid" in result:
                return self.refresh()
            raise TypeError(f"Expected dict, received {type(result)}")
        raise AttributeError("Adapter not set on object")

    @log_call
    def unshare(self: CardItem) -> CardItem:
        """Remove publicly-accessible links for card

        Returns:
            dict: UUID to be used in public link.
        """
        if self._adapter:
            result = self._adapter.delete(endpoint=f"/card/{self.id}/public_link")
            if isinstance(result, dict) and isinstance(self.id, int):
                card = self._adapter.cards.get([self.id])[0]
                return card
            raise TypeError(f"Expected dict, received {type(result)}")
        raise AttributeError("Adapter not set on object")

    @log_call
    def query(self: CardItem) -> CardQueryResult:
        """Execute a query stored in card(s)

        Returns:
            CardQueryResult: Results of query
        """
        if self._adapter:
            result = self._adapter.post(endpoint=f"/card/{self.id}/query")
            if isinstance(result, dict):
                return CardQueryResult(**result)
            raise TypeError(f"Expected dict, received {type(result)}")
        raise AttributeError("Adapter not set on object")


class CardQueryResult(BaseModel):
    """Object for results of a card query"""

    data: dict[str, Any]
    database_id: int
    started_at: datetime
    json_query: dict[str, Any]
    average_execution_time: int | None
    status: str
    context: str
    row_count: int
    running_time: int


class CardRelatedObjects(BaseModel):
    """Objects related to the specified card"""

    card_id: int
    table: str | None
    metrics: list[dict[str, int]]
    segments: list[dict[str, int]]
    dashboard_mates: list[dict[str, int]] = Field(alias="dashboard-mates")
    similar_questions: list[dict[str, int]] = Field(alias="similar-questions")
    canonical_metric: str | None = Field(alias="canonical-metric")
    dashboards: list[dict[str, Any]]
    collections: list[dict[str, Any]]
