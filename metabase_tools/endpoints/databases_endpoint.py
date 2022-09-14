"""Classes related to database endpoints
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar, Optional

from metabase_tools.common import log_call
from metabase_tools.endpoints.generic_endpoint import Endpoint
from metabase_tools.models.database_model import DatabaseItem

logger = logging.getLogger(__name__)


class Databases(Endpoint[DatabaseItem]):
    """Database related endpoint methods"""

    _BASE_EP: ClassVar[str] = "/database"
    _STD_OBJ: ClassVar[type] = DatabaseItem

    @log_call
    def get(self, targets: Optional[list[int]] = None) -> list[DatabaseItem]:
        """Fetch list of databases

        Args:
            targets (list[int], optional): If provided, the list of databases to fetch

        Returns:
            list[DatabaseItem]
        """
        return super().get(targets=targets)

    @log_call
    def create(self, payloads: list[dict[str, Any]]) -> list[DatabaseItem]:
        """Create new database(s)

        Args:
            payloads (list[dict[str, Any]]): database details

        Returns:
            list[DatabaseItem]: Created databases
        """
        return super().create(payloads=payloads)

    @log_call
    def search(
        self,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[DatabaseItem]] = None,
    ) -> list[DatabaseItem]:
        """Method to search a list of databases meeting a list of parameters

        Args:
            search_params (list[dict]): Each dict contains search criteria and returns\
                 1 result
            search_list (list[DatabaseItem], optional): Provide to search an existing \
                list, by default pulls from API

        Returns:
            list[DatabaseItem]: List of databases of the relevant type
        """
        return super().search(search_params=search_params, search_list=search_list)
