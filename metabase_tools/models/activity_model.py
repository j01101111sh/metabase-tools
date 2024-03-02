"""Classes related to activity endpoints
"""

from __future__ import annotations

from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING, Any

from metabase_tools.models.database_model import DatabaseItem
from metabase_tools.models.generic_model import Item
from metabase_tools.models.user_model import UserItem
from metabase_tools.utils.logging_utils import log_call

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = getLogger(__name__)


class ActivityItem(Item):
    """Activity object class with related methods"""

    id: int
    table_id: int | None
    table: str | None
    database_id: int | None
    model_exists: bool | None
    topic: str | None
    custom_id: int | None
    details: dict[str, Any] | None
    model_id: int | None
    database: DatabaseItem | None
    user_id: int | None
    timestamp: datetime
    user: UserItem | None
    model: str | None

    @log_call
    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        super().set_adapter(adapter=adapter)
