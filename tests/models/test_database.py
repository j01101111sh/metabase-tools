import pytest

from metabase_tools import Database, MetabaseApi


def test_database_get_one(api: MetabaseApi):
    db_to_get = [1]
    db = Database.get(adapter=api, targets=db_to_get)
    assert isinstance(db, list)
    assert all(isinstance(d, Database) for d in db)


def test_database_get_many(api: MetabaseApi):
    dbs_to_get = [1, 1]
    dbs = Database.get(adapter=api, targets=dbs_to_get)
    assert isinstance(dbs, list)
    assert all(isinstance(d, Database) for d in dbs)


def test_database_get_all(api: MetabaseApi):
    dbs = Database.get(adapter=api)
    assert isinstance(dbs, list)
    assert all(isinstance(d, Database) for d in dbs)
