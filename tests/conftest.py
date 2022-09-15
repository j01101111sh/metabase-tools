from datetime import datetime
from pathlib import Path

import pytest

from metabase_tools import MetabaseApi
from tests import helpers


@pytest.fixture(scope="session")
def credentials():
    return helpers.CREDENTIALS


@pytest.fixture(scope="session")
def host():
    return helpers.HOST


@pytest.fixture(scope="package")
def api(host, credentials):
    return MetabaseApi(
        metabase_url=host,
        credentials=credentials,
        cache_token=True,
    )
