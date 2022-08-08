from metabase_tools import RestAdapter

from tests.metabase_details import CREDENTIALS, HOST


def test_authentication():
    rest_adapter = RestAdapter(metabase_url=HOST, credentials=CREDENTIALS)
    assert rest_adapter.get_token() is not None
