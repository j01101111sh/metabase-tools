import packaging.version

from metabase_tools import DatabaseItem, MetabaseApi
from tests.helpers import random_string


def test_database_get_one(api: MetabaseApi):
    db_to_get = [1]
    db = api.databases.get(targets=db_to_get)
    assert isinstance(db, list)
    assert all(isinstance(d, DatabaseItem) for d in db)


def test_database_get_many(api: MetabaseApi):
    dbs_to_get = [1, 1]
    dbs = api.databases.get(targets=dbs_to_get)
    assert isinstance(dbs, list)
    assert all(isinstance(d, DatabaseItem) for d in dbs)


def test_database_get_all(api: MetabaseApi):
    dbs = api.databases.get()
    assert isinstance(dbs, list)
    assert all(isinstance(d, DatabaseItem) for d in dbs)


def test_database_create(api: MetabaseApi, server_version: packaging.version.Version):
    new_db = {
        "name": f"API DB - {random_string(6)}",
        "engine": "h2",
        "details": {
            "db": "zip:/app/metabase.jar!/sample-dataset.db;USER=GUEST;PASSWORD=guest"
        },
    }
    if server_version >= packaging.version.Version("v0.42"):
        new_db["details"]["db"] = new_db["details"]["db"].replace(
            "sample-dataset", "sample-database"
        )
    result = api.databases.create(**new_db)
    assert isinstance(result, DatabaseItem)


def test_database_search(api: MetabaseApi, server_version: packaging.version.Version):
    search_params = [{"name": "Sample Dataset"}]
    if server_version >= packaging.version.Version("v0.42"):
        search_params = [{"name": "Sample Database"}]
    result = api.databases.search(search_params=search_params)
    assert isinstance(result, list)
    assert all(isinstance(r, DatabaseItem) for r in result)
    assert len(result) == len(search_params)


def test_database_delete(api: MetabaseApi, server_version: packaging.version.Version):
    params = [{"name": "Test DB"}]
    db = api.databases.search(search_params=params)[0]
    assert isinstance(db, DatabaseItem)
    result = db.delete()
    assert isinstance(result, dict)
    new_db = {
        "name": "Test DB",
        "engine": "h2",
        "details": {
            "db": "zip:/app/metabase.jar!/sample-dataset.db;USER=GUEST;PASSWORD=guest"
        },
    }
    if server_version >= packaging.version.Version("v0.42"):
        new_db["details"]["db"] = new_db["details"]["db"].replace(
            "sample-dataset", "sample-database"
        )
    created_db = api.databases.create(**new_db)
    assert isinstance(created_db, DatabaseItem)


def test_database_update(api: MetabaseApi):
    params = [{"name": "Test DB"}]
    db = api.databases.search(search_params=params)[0]
    assert isinstance(db, DatabaseItem)
    renamed = db.update(name=f"Test DB - {random_string(6)}")
    assert isinstance(renamed, DatabaseItem)
    _ = renamed.update(name="Test DB")
