"""Classes related to dashboard endpoints
"""

from __future__ import annotations

from logging import getLogger
from typing import Any, ClassVar, Optional

from metabase_tools.endpoints.generic_endpoint import Endpoint
from metabase_tools.models.dashboard_model import DashboardItem
from metabase_tools.models.generic_model import MissingParam
from metabase_tools.utils.logging_utils import log_call

logger = getLogger(__name__)


class Dashboards(Endpoint[DashboardItem]):
    """Dashboard related endpoint methods"""

    _BASE_EP: ClassVar[str] = "/dashboard"
    _STD_OBJ: ClassVar[type] = DashboardItem
    _required_params: ClassVar[list[str]] = ["name", "engine", "details"]

    @log_call
    def get(self, targets: Optional[list[int]] = None) -> list[DashboardItem]:
        """Fetch list of dashboards

        Args:
            targets (list[int], optional): If provided, the list of dashboards to fetch

        Returns:
            list[DashboardItem]
        """
        return super().get(targets=targets)

    def _make_create(self, **kwargs: Any) -> DashboardItem:
        """Makes create request

        Args:
            self (DashboardItem)

        Returns:
            DashboardItem: self
        """
        return super()._make_create(**kwargs)

    @log_call
    def create(
        self,
        name: str | MissingParam = MissingParam(),
        engine: str | MissingParam = MissingParam(),
        details: dict[str, Any] | MissingParam = MissingParam(),
        is_full_sync: Optional[bool | MissingParam] = MissingParam(),
        is_on_demand: Optional[bool | MissingParam] = MissingParam(),
        schedules: Optional[dict[str, Any] | MissingParam] = MissingParam(),
        auto_run_queries: Optional[bool | MissingParam] = MissingParam(),
        **kwargs: Any,
    ) -> DashboardItem:
        return super()._make_create(
            name=name,
            engine=engine,
            details=details,
            is_full_sync=is_full_sync,
            is_on_demand=is_on_demand,
            schedules=schedules,
            auto_run_queries=auto_run_queries,
            **kwargs,
        )

    @log_call
    def search(
        self,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[DashboardItem]] = None,
    ) -> list[DashboardItem]:
        """Method to search a list of dashboards meeting a list of parameters

        Args:
            search_params (list[dict]): Each dict contains search criteria and returns\
                 1 result
            search_list (list[DashboardItem], optional): Provide to search an existing \
                list, by default pulls from API

        Returns:
            list[DashboardItem]: List of dashboards of the relevant type
        """
        return super().search(search_params=search_params, search_list=search_list)
