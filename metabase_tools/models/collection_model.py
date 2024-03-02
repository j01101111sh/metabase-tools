"""Classes related to collections endpoints
"""

from __future__ import annotations  # Included for support of |

from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import PrivateAttr

from metabase_tools.exceptions import MetabaseApiException
from metabase_tools.models.generic_model import Item, MissingParam
from metabase_tools.utils.logging_utils import log_call

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = getLogger(__name__)


class CollectionItem(Item):
    """Collection object class with related methods"""

    _BASE_EP: ClassVar[str] = "/collection/{id}"

    _adapter: MetabaseApi | None = PrivateAttr(None)

    description: str | None
    archived: bool | None
    slug: str | None
    color: str | None
    personal_owner_id: int | None
    location: str | None
    namespace: int | None
    effective_location: str | None
    effective_ancestors: list[dict[str, Any]] | None
    can_write: bool | None
    parent_id: int | None

    authority_level: Any | None
    entity_id: str | None
    created_at: datetime | None

    @log_call
    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        super().set_adapter(adapter=adapter)

    @log_call
    def refresh(self: CollectionItem) -> CollectionItem:
        """Returns refreshed copy of the collection

        Returns:
            CollectionItem: self
        """
        return super().refresh()

    def _make_update(self: CollectionItem, **kwargs: Any) -> CollectionItem:
        """Makes update request

        Args:
            self (CollectionItem)

        Returns:
            CollectionItem: self
        """
        return super()._make_update(**kwargs)

    @log_call
    def update(
        self: CollectionItem,
        name: str | MissingParam | None = MissingParam(),
        color: str | MissingParam | None = MissingParam(),
        description: str | MissingParam | None = MissingParam(),
        archived: bool | MissingParam | None = MissingParam(),
        parent_id: int | MissingParam | None = MissingParam(),
        **kwargs: Any,
    ) -> CollectionItem:
        """Updates a collection using the provided parameters

        Args:
            self (CollectionItem)
            name (str, optional)
            color (str, optional)
            description (str, optional)
            archived (bool, optional)
            parent_id (int, optional)

        Returns:
            CollectionItem
        """
        return self._make_update(
            name=name,
            color=color,
            description=description,
            archived=archived,
            parent_id=parent_id,
            **kwargs,
        )

    @log_call
    def archive(self: CollectionItem) -> CollectionItem:
        """Method for archiving a collection

        Returns:
            CollectionItem: Object of the relevant type
        """
        return super().archive()

    @log_call
    def unarchive(self: CollectionItem) -> CollectionItem:
        """Method for unarchiving a collection

        Returns:
            CollectionItem: Object of the relevant type
        """
        return super().unarchive()

    @log_call
    def delete(self: CollectionItem) -> None:
        """DEPRECATED; use archive instead"""
        raise NotImplementedError

    @log_call
    def get_contents(
        self,
        model_type: str | None = None,
        archived: bool = False,
    ) -> list[dict[str, Any]]:
        """Get the contents of the provided collection

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            collection_id (int): ID of the requested collection
            model_type (str, optional): Filter to provided model. Defaults to all.
            archived (bool, optional): Archived objects. Defaults to False.

        Raises:
            EmptyDataReceived: No results from API

        Returns:
            list: Contents of collection
        """
        params: dict[Any, Any] = {}
        if archived:
            params["archived"] = archived
        if model_type:
            params["model"] = model_type

        if self._adapter:
            result = self._adapter.get(
                endpoint=f"/collection/{self.id}/items",
                params=params,
            )
            if isinstance(result, list) and all(
                isinstance(record, dict) for record in result
            ):
                return result
            raise TypeError(f"Expected list[dict], received {type(result)}")
        raise AttributeError("Adapter not set on object")

    @log_call
    def check_for_object(self, item_name: str) -> int:
        """Checks for object in the collection and returns the id, if found

        Args:
            item_name (str): Name of the item being located

        Raises:
            MetabaseApiException: Item not found

        Returns:
            int: id of the item being located
        """
        collection_items = self.get_contents(model_type="card", archived=False)
        for item in collection_items:
            if item["name"] == item_name and isinstance(item["id"], int):
                return item["id"]
        raise MetabaseApiException
