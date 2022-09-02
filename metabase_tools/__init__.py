"""Unofficial API wrapper for Metabase
"""

__version__ = "0.7.0"

from metabase_tools.exceptions import (
    AuthenticationFailure,
    EmptyDataReceived,
    InvalidDataReceived,
    InvalidParameters,
    ItemInPersonalCollection,
    ItemNotFound,
    MetabaseApiException,
    NoUpdateProvided,
    RequestFailure,
)
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.card_model import CardItem, CardQueryResult
from metabase_tools.models.collection_model import Collection
from metabase_tools.models.database_model import Database
from metabase_tools.models.user_model import User
from metabase_tools.tools import MetabaseTools

__all__ = (
    "AuthenticationFailure",
    "EmptyDataReceived",
    "InvalidDataReceived",
    "InvalidParameters",
    "ItemNotFound",
    "ItemInPersonalCollection",
    "MetabaseApiException",
    "NoUpdateProvided",
    "RequestFailure",
    "MetabaseApi",
    "CardItem",
    "CardQueryResult",
    "Collection",
    "Database",
    "User",
    "MetabaseTools",
)
