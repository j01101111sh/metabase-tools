import pytest

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


def test_database_create(api: MetabaseApi):
    new_db = {
        "name": f"API DB - {random_string(6)}",
        "engine": "h2",
        "details": {
            "db": "zip:/app/metabase.jar!/sample-dataset.db;USER=GUEST;PASSWORD=guest"
        },
    }
    result = api.databases.create(payloads=[new_db])
    assert isinstance(result, list)
    assert all(isinstance(r, DatabaseItem) for r in result)


def test_database_search(api: MetabaseApi):
    search_params = [{"name": "Sample Dataset"}]
    result = api.databases.search(search_params=search_params)
    assert isinstance(result, list)
    assert all(isinstance(r, DatabaseItem) for r in result)
    assert len(result) == len(search_params)
