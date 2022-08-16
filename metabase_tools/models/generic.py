from typing import Optional

from pydantic import BaseModel
from typing_extensions import Self

from metabase_tools.exceptions import EmptyDataReceived, InvalidParameters
from metabase_tools.metabase import MetabaseApi


class MetabaseGeneric(BaseModel):
    id: int
    name: str

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
            results = []
            for target in targets:
                response = adapter.get(endpoint=f"{endpoint}/{target}")
                if response.data and isinstance(response.data, dict):
                    results.append(cls(**response.data))
            if len(results) > 0:
                return results
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
        # TODO docstring
        # TODO refactor for DRY
        if isinstance(payloads, list) and all(isinstance(t, dict) for t in payloads):
            # If a list of targets is provided, return a list of objects
            results = []
            for payload in payloads:
                response = adapter.post(endpoint=f"{endpoint}", json=payload)
                if response.data and isinstance(response.data, dict):
                    results.append(cls(**response.data))
            if len(results) > 0:
                return results
        else:
            # If something other than dict or list[dict], raise error
            raise InvalidParameters("Invalid target(s)")
        # If response.data was empty or not a valid type, raise error
        raise EmptyDataReceived("No data returned")

    @classmethod
    def put(
        cls, adapter: MetabaseApi, endpoint: str, payloads: list[dict]
    ) -> list[Self]:
        # TODO docstring
        if isinstance(payloads, list) and all(isinstance(t, dict) for t in payloads):
            # If a list of targets is provided, return a list of objects
            results = []
            for payload in payloads:
                response = adapter.put(
                    endpoint=f"{endpoint}/{payload['id']}", json=payload
                )
                if response.data and isinstance(response.data, dict):
                    results.append(cls(**response.data))
            if len(results) > 0:
                return results
        else:
            # If something other than dict or list[dict], raise error
            raise InvalidParameters("Invalid target(s)")
        # If response.data was empty or not a valid type, raise error
        raise EmptyDataReceived("No data returned")

    @classmethod
    def archive(
        cls,
        adapter: MetabaseApi,
        endpoint: str,
        targets: list[int],
        unarchive: bool,
    ) -> list[Self]:
        archive_template = {"id": None, "archived": not unarchive}
        if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
            results = []
            for target in targets:
                archive_template["id"] = target
                response = adapter.put(
                    endpoint=f"{endpoint}/{target}", json=archive_template
                )
                if response.data and isinstance(response.data, dict):
                    results.append(cls(**response.data))
            if len(results) > 0:
                return results
        else:
            raise InvalidParameters("Invalid set of targets")
        raise EmptyDataReceived("No data returned")

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
