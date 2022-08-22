"""
    MetabaseGeneric class to provide generic methods for objects following this pattern
"""

from typing import Optional

from pydantic import BaseModel
from typing_extensions import Self

from metabase_tools.exceptions import EmptyDataReceived, InvalidParameters
from metabase_tools.metabase import MetabaseApi


class MetabaseGeneric(BaseModel):
    """Provides generic methods for objects following generic pattern"""

    id: int
    name: str

    @classmethod
    def _request_list(
        cls,
        http_method: str,
        adapter: MetabaseApi,
        endpoint: str,
        source: list[int] | list[dict],
    ) -> list[dict]:
        """Sends requests to API based on a list of objects

        Parameters
        ----------
        http_method : str
            GET or POST or PUT or DELETE
        adapter : MetabaseApi
            Connection to Metabase API
        endpoint : str
            Endpoint to use for the requests
        source : list[int] | list[dict]
            List of targets or payloads

        Returns
        -------
        list[Self]
            List of objects of the relevant type

        Raises
        ------
        InvalidParameters
            Targets and jsons are both None
        EmptyDataReceived
            No results returned from API
        """
        results = []

        for item in source:
            if isinstance(item, int):
                response = adapter.do(
                    http_method=http_method, endpoint=endpoint.format(id=item)
                )
            elif isinstance(item, dict):
                item_ep = endpoint.format(**item)
                if http_method == "PUT":
                    response = adapter.do(
                        http_method=http_method,
                        endpoint=item_ep,
                        json=item,
                    )
                else:
                    response = adapter.do(
                        http_method=http_method,
                        endpoint=item_ep,
                        json=item,
                    )
            else:
                raise InvalidParameters
            if response.data and isinstance(response.data, dict):
                results.append(response.data)
            elif response.data and isinstance(response.data, list):
                results.extend(response.data)
        if len(results) > 0:
            return results
        raise EmptyDataReceived("No data returned")

    @classmethod
    def get(
        cls, adapter: MetabaseApi, endpoint: str, targets: Optional[list[int]] = None
    ) -> list[Self]:
        """Generic method for returning an object or list of objects

        Parameters
        ----------
        adapter : MetabaseApi
            Connection to Metabase API
        endpoint : str
            Endpoint to use for the request
        targets : Optional[list[int]]
            If None, return all objects; else return the objects requested

        Returns
        -------
        list[Self]
            List of objects of the relevant type

        Raises
        ------
        InvalidParameters
            Targets are not None or list[int]
        EmptyDataReceived
            No data is received from the API
        """
        if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
            results = cls._request_list(
                http_method="GET",
                adapter=adapter,
                endpoint=endpoint + "/{id}",
                source=targets,
            )
            return [cls(**result) for result in results]

        if targets is None:
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
        """Generic method for creating a list of objects

        Parameters
        ----------
        adapter : MetabaseApi
            Connection to Metabase API
        endpoint : str
            Endpoint to use for the requests
        payloads : list[dict]
            List of json payloads

        Returns
        -------
        list[Self]
            List of objects of the relevant type

        Raises
        ------
        InvalidParameters
            Targets and jsons are both None
        EmptyDataReceived
            No results returned from API
        """
        # TODO validate params by creating a method in the child class
        if isinstance(payloads, list) and all(isinstance(t, dict) for t in payloads):
            # If a list of targets is provided, return a list of objects
            results = cls._request_list(
                http_method="POST",
                adapter=adapter,
                endpoint=endpoint,
                source=payloads,
            )
            return [cls(**result) for result in results]
        # If something other than dict or list[dict], raise error
        raise InvalidParameters("Invalid target(s)")

    @classmethod
    def put(
        cls, adapter: MetabaseApi, endpoint: str, payloads: list[dict]
    ) -> list[Self]:
        """Generic method for updating a list of objects

        Parameters
        ----------
        adapter : MetabaseApi
            Connection to Metabase API
        endpoint : str
            Endpoint to use for the requests
        payloads : list[dict]
            List of json payloads

        Returns
        -------
        list[Self]
            List of objects of the relevant type

        Raises
        ------
        InvalidParameters
            Targets and jsons are both None
        EmptyDataReceived
            No results returned from API
        """
        if isinstance(payloads, list) and all(isinstance(t, dict) for t in payloads):
            # If a list of targets is provided, return a list of objects
            results = cls._request_list(
                http_method="PUT",
                adapter=adapter,
                endpoint=endpoint,
                source=payloads,
            )
            return [cls(**result) for result in results]
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
        """Generic method for archiving a list of objects

        Parameters
        ----------
        adapter : MetabaseApi
            Connection to Metabase API
        endpoint : str
            Endpoint to use for the requests
        payloads : list[dict]
            List of json payloads

        Returns
        -------
        list[Self]
            List of objects of the relevant type

        Raises
        ------
        InvalidParameters
            Targets and jsons are both None
        EmptyDataReceived
            No results returned from API
        """
        if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
            results = cls._request_list(
                http_method="PUT",
                adapter=adapter,
                endpoint=endpoint,
                source=[
                    {"id": target, "archived": not unarchive} for target in targets
                ],
            )
            return [cls(**result) for result in results]
        raise InvalidParameters("Invalid set of targets")

    @classmethod
    def search(
        cls,
        adapter: MetabaseApi,
        search_params: list[dict],
        search_list: Optional[list[Self]] = None,
    ) -> list[Self]:
        """Method to search a list of objects meeting a list of parameters

        Parameters
        ----------
        adapter : MetabaseApi
            Connection to Metabase API
        endpoint : str
            Endpoint to use for the requests
        search_params : list[dict]
            List of dicts, each containing search criteria. 1 result returned per dict.
        search_list : Optional[list[Self]], optional
            Provide to search against an existing list, by default pulls from API

        Returns
        -------
        list[Self]
            List of objects of the relevant type
        """
        # TODO add tests for search
        objs = search_list or cls.get(adapter=adapter)  # type: ignore
        results = []
        for param in search_params:
            for obj in objs:
                obj_dict = obj.dict()
                for key, value in param.items():
                    if key in obj_dict and value == obj_dict[key]:
                        results.append(obj)
        return results

    @classmethod
    def delete(cls, adapter: MetabaseApi, endpoint: str, targets: list[int]) -> dict:
        if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
            results = cls._request_list(
                http_method="DELETE",
                adapter=adapter,
                endpoint=endpoint,
                source=targets,
            )
            return {target: result for result, target in zip(results, targets)}
        raise InvalidParameters("Invalid set of targets")
