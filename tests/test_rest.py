import pytest
from metabase_tools import RestAdapter
from metabase_tools.exceptions import AuthenticationFailure


@pytest.fixture
def credentials():
    from tests.metabase_details import CREDENTIALS
    return CREDENTIALS


@pytest.fixture
def host():
    from tests.metabase_details import HOST
    return HOST


def test_auth_success(host, credentials):
    rest_adapter = RestAdapter(metabase_url=host, credentials=credentials)
    assert rest_adapter.get_token() is not None


def test_auth_fail(host, credentials):
    bad_credentials = credentials
    bad_credentials['password'] = 'wrong'
    with pytest.raises(AuthenticationFailure):
        rest_adapter = RestAdapter(metabase_url=host, credentials=credentials)
