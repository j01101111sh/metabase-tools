"""Classes related to alert endpoints
"""

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from metabase_tools.exceptions import MetabaseApiException
from metabase_tools.models.activity_model import ActivityItem

if TYPE_CHECKING:
    from metabase_tools import MetabaseApi

logger = getLogger(__name__)


class Activity:
    """Activity related endpoint methods"""

    _BASE_EP: ClassVar[str] = "/activity"
    _STD_OBJ: ClassVar[type] = ActivityItem

    def __init__(self, adapter: MetabaseApi):
        self._adapter = adapter

    def get(self: Activity) -> list[ActivityItem]:
        """Get recent activity on the server

        Raises:
            MetabaseApiException: Invalid results received from server

        Returns:
            list[ActivityItem]
        """
        result = self._adapter.get(endpoint=self._BASE_EP)
        if isinstance(result, list):
            activities = [self._STD_OBJ(**item) for item in result]
            for activity in activities:
                activity.set_adapter(self._adapter)
            return activities
        raise MetabaseApiException

    def search(
        self,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[ActivityItem]] = None,
    ) -> list[ActivityItem]:
        """Method to search a list of objects meeting a list of parameters

        Args:
            search_params (list[dict]): Each dict contains search criteria and returns\
                 1 result
            search_list (list[T], optional): Provide to search against an existing \
                list, by default pulls from API

        Returns:
            list[T]: List of objects of the relevant type
        """
        objs = search_list or self.get()
        results = []
        for param in search_params:
            for obj in objs:
                obj_dict = obj.dict()
                for key, value in param.items():
                    if key in obj_dict and value == obj_dict[key]:
                        results.append(obj)
        return results
