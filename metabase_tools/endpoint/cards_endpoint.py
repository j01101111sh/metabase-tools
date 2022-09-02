from __future__ import annotations

import logging
from typing import Any, ClassVar, Optional

from metabase_tools.exceptions import EmptyDataReceived
from metabase_tools.models.card_model import CardItem

from .generic_endpoint import Endpoint

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
