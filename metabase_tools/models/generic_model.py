"""
    Generic classes for Metabase
"""
from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, ClassVar, Optional, TypeVar

from pydantic import BaseModel, PrivateAttr

from metabase_tools.exceptions import InvalidParameters

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

T = TypeVar("T", bound="Item")


class Item(BaseModel, ABC, extra="forbid"):
    """Base class for all Metabase objects. Provides generic fields and methods."""

    _BASE_EP: ClassVar[str]

    _adapter: Optional[MetabaseApi] = PrivateAttr(None)

    id: int | str
    name: str

    def set_adapter(self, adapter: MetabaseApi) -> None:
        self._adapter = adapter

    def update(self: T, payload: dict[str, Any]) -> T:
        """Generic method for updating an object

        Args:
            payloads (list[dict]): List of json payloads

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            list[Self]: List of objects of the relevant type
        """
        if self._adapter:
            try:
                result = self._adapter.put(
                    endpoint=self._BASE_EP.format(**payload), json=payload
                )
            except KeyError:
                result = None
            if isinstance(result, dict):
                obj = self.__class__(**result)
                obj.set_adapter(adapter=self._adapter)
                return obj
        raise InvalidParameters("Invalid target(s)")

    def archive(self: T, unarchive: bool = False) -> T:
        """Generic method for archiving an of object

        Args:
            unarchive (bool): Whether object should be unarchived instead of archived

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            list[Self]: List of objects of the relevant type
        """
        payload = {"id": self.id, "archived": not unarchive}
        if self._adapter:
            result = self._adapter.put(
                endpoint=self._BASE_EP.format(**payload), json=payload
            )
            if isinstance(result, dict):
                obj = self.__class__(**result)
                obj.set_adapter(self._adapter)
                return obj
        raise InvalidParameters("Invalid target(s)")

    def delete(self) -> dict[int | str, dict[str, Any]]:
        """Method to delete an object

        Raises:
            InvalidParameters: Targets is not a list of ints

        Returns:
            dict: _description_
        """
        if self._adapter:
            result = self._adapter.delete(endpoint=self._BASE_EP)
            if isinstance(result, dict):
                final = {self.id: result}
                return final
        raise InvalidParameters("Invalid target(s)")
        # if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
        #     results = cls._request_list(
        #         http_method="DELETE",
        #         adapter=adapter,
        #         endpoint=cls.BASE_EP + "/{id}",
        #         source=targets,
        #     )
        #     return {target: result for result, target in zip(results, targets)}
        # raise InvalidParameters("Invalid set of targets")
