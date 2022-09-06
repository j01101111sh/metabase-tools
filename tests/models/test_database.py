import pytest

from metabase_tools import DatabaseItem, MetabaseApi


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
