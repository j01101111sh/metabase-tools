"""Unofficial API wrapper for Metabase
"""

__version__ = "0.12.0"

from metabase_tools.exceptions import MetabaseApiException
from metabase_tools.metabase import MetabaseApi

__all__ = ("MetabaseApiException", "MetabaseApi")
