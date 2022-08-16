from datetime import datetime
from typing import Optional

from metabase_tools.models.generic import MetabaseGeneric


class User(MetabaseGeneric):
    name: Optional[str]  # TODO generate this
    email: str
    first_name: str
    last_login: datetime
    is_qbnewb: bool
    is_superuser: bool
    last_name: str
    date_joined: datetime
    common_name: str
