from typing import Optional

from pydantic import BaseModel
from typing_extensions import Self

from metabase_tools.exceptions import EmptyDataReceived, InvalidParameters
from metabase_tools.metabase import MetabaseApi


class MetabaseGeneric(BaseModel):
    @classmethod
    def _request_list(
        cls,
        http_method: str,
        adapter: MetabaseApi,
        endpoint: str,
        targets: Optional[list[int]] = None,
        jsons: Optional[list[dict]] = None,
    ) -> list[Self]:
        results = []
        source = targets or jsons
        if not source:
            raise InvalidParameters

        for item in source:
            if isinstance(item, int):
                response = adapter.do(
                    http_method=http_method, endpoint=f"{endpoint}/{item}"
                )
            elif isinstance(item, dict):
                if http_method == "PUT":
                    response = adapter.do(
                        http_method=http_method,
                        endpoint=f"{endpoint}/{item['id']}",
                        json=item,
                    )
                else:
                    response = adapter.do(
                        http_method=http_method, endpoint=f"{endpoint}", json=item
                    )
            else:
                raise InvalidParameters
            if response.data and isinstance(response.data, dict):
                results.append(cls(**response.data))
        if len(results) > 0:
            return results
        raise EmptyDataReceived("No data returned")

    @classmethod
    def get(
        cls, adapter: MetabaseApi, endpoint: str, targets: Optional[list[int]]
    ) -> list[Self]:
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
         list[Self]

        Raises
        ------
        InvalidParameters
            Targets are not None, int, or list[int]
        EmptyDataReceived
            No data is received from the API
        """
        if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
            return cls._request_list(
                http_method="GET",
                adapter=adapter,
                endpoint=endpoint,
                targets=targets,
            )
        elif targets is None:
            # If no targets are provided, all objects of that type should be returned
            response = adapter.get(endpoint=endpoint)
            if response.data:  # Validate data was returned
                # Unpack data into instances of the class and return
                return [cls(**record) for record in response.data]
        else:
            # If something other than None, int or list[int], raise error
            raise InvalidParameters("Invalid target(s)")
        # If response.data was empty, raise error
        raise EmptyDataReceived("No data returned")

    @classmethod
    def post(
        cls, adapter: MetabaseApi, endpoint: str, payloads: list[dict]
    ) -> list[Self]:
        # TODO validate params by creating a method in the child class
        if isinstance(payloads, list) and all(isinstance(t, dict) for t in payloads):
            # If a list of targets is provided, return a list of objects
            return cls._request_list(
                http_method="POST",
                adapter=adapter,
                endpoint=endpoint,
                jsons=payloads,
            )
        else:
            # If something other than dict or list[dict], raise error
            raise InvalidParameters("Invalid target(s)")

    @classmethod
    def put(
        cls, adapter: MetabaseApi, endpoint: str, payloads: list[dict]
    ) -> list[Self]:
        if isinstance(payloads, list) and all(isinstance(t, dict) for t in payloads):
            # If a list of targets is provided, return a list of objects
            return cls._request_list(
                http_method="PUT",
                adapter=adapter,
                endpoint=endpoint,
                jsons=payloads,
            )
        else:
            # If something other than dict or list[dict], raise error
            raise InvalidParameters("Invalid target(s)")

    @classmethod
    def archive(
        cls,
        adapter: MetabaseApi,
        endpoint: str,
        targets: list[int],
        unarchive: bool,
    ) -> list[Self]:
        if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
            return cls._request_list(
                http_method="PUT",
                adapter=adapter,
                endpoint=endpoint,
                jsons=[{"id": target, "archived": not unarchive} for target in targets],
            )
        else:
            raise InvalidParameters("Invalid set of targets")
