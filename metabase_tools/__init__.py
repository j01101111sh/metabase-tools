from . import _version

__version__ = _version.get_versions()['version']

from .exceptions import MetabaseApiException
from .metabase_api import MetabaseApi
