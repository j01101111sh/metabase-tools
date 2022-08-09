from typing import Optional

from pydantic import BaseModel
from typing_extensions import Self

from ..exceptions import EmptyDataReceived, InvalidParameters
from ..metabase import MetabaseApi


class MetabaseGeneric(BaseModel):
    @classmethod
    def get(cls, adapter: MetabaseApi, endpoint: str, targets: Optional[int | list[int]]) -> Self | list[Self]:
        """Generic method for returning an object or list of objects

        Parameters
        ----------
        adapter : MetabaseApi
            Connection to Metabase API
        endpoint : str
            Endpoint to use for the request
        targets : Optional[int  |  list[int]]
            If None, return list of the selected objects. Otherwise, return the object(s) of the selected type with the ID(s) provided.

        Returns
        -------
        Self | list[Self]

        Raises
        ------
        InvalidParameters
            Targets are not None, int, or list[int]
        EmptyDataReceived
            No data is received from the API
        """
        if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
            # If a list of targets is provided, return a list of objects
            pass
        elif isinstance(targets, int):
            # If a single target is provided, return that object
            pass
        elif targets is None:
            # If no targets are provided, all objects of that type should be returned
            response = adapter.get(endpoint=endpoint)
            if response.data:  # Validate data was returned
                # Unpack data into instances of the class and return
                return [cls(**record) for record in response.data]
        else:
            # If something other than None, int or list[int], raise error
            raise InvalidParameters('Invalid target(s)')
        # If response.data was empty, raise error
        raise EmptyDataReceived('No data returned')

    @classmethod
    def post(cls, adapter: MetabaseApi, endpoint: str, payloads: dict | list[dict]) -> Self | list[Self]:
        # TODO validate params by creating a method in the child class
        # TODO docstring
        if isinstance(payloads, list) and all(isinstance(t, dict) for t in payloads):
            # If a list of targets is provided, return a list of objects
            pass
        elif isinstance(payloads, dict):
            # If a single target is provided, return that object
            response = adapter.post(endpoint=endpoint, json=payloads)
            if response.data and isinstance(response.data, dict):
                return cls(**response.data)
        else:
            # If something other than dict or list[dict], raise error
            raise InvalidParameters('Invalid target(s)')
        # If response.data was empty or not a valid type, raise error
        raise EmptyDataReceived('No data returned')
