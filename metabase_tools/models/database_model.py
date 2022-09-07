"""Classes related to database endpoints
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from pydantic import PrivateAttr

from metabase_tools.common import log_call
from metabase_tools.models.generic_model import Item

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = logging.getLogger(__name__)


class DatabaseItem(Item):
    """Database object class with related methods"""

    _BASE_EP: ClassVar[str] = "/database/{id}"

    _adapter: Optional[MetabaseApi] = PrivateAttr(None)

    description: Optional[str]
    features: list[str]
    cache_field_values_schedule: str
    timezone: Optional[str]
    auto_run_queries: bool
    metadata_sync_schedule: str
    caveats: Optional[str]
    is_full_sync: bool
    updated_at: datetime
    native_permissions: Optional[str]
    details: dict[str, Any]
    is_sample: bool
    is_on_demand: bool
    options: Optional[str]
    engine: str
    refingerprint: Optional[str]
    created_at: datetime
    points_of_interest: Optional[str]
    schedules: Optional[dict[str, Any]]

    @log_call
    def delete(self: DatabaseItem) -> dict[int | str, dict[str, Any]]:
        """Deletes the database

        Returns:
            dict[int | str, dict[str, Any]]
        """
        return super().delete()

    @log_call
    def update(self: DatabaseItem, payload: dict[str, Any]) -> DatabaseItem:
        """Method for updating a database

        Args:
            payloads (dict): Details of update

        Returns:
            DatabaseItem: Object of the relevant type
        """
        return super().update(payload=payload)
