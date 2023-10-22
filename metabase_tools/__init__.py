"""Unofficial API wrapper for Metabase
"""

__version__ = "0.16.0"

from beartype.claw import beartype_this_package

from metabase_tools.exceptions import MetabaseApiException
from metabase_tools.metabase import MetabaseApi

__all__ = ("MetabaseApiException", "MetabaseApi")

beartype_this_package()
