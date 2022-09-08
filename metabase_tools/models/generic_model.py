"""
    Generic classes for Metabase
"""
from __future__ import annotations

import logging
from abc import ABC
from typing import TYPE_CHECKING, Any, ClassVar, Optional, TypeVar

from pydantic import BaseModel, PrivateAttr

from metabase_tools.common import log_call
from metabase_tools.exceptions import InvalidParameters

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

T = TypeVar("T", bound="Item")
logger = logging.getLogger(__name__)


class Item(BaseModel, ABC, extra="forbid"):
    """Base class for all Metabase objects. Provides generic fields and methods."""

    _BASE_EP: ClassVar[str]

    _adapter: Optional[MetabaseApi] = PrivateAttr(None)

    id: int | str
    name: str

    def set_adapter(self, adapter: MetabaseApi) -> None:
        """Sets the adapter on an object

        Args:
            adapter (MetabaseApi): Connection to MetabaseApi
        """
        self._adapter = adapter

    def update(self: T, payload: dict[str, Any]) -> T:
        """Generic method for updating an object

        Args:
            payloads (dict): Details of update

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            T: Object of the relevant type
        """
        if self._adapter:
            result = self._adapter.put(
                endpoint=self._BASE_EP.format(id=self.id), json=payload
            )
            if isinstance(result, dict):
                obj = self.__class__(**result)
                obj.set_adapter(adapter=self._adapter)
                return obj
        raise InvalidParameters("Invalid target(s)")

    def archive(self: T) -> T:
        """Generic method for archiving an object

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            T: Object of the relevant type
        """
        payload = {"id": self.id, "archived": True}
        if self._adapter:
            result = self._adapter.put(
                endpoint=self._BASE_EP.format(id=self.id), json=payload
            )
            if isinstance(result, dict):
                obj = self.__class__(**result)
                obj.set_adapter(self._adapter)
                return obj
        raise InvalidParameters("Invalid target(s)")

    def unarchive(self: T) -> T:
        """Generic method for unarchiving an object

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            T: Object of the relevant type
        """
        payload = {"id": self.id, "archived": False}
        if self._adapter:
            result = self._adapter.put(
                endpoint=self._BASE_EP.format(id=self.id), json=payload
            )
            if isinstance(result, dict):
                obj = self.__class__(**result)
                obj.set_adapter(self._adapter)
                return obj
        raise InvalidParameters("Invalid target(s)")

    @log_call
    def delete(self) -> dict[int | str, dict[str, Any]]:
        """Method to delete an object

        Raises:
            InvalidParameters: Invalid target

        Returns:
            dict: Results
        """
        if self._adapter:
            result = self._adapter.delete(endpoint=self._BASE_EP.format(id=self.id))
            if isinstance(result, dict):
                final = {self.id: result}
                return final
        raise InvalidParameters("Invalid target(s)")
