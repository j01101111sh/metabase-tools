"""Unofficial API wrapper for Metabase
"""

__version__ = "0.11.1"

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
)
