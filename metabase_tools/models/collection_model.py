"""Classes related to collections endpoints
"""
from __future__ import annotations  # Included for support of |

import logging
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from pydantic import PrivateAttr

from metabase_tools.common import log_call
from metabase_tools.exceptions import EmptyDataReceived
from metabase_tools.models.generic_model import Item

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = logging.getLogger(__name__)


class CollectionItem(Item):
    """Collection object class with related methods"""

    _BASE_EP: ClassVar[str] = "/collection/{id}"

    _adapter: Optional[MetabaseApi] = PrivateAttr(None)

    description: Optional[str]
    archived: Optional[bool]
    slug: Optional[str]
    color: Optional[str]
    personal_owner_id: Optional[int]
    location: Optional[str]
    namespace: Optional[int]
    effective_location: Optional[str]
    effective_ancestors: Optional[list[dict[str, Any]]]
    can_write: Optional[bool]
    parent_id: Optional[int]

    authority_level: Optional[Any]
    entity_id: Optional[str]

    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        super().set_adapter(adapter=adapter)

    @log_call
    def update(self: CollectionItem, payload: dict[str, Any]) -> CollectionItem:
        """Method for updating a collection

        Args:
            payload (dict): Details of update

        Returns:
            CollectionItem: Object of the relevant type
        """
        return super().update(payload=payload)

    @log_call
    def archive(self: CollectionItem) -> CollectionItem:
        """Method for archiving a collection

        Returns:
            CollectionItem: Object of the relevant type
        """
        return super().archive()

    def unarchive(self: CollectionItem) -> CollectionItem:
        """Method for unarchiving a collection

        Returns:
            CollectionItem: Object of the relevant type
        """
        return super().unarchive()

    @log_call
    def delete(self: CollectionItem) -> dict[int | str, dict[str, Any]]:
        """DEPRECATED; use archive instead

        Returns:
            dict[int | str, dict[str, Any]]
        """
        raise NotImplementedError

    @log_call
    def get_contents(
        self,
        model_type: Optional[str] = None,
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
            response = self._adapter.get(
                endpoint=f"/collection/{self.id}/items",
                params=params,
            )
            if isinstance(response, list) and all(
                isinstance(record, dict) for record in response
            ):
                return response
        raise EmptyDataReceived
