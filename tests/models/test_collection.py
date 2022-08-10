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


def test_collection_create_one(api: MetabaseApi):
    # TODO
    pass


def test_collection_create_many(api: MetabaseApi):
    # TODO
    pass


def test_collection_update_one(api: MetabaseApi):
    # TODO
    pass


def test_collection_update_many(api: MetabaseApi):
    # TODO
    pass


def test_collection_archive_one(api: MetabaseApi):
    # TODO
    pass


def test_collection_archive_many(api: MetabaseApi):
    # TODO
    pass


def test_collection_unarchive_one(api: MetabaseApi):
    # TODO
    pass


def test_collection_unarchive_many(api: MetabaseApi):
    # TODO
    pass


def test_collection_get_one(api: MetabaseApi):
    # TODO
    pass


def test_collection_get_many(api: MetabaseApi):
    # TODO
    pass


def test_collection_get_all(api: MetabaseApi):
    collections = Collection.get(adapter=api)
    assert isinstance(collections, list)
    assert all(isinstance(collection, Collection)
               for collection in collections)


def test_get_collection_tree(api: MetabaseApi):
    collection_tree = Collection.get_tree(adapter=api)
    assert isinstance(collection_tree, list)
    assert all(isinstance(collection, dict) for collection in collection_tree)


def test_flatten_tree(api: MetabaseApi):
    collections = Collection.get_flat_list(adapter=api)
    assert isinstance(collections, list)
    assert all(isinstance(collection, dict) for collection in collections)
