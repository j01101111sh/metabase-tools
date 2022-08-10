from datetime import datetime

from metabase_tools.models.generic import MetabaseGeneric


class User(MetabaseGeneric):
    email: str
    first_name: str
    last_login: datetime
    is_qbnewb: bool
    is_superuser: bool
    id: int
    last_name: str
    date_joined: datetime
    common_name: str
