from typing import Optional

from typing_extensions import Self

from ..metabase import MetabaseApi
from .generic import MetabaseGeneric


class Collection(MetabaseGeneric):
    description: Optional[str]
    archived: Optional[bool]
    slug: Optional[str]
    color: Optional[str]
    name: str
    personal_owner_id: Optional[int]
    id: str | int
    location: Optional[str]
    namespace: Optional[int]
    effective_location: Optional[str]
    effective_ancestors: Optional[list[str]]
    can_write: Optional[bool]

    @classmethod
    def get(cls, adapter: MetabaseApi, targets: Optional[int | list[int]] = None) -> Self | list[Self]:
        return super(Collection, cls).get(adapter=adapter, endpoint='/collection', targets=targets)

    @classmethod
    def post(cls, adapter: MetabaseApi, payloads: dict | list[dict]) -> Self | list[Self]:
        return super(Collection, cls).post(adapter=adapter, endpoint='/collection', payloads=payloads)

    @classmethod
    def put(cls, adapter: MetabaseApi, payloads: dict | list[dict]) -> Self | list[Self]:
        return super(Collection, cls).put(adapter=adapter, endpoint='/collection', payloads=payloads)

    @classmethod
    def archive(cls, adapter: MetabaseApi, targets: int | list[int], unarchive=False) -> Self | list[Self]:
        return super(Collection, cls).archive(adapter=adapter, endpoint='/collection', targets=targets, unarchive=unarchive)
