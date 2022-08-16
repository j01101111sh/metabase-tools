import pytest

from metabase_tools import Database, MetabaseApi


@pytest.fixture(scope="module")
def api(host, credentials):
    return MetabaseApi(
        metabase_url=host,
        credentials=credentials,
        cache_token=True,
        token_path="./metabase.token",
    )


@pytest.fixture(scope="module")
def credentials():
    from tests.metabase_details import CREDENTIALS

    return CREDENTIALS


@pytest.fixture(scope="module")
def host():
    from tests.metabase_details import HOST

    return HOST


def test_Database_get_one(api: MetabaseApi):
    db_to_get = [1]
    db = Database.get(adapter=api, targets=db_to_get)
    assert isinstance(db, list)
    assert all(isinstance(d, Database) for d in db)


def test_Database_get_many(api: MetabaseApi):
    dbs_to_get = [1, 1]
    dbs = Database.get(adapter=api, targets=dbs_to_get)
    assert isinstance(dbs, list)
    assert all(isinstance(d, Database) for d in dbs)


def test_Database_get_all(api: MetabaseApi):
    dbs = Database.get(adapter=api)
    assert isinstance(dbs, list)
    assert all(isinstance(d, Database) for d in dbs)
