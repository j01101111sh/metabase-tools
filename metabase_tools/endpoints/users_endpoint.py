"""Classes related to card endpoints
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar, Optional

from metabase_tools.common import log_call
from metabase_tools.endpoints.generic_endpoint import Endpoint
from metabase_tools.exceptions import InvalidParameters
from metabase_tools.models.user_model import UserItem

logger = logging.getLogger(__name__)


class Users(Endpoint[UserItem]):
    """Card related endpoint methods"""

    _BASE_EP: ClassVar[str] = "/user"
    _STD_OBJ: ClassVar[type] = UserItem

    @log_call
    def get(self, targets: Optional[list[int]] = None) -> list[UserItem]:
        """Fetch list of users

        Args:
            targets (list[int], optional): If provided, the list of users to fetch

        Returns:
            list[UserItem]
        """
        return super().get(targets=targets)

    @log_call
    def create(self, payloads: list[dict[str, Any]]) -> list[UserItem]:
        """Create new card(s)

        Args:
            payloads (list[dict[str, Any]]): User details

        Returns:
            list[UserItem]: Created users
        """
        return super().create(payloads=payloads)

    @log_call
    def search(
        self,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[UserItem]] = None,
    ) -> list[UserItem]:
        """Method to search a list of users meeting a list of parameters

        Args:
            search_params (list[dict]): Each dict contains search criteria and returns\
                 1 result
            search_list (list[UserItem], optional): Provide to search an existing \
                list, by default pulls from API

        Returns:
            list[UserItem]: List of users of the relevant type
        """
        return super().search(search_params=search_params, search_list=search_list)

    @log_call
    def current(self) -> UserItem:
        """Current user details

        Raises:
            RequestFailure: Invalid response from API

        Returns:
            User: Current user details
        """
        response = self._adapter.get(endpoint="/user/current")
        if isinstance(response, dict):
            return UserItem(**response)
        raise InvalidParameters
