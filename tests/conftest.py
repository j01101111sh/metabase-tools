from datetime import datetime
from pathlib import Path

import pytest

from metabase_tools import MetabaseApi
from tests import helpers

_run_id = datetime.now().strftime("%y%m%dT%H%M%S")
_result_path = Path(f"./temp/test-{_run_id}")


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
