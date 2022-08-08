import pytest
from metabase_tools import RestAdapter
from metabase_tools.exceptions import AuthenticationFailure

from tests.metabase_details import CREDENTIALS, HOST


def test_auth_success():
    rest_adapter = RestAdapter(metabase_url=HOST, credentials=CREDENTIALS)
    assert rest_adapter.get_token() is not None


def test_auth_fail():
    bad_credentials = CREDENTIALS
    CREDENTIALS['password'] = 'wrong'
    with pytest.raises(AuthenticationFailure):
        rest_adapter = RestAdapter(metabase_url=HOST, credentials=CREDENTIALS)
