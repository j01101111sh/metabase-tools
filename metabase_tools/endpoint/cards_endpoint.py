from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from metabase_tools.exceptions import EmptyDataReceived

# from metabase_tools.models.card_model import CardObject
from metabase_tools.models.card_model import CardItem

from .generic_endpoint import Endpoint

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = logging.getLogger(__name__)


class Cards(Endpoint[CardItem]):
    _BASE_EP: ClassVar[str] = "/card"
    _STD_OBJ: ClassVar[type] = CardItem

    def get(self, targets: Optional[list[int]] = None) -> list[CardItem]:
        """_summary_

        Args:
            targets (Optional[list[int]], optional): _description_. Defaults to None.

        Returns:
            list[CardItem]: _description_
        """
        return super().get(targets=targets)

    def create(self, payloads: list[dict[str, Any]]) -> list[CardItem]:
        return super().create(payloads=payloads)

    def search(
        self,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[CardItem]] = None,
    ) -> list[CardItem]:
        return super().search(search_params=search_params, search_list=search_list)

    def embeddable(self) -> list[CardItem]:
        """Fetch list of cards with embedding enabled

        Raises:
            EmptyDataReceived: If no cards have embedding enabled

        Returns:
            list[CardItem]: List of cards with embedding enabled
        """
        cards = self._adapter.get(endpoint="/card/embeddable")
        if cards:
            return [CardItem(**card) for card in cards if isinstance(card, dict)]
        raise EmptyDataReceived

    # @classmethod
    # def share(
    #     cls: type[GA], adapter: MetabaseApi, targets: list[int]
    # ) -> list[dict[str, Any]]:
    #     """Generate publicly-accessible links for cards

    #     Args:
    #         adapter (MetabaseApi): Connection to Metabase API
    #         targets (list[int]): Card IDs to share

    #     Returns:
    #         list[dict]: UUIDs to be used in public links.
    #     """
    #     return cls._request_list(
    #         http_method="POST",
    #         adapter=adapter,
    #         endpoint="/card/{id}/public_link",
    #         source=targets,
    #     )

    # @classmethod
    # def unshare(
    #     cls: type[GA], adapter: MetabaseApi, targets: list[int]
    # ) -> list[dict[str, Any]]:
    #     """Remove publicly-accessible links for cards

    #     Args:
    #         adapter (MetabaseApi): Connection to Metabase API
    #         targets (list[int]): Card IDs to unshare

    #     Returns:
    #         list[dict]: Result of unshare operation
    #     """
    #     return cls._request_list(
    #         http_method="DELETE",
    #         adapter=adapter,
    #         endpoint="/card/{id}/public_link",
    #         source=targets,
    #     )

    # @classmethod
    # def query(
    #     cls: type[GA], adapter: MetabaseApi, payloads: list[int]
    # ) -> list[CardQueryResult]:
    #     """Execute a query stored in card(s)

    #     Args:
    #         adapter (MetabaseApi): Connection to Metabase API
    #         targets (list[int]): list of cards to query

    #     Returns:
    #         list[CardQueryResult]: Results of queries
    #     """
    #     results = cls._request_list(
    #         http_method="POST",
    #         adapter=adapter,
    #         endpoint="/card/{id}/query",
    #         source=payloads,
    #     )
    #     return [CardQueryResult(**result) for result in results]
