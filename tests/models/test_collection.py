import pytest
from metabase_tools import Collection, MetabaseApi


@pytest.fixture(scope='module')
def api(host, credentials):
    return MetabaseApi(metabase_url=host, credentials=credentials, cache_token=True, token_path='./metabase.token')


@pytest.fixture(scope='module')
def credentials():
    from tests.metabase_details import CREDENTIALS
    return CREDENTIALS


@pytest.fixture(scope='module')
def host():
    from tests.metabase_details import HOST
    return HOST


def test_collection_list_all(api):
    collections = Collection.get(adapter=api)
    assert isinstance(collections, list)
    assert all(isinstance(collection, Collection)
               for collection in collections)


def test_collection_tree(api):
    collection_tree = Collection.get_tree(adapter=api)
    assert isinstance(collection_tree, list)
    assert all(isinstance(collection, dict) for collection in collection_tree)


def test_flat_tree(api):
    collections = Collection.get_flat_list(adapter=api)
    assert isinstance(collections, list)
    assert all(isinstance(collection, dict) for collection in collections)
