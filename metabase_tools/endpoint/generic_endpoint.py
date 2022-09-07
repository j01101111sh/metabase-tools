"""Generic methods for endpoints
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Optional, TypeVar

from metabase_tools.common import log_call
from metabase_tools.exceptions import EmptyDataReceived, InvalidParameters
from metabase_tools.models.generic_model import Item

if TYPE_CHECKING:
    from metabase_tools import MetabaseApi

T = TypeVar("T", bound=Item)

logger = logging.getLogger(__name__)


class Endpoint(ABC, Generic[T]):
    """Abstract base class for endpoints"""

    _BASE_EP: ClassVar[str]
    _STD_OBJ: ClassVar[type]
    _adapter: MetabaseApi

    def __init__(self, adapter: MetabaseApi):
        self._adapter = adapter

    @log_call
    def _request_list(
        self,
        http_method: str,
        endpoint: str,
        source: list[int] | list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Sends requests to API based on a list of objects

        Args:
            http_method (str): GET or POST or PUT or DELETE
            endpoint (str): Endpoint to use for request
            source (list[int] | list[dict]): List of targets or payloads

        Raises:
            InvalidParameters: Item in source is not an int or dict
            EmptyDataReceived: No data returned

        Returns:
            list[dict]: Aggregated results of all API calls
        """
        results = []

        for item in source:
            if isinstance(item, int):
                response = self._adapter.generic_request(
                    http_method=http_method, endpoint=endpoint.format(id=item)
                )
            elif isinstance(item, dict):
                item_ep = endpoint.format(**item)
                response = self._adapter.generic_request(
                    http_method=http_method,
                    endpoint=item_ep,
                    json=item,
                )
            else:
                raise InvalidParameters
            if isinstance(response, dict):
                results.append(response)
        if len(results) > 0:
            return results
        raise EmptyDataReceived("No data returned")

    @abstractmethod
    def get(self, targets: Optional[list[int]] = None) -> list[T]:
        """Generic method for returning an object or list of objects

        Args:
            targets (list[int], optional): IDs of the objects being requested

        Raises:
            InvalidParameters: Targets are not None or list[int]
            EmptyDataReceived: No data is received from the API

        Returns:
            list[T]: List of objects of the relevant type
        """
        if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
            results = self._request_list(
                http_method="GET",
                endpoint=self._BASE_EP + "/{id}",
                source=targets,
            )
            objs = [self._STD_OBJ(**result) for result in results]
            for obj in objs:
                obj.set_adapter(self._adapter)
            return objs

        if targets is None:
            # If no targets are provided, all objects of that type should be returned
            response = self._adapter.get(endpoint=self._BASE_EP)
            if isinstance(response, list):  # Validate data was returned
                # Unpack data into instances of the class and return
                objs = [
                    self._STD_OBJ(**record)
                    for record in response
                    if isinstance(record, dict)
                ]
                for obj in objs:
                    obj.set_adapter(self._adapter)
                return objs
        else:
            # If something other than None, int or list[int], raise error
            raise InvalidParameters("Invalid target(s)")
        # If response.data was empty, raise error
        raise EmptyDataReceived("No data returned")

    @abstractmethod
    def create(self, payloads: list[dict[str, Any]]) -> list[T]:
        """Generic method for creating a list of objects

        Args:
            payloads (list[dict]): List of json payloads

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            list[T]: List of objects of the relevant type
        """
        if isinstance(payloads, list) and all(isinstance(t, dict) for t in payloads):
            # If a list of targets is provided, return a list of objects
            results = self._request_list(
                http_method="POST",
                endpoint=self._BASE_EP,
                source=payloads,
            )
            objs = [self._STD_OBJ(**result) for result in results]
            for obj in objs:
                obj.set_adapter(self._adapter)
            return objs
        # If something other than dict or list[dict], raise error
        raise InvalidParameters("Invalid target(s)")

    @abstractmethod
    def search(
        self,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[T]] = None,
    ) -> list[T]:
        """Method to search a list of objects meeting a list of parameters

        Args:
            search_params (list[dict]): Each dict contains search criteria and returns\
                 1 result
            search_list (list[T], optional): Provide to search against an existing \
                list, by default pulls from API

        Returns:
            list[T]: List of objects of the relevant type
        """
        objs = search_list or self.get()
        results = []
        for param in search_params:
            for obj in objs:
                obj_dict = obj.dict()
                for key, value in param.items():
                    if key in obj_dict and value == obj_dict[key]:
                        results.append(obj)
        return results
