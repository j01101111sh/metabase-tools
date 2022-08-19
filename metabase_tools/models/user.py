from datetime import datetime
from typing import Optional

from pydantic.fields import Field
from typing_extensions import Self

from metabase_tools.exceptions import RequestFailure
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.generic import MetabaseGeneric


class User(MetabaseGeneric):
    name: str = Field(alias="common_name")
    email: str
    first_name: str
    last_name: str
    date_joined: datetime
    last_login: Optional[datetime]
    updated_at: Optional[datetime]
    is_qbnewb: bool
    is_superuser: bool
    ldap_auth: Optional[bool]
    google_auth: Optional[bool]
    is_active: Optional[bool]
    locale: Optional[str]
    group_ids: Optional[list[int]]
    login_attributes: Optional[list]
    personal_collection_id: Optional[int]

    @classmethod
    def get(
        cls, adapter: MetabaseApi, targets: Optional[list[int]] = None
    ) -> list[Self]:
        return super(User, cls).get(adapter=adapter, endpoint="/user", targets=targets)

    @classmethod
    def post(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        return super(User, cls).post(
            adapter=adapter, endpoint="/user", payloads=payloads
        )

    @classmethod
    def put(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        return super(User, cls).put(
            adapter=adapter, endpoint="/user", payloads=payloads
        )

    @classmethod
    def search(
        cls,
        adapter: MetabaseApi,
        search_params: list[dict],
        search_list: Optional[list] = None,
    ) -> list[Self]:
        return super(User, cls).search(
            adapter=adapter,
            search_params=search_params,
            search_list=search_list,
        )

    @classmethod
    def current(cls, adapter: MetabaseApi) -> list[Self]:
        response = adapter.get(endpoint="/user/current")
        if response.data:
            return [cls(**record) for record in [response.data]]  # type: ignore
        raise RequestFailure

    @classmethod
    def disable(cls, adapter: MetabaseApi, targets: list[int]) -> list[Self]:
        return super(User, cls).delete(
            adapter=adapter, endpoint="/user", targets=targets
        )
