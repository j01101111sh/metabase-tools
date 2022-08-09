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


@pytest.fixture
def email():
    from tests.metabase_details import EMAIL
    return EMAIL


def test_auth_success(host, credentials):
    rest_adapter = RestAdapter(metabase_url=host, credentials=credentials)
    assert rest_adapter.get_token() is not None


def test_auth_fail(host, email):
    bad_credentials = {'username': email, 'password': 'badpass'}
    with pytest.raises(AuthenticationFailure):
        rest_adapter = RestAdapter(
            metabase_url=host, credentials=bad_credentials)
