import random

import pytest

from metabase_tools import CollectionItem, MetabaseApi


@pytest.fixture(scope="module")
def collections(api: MetabaseApi) -> list[CollectionItem]:
    collections = api.collections.get()[1:]
    collections = [coll for coll in collections if coll.personal_owner_id is None]
    return collections


@pytest.fixture(scope="module")
def new_coll_def():
    new_coll_def = {
        "name": "API Created",
        "color": "#FFFFFF",
    }
    return new_coll_def


def test_collection_create_one(api: MetabaseApi, new_coll_def: dict):
    new_coll_objs = api.collections.create(payloads=[new_coll_def])
    assert isinstance(new_coll_objs, list)
    assert all(isinstance(coll, CollectionItem) for coll in new_coll_objs)


def test_collection_create_many(api: MetabaseApi, new_coll_def: dict):
    new_colls = [new_coll_def, new_coll_def]
    new_coll_objs = api.collections.create(payloads=new_colls)
    assert isinstance(new_coll_objs, list)
    assert all(isinstance(coll, CollectionItem) for coll in new_coll_objs)


def test_collection_update_one(collections: list[CollectionItem], run_id: str):
    coll = random.choice(collections)
    coll_change = {"id": 3, "description": f"Updated {run_id}"}
    change_result = coll.update(payload=coll_change)
    assert isinstance(change_result, CollectionItem)


def test_collection_archive_one(collections: list[CollectionItem]):
    coll_to_archive = random.choice(collections)
    try:
        _ = coll_to_archive.archive(unarchive=True)
    except:
        pass
    change_result = coll_to_archive.archive()
    _ = coll_to_archive.archive(unarchive=True)
    assert isinstance(change_result, CollectionItem)
    assert change_result.archived is True


def test_collection_unarchive_one(collections: list[CollectionItem]):
    coll_to_archive = random.choice(collections)
    try:
        _ = coll_to_archive.archive()
    except:
        pass
    change_result = coll_to_archive.archive(unarchive=True)
    assert isinstance(change_result, CollectionItem)
    assert change_result.archived is False


def test_collection_get_one(api: MetabaseApi):
    coll_to_get = 2
    coll = api.collections.get(targets=[coll_to_get])
    assert isinstance(coll, list)
    assert all(isinstance(c, CollectionItem) for c in coll)


def test_collection_get_many(api: MetabaseApi):
    colls_to_get = [3, 4]
    colls = api.collections.get(targets=colls_to_get)
    assert isinstance(colls, list)
    assert all(isinstance(coll, CollectionItem) for coll in colls)


def test_collection_get_all(api: MetabaseApi):
    colls = api.collections.get()
    assert isinstance(colls, list)
    assert all(isinstance(coll, CollectionItem) for coll in colls)


def test_get_collection_tree(api: MetabaseApi):
    coll_tree = api.collections.get_tree()
    assert isinstance(coll_tree, list)
    assert all(isinstance(coll, dict) for coll in coll_tree)


def test_flatten_tree(api: MetabaseApi):
    collections = api.collections.get_flat_list()
    assert isinstance(collections, list)
    assert all(isinstance(collection, dict) for collection in collections)


def test_collection_graph(api: MetabaseApi):
    graph = api.collections.graph()
    assert isinstance(graph, dict)


def test_collection_search(api: MetabaseApi):
    search_params = [{"name": "Development"}]
    result = api.collections.search(search_params=search_params)
    assert isinstance(result, list)
    assert all(isinstance(coll, CollectionItem) for coll in result)
    assert len(search_params) == len(result)
