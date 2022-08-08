from typing import Optional

from pydantic import BaseModel
from typing_extensions import Self

from ..exceptions import EmptyDataReceived, InvalidParameters
from ..metabase import MetabaseApi


class MetabaseGeneric(BaseModel):
    @classmethod
    def get(cls, adapter: MetabaseApi, endpoint: str, targets: Optional[int | list[int]]) -> Self | list[Self]:
        if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
            pass
        elif isinstance(targets, int):
            pass
        elif targets is None:
            # If no targets are provided, all objects of that type should be returned
            response = adapter.get(endpoint=endpoint)
            if response.data:  # Validate data was returned
                # Unpack data into instances of the class and return
                return [cls(**record) for record in response.data]
        else:
            raise InvalidParameters('Invalid target(s)')
        raise EmptyDataReceived('No data returned')
