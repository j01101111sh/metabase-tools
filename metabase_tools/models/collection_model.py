"""Classes related to collections endpoints
"""
from __future__ import annotations  # Included for support of |

from typing import TYPE_CHECKING, Any, ClassVar, Optional

from pydantic import PrivateAttr

from metabase_tools.exceptions import EmptyDataReceived
from metabase_tools.models.generic_model import Item

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi


class CollectionItem(Item):
    """Collection object class with related methods"""

    _BASE_EP: ClassVar[str] = "/collection"

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

    @classmethod
    def get_contents(
        cls,
        adapter: MetabaseApi,
        collection_id: int,
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

        response = adapter.get(
            endpoint=f"/collection/{collection_id}/items",
            params=params,
        )

        if isinstance(response, list) and all(
            isinstance(record, dict) for record in response
        ):
            return response
        raise EmptyDataReceived

    @classmethod
    def graph(cls, adapter: MetabaseApi) -> dict[str, Any]:
        """Graph of collection

        Returns:
            dict: graph of collection
        """
        result = adapter.get(endpoint="/collection/graph")
        if isinstance(result, dict):
            return result
        raise EmptyDataReceived
