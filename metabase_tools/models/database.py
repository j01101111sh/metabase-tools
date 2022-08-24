from datetime import datetime
from typing import Optional

from typing_extensions import Self

from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.generic import MetabaseGeneric


class Database(MetabaseGeneric):
    description: Optional[str]
    features: list[str]
    cache_field_values_schedule: str
    timezone: str
    auto_run_queries: bool
    metadata_sync_schedule: str
    caveats: Optional[str]
    is_full_sync: bool
    updated_at: datetime
    native_permissions: Optional[str]
    details: dict
    is_sample: bool
    is_on_demand: bool
    options: Optional[str]
    engine: str
    refingerprint: Optional[str]
    created_at: datetime
    points_of_interest: Optional[str]

    @classmethod
    def get(
        cls, adapter: MetabaseApi, targets: Optional[list[int]] = None
    ) -> list[Self]:
        return super(Database, cls).get(
            adapter=adapter, endpoint="/database", targets=targets
        )

    @classmethod
    def post(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        return super(Database, cls).post(
            adapter=adapter, endpoint="/database", payloads=payloads
        )

    @classmethod
    def put(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        return super(Database, cls).put(
            adapter=adapter, endpoint="/database", payloads=payloads
        )

    @classmethod
    def search(
        cls,
        adapter: MetabaseApi,
        search_params: list[dict],
        search_list: Optional[list] = None,
    ) -> list[Self]:
        return super(Database, cls).search(
            adapter=adapter,
            # endpoint="/database",
            search_params=search_params,
            search_list=search_list,
        )
