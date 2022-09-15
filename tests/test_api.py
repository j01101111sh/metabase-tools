import packaging.version
import pytest

from metabase_tools import MetabaseApi


def test_server_version(api: MetabaseApi):
    assert isinstance(api.server_version, packaging.version.Version)
