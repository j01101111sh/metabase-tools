"""Classes related to card endpoints
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar, Optional

from metabase_tools.common import log_call, untested
from metabase_tools.endpoints.generic_endpoint import Endpoint
from metabase_tools.exceptions import EmptyDataReceived
from metabase_tools.models.card_model import CardItem

logger = logging.getLogger(__name__)


class Cards(Endpoint[CardItem]):
    """Card related endpoint methods"""

    _BASE_EP: ClassVar[str] = "/card"
    _STD_OBJ: ClassVar[type] = CardItem

    @log_call
    def get(self, targets: Optional[list[int]] = None) -> list[CardItem]:
        """Fetch list of cards

        Args:
            targets (list[int], optional): If provided, the list of cards to fetch

        Returns:
            list[CardItem]
        """
        return super().get(targets=targets)

    @log_call
    def create(self, payloads: list[dict[str, Any]]) -> list[CardItem]:
        """Create new card(s)

        Args:
            payloads (list[dict[str, Any]]): Card details

        Returns:
            list[CardItem]: Created cards
        """
        return super().create(payloads=payloads)

    @log_call
    def search(
        self,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[CardItem]] = None,
    ) -> list[CardItem]:
        """Method to search a list of cards meeting a list of parameters

        Args:
            search_params (list[dict]): Each dict contains search criteria and returns\
                 1 result
            search_list (list[CardItem], optional): Provide to search an existing \
                list, by default pulls from API

        Returns:
            list[CardItem]: List of cards of the relevant type
        """
        return super().search(search_params=search_params, search_list=search_list)

    @untested
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
