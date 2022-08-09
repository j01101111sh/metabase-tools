from typing import Optional

from .generic import MetabaseGeneric


class Collection(MetabaseGeneric):
    description: Optional[str]
    archived: bool
    slug: str
    color: str
    name: str
    personal_owner_id: Optional[int]
    id: int
    location: str
    namespace: Optional[int]
