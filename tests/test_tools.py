from datetime import datetime

import pytest
from metabase_tools import MetabaseTools


@pytest.fixture(scope='module')
def tools(host, credentials):
    return MetabaseTools(metabase_url=host, credentials=credentials, cache_token=True, token_path='./metabase.token')


@pytest.fixture(scope='module')
def credentials():
    from tests.metabase_details import CREDENTIALS
    return CREDENTIALS


@pytest.fixture(scope='module')
def host():
    from tests.metabase_details import HOST
    return HOST


def test_auth(tools):
    token = tools._rest_adapter.get_token()
    assert token is not None


def test_download_native_queries(tools):
    f = tools.download_native_queries(save_path='./scratch/files/')
    size = f.stat().st_size
    create_time = f.stat().st_ctime
    now = datetime.now().timestamp()
    assert size > 0  # File size greater than 0
    assert create_time - now < 2  # file was created in the last 2 seconds
    f.unlink()  # remove created file
