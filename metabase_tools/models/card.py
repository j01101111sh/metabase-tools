"""Classes related to card endpoints
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic.fields import Field
from typing_extensions import Self

from metabase_tools.exceptions import (
    EmptyDataReceived,
    InvalidDataReceived,
    RequestFailure,
)
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.collection import Collection
from metabase_tools.models.generic import MetabaseGeneric
from metabase_tools.models.user import User


class Card(MetabaseGeneric):
    """Card object class with related methods"""

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
        """Fetch a list of cards using the provided MetabaseAPI

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int], optional): Card IDs to fetch or returns all cards

        Returns:
            list[Card]: List of cards requested
        """
        return super(Card, cls).get(adapter=adapter, endpoint="/card", targets=targets)

    @classmethod
    def post(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        """Create new cards

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            payloads (list[dict]): Details of cards to create

        Returns:
            list[Card]: List of cards created
        """
        return super(Card, cls).post(
            adapter=adapter, endpoint="/card", payloads=payloads
        )

    @classmethod
    def put(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        """Update existing cards

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            payloads (list[dict]): Details of cards to update

        Returns:
            list[Card]: List of updated cards
        """
        return super(Card, cls).put(
            adapter=adapter, endpoint="/card/{id}", payloads=payloads
        )

    @classmethod
    def archive(
        cls, adapter: MetabaseApi, targets: list[int], unarchive=False
    ) -> list[Self]:
        """Archive cards

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): Card IDs to archive
            unarchive (bool, optional): Unarchive targets. Defaults to False.

        Returns:
            list[Card]: List of archived cards
        """
        return super(Card, cls).archive(
            adapter=adapter, endpoint="/card/{id}", targets=targets, unarchive=unarchive
        )

    @classmethod
    def search(
        cls,
        adapter: MetabaseApi,
        search_params: list[dict],
        search_list: Optional[list] = None,
    ) -> list[Self]:
        """Search for cards based on provided criteria

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            search_params (list[dict]): Search criteria; 1 result per
            search_list (list, optional): Search existing list or pulls from API

        Returns:
            list[Card]: List of cards from results
        """
        return super(Card, cls).search(
            adapter=adapter,
            search_params=search_params,
            search_list=search_list,
        )

    @classmethod
    def related(cls, adapter: MetabaseApi, targets: list[int]) -> list[dict]:
        """Objects related to targets

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): Card IDs to pull

        Returns:
            list[dict]: List of dicts with related objects for each target
        """
        results = []
        for target in targets:
            new = {"card_id": target}
            result = adapter.get(endpoint=f"/card/{target}/related").data
            if isinstance(result, dict):
                new |= result
            results.append(new)
        return results

    @classmethod
    def embeddable(cls, adapter: MetabaseApi) -> list[Self]:
        """Fetch list of cards with embedding enabled

        Args:
            adapter (MetabaseApi): Connection to Metabase API

        Raises:
            EmptyDataReceived: If no cards have embedding enabled

        Returns:
            list[Self]: List of cards with embedding enabled
        """
        cards = adapter.get(endpoint="/card/embeddable").data
        if cards:
            return [cls(**card) for card in cards]
        raise EmptyDataReceived

    @classmethod
    def favorite(cls, adapter: MetabaseApi, targets: list[int]) -> list[dict]:
        """Favorite cards

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): Card IDs to favorite

        Returns:
            list[dict]: Results of favoriting operation
        """
        results = []
        for target in targets:
            try:
                result = adapter.post(endpoint=f"/card/{target}/favorite").data
            except RequestFailure:
                result = {
                    "card_id": target,
                    "error": "Metabase error, probably already a favorite",
                }
            if isinstance(result, dict):
                results.append(result)
        return results

    @classmethod
    def unfavorite(cls, adapter: MetabaseApi, targets: list[int]) -> list[dict]:
        """Unfavorite cards

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): Card IDs to unfavorite

        Returns:
            list[dict]: Results of unfavoriting operation
        """
        results = []
        for target in targets:
            try:
                success = (
                    adapter.delete(endpoint=f"/card/{target}/favorite").status_code
                    == 204
                )
                result = {"card_id": target, "success": success}
            except InvalidDataReceived:
                result = {
                    "card_id": target,
                    "error": "Metabase error, probably not a favorite",
                }
            results.append(result)
        return results

    @classmethod
    def share(cls, adapter: MetabaseApi, targets: list[int]) -> list[dict]:
        """Generate publicly-accessible links for cards

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): Card IDs to share

        Returns:
            list[dict]: UUIDs to be used in public links.
        """
        results = []
        for target in targets:
            result = adapter.post(endpoint=f"/card/{target}/public_link").data
            results.append(result)
        return results

    @classmethod
    def unshare(cls, adapter: MetabaseApi, targets: list[int]) -> list[dict]:
        """Remove publicly-accessible links for cards

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): Card IDs to unshare

        Returns:
            list[dict]: Result of unshare operation
        """
        results = []
        for target in targets:
            result = adapter.delete(endpoint=f"/card/{target}/public_link").data
            results.append(result)
        return results
