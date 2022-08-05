from .metabase_objects import MetabaseObject


class Collection(MetabaseObject):
    authority_level: None
    description: None
    archived: bool
    slug: str
    color: str
    name: str
    personal_owner_id: None
    id: int
    location: str
    namespace: None
