import pytest

from metabase_tools import Collection, MetabaseApi


@pytest.fixture(scope="module")
def new_coll_def():
    new_coll_def = {
        "name": "API Created",
        "color": "#FFFFFF",
    }
    return new_coll_def


def test_coll_create_one(api: MetabaseApi, new_coll_def: dict):
    new_coll_objs = Collection.create(adapter=api, payloads=[new_coll_def])
    assert isinstance(new_coll_objs, list)
    assert all(isinstance(coll, Collection) for coll in new_coll_objs)


def test_collection_create_many(api: MetabaseApi, new_coll_def: dict):
    new_colls = [new_coll_def, new_coll_def]
    new_coll_objs = Collection.create(adapter=api, payloads=new_colls)
    assert isinstance(new_coll_objs, list)
    assert all(isinstance(coll, Collection) for coll in new_coll_objs)


def test_collection_update_one(api: MetabaseApi, run_id: str):
    coll_change = [
        {"id": 3, "description": f"Updated {run_id}"},
        {"id": 4, "description": f"Updated {run_id}"},
    ]
    change_result = Collection.update(adapter=api, payload=coll_change)
    assert isinstance(change_result, list)
    assert all(isinstance(coll, Collection) for coll in change_result)
    assert all(coll.description == f"Updated {run_id}" for coll in change_result)


def test_collection_update_many(api: MetabaseApi, run_id):
    coll_changes = {"id": 2, "description": f"Updated {run_id}"}
    change_results = Collection.update(adapter=api, payload=[coll_changes])
    assert isinstance(change_results, list)
    assert all(isinstance(coll, Collection) for coll in change_results)
    assert all(coll.description == f"Updated {run_id}" for coll in change_results)


def test_collection_archive_one(api: MetabaseApi):
    coll_to_archive = 2
    change_result = Collection.archive(adapter=api, target=[coll_to_archive])
    assert isinstance(change_result, list)
    assert all(isinstance(coll, Collection) for coll in change_result)
    assert all(coll.archived is True for coll in change_result)


def test_collection_archive_many(api: MetabaseApi):
    colls_to_archive = [3, 4]
    change_results = Collection.archive(adapter=api, target=colls_to_archive)
    assert isinstance(change_results, list)
    assert all(isinstance(coll, Collection) for coll in change_results)
    assert all(coll.archived is True for coll in change_results)


def test_collection_unarchive_one(api: MetabaseApi):
    coll_to_unarchive = 2
    change_result = Collection.archive(
        adapter=api, target=[coll_to_unarchive], unarchive=True
    )
    assert isinstance(change_result, list)
    assert all(isinstance(coll, Collection) for coll in change_result)
    assert all(coll.archived is False for coll in change_result)


def test_collection_unarchive_many(api: MetabaseApi):
    colls_to_archive = [3, 4]
    change_results = Collection.archive(
        adapter=api, target=colls_to_archive, unarchive=True
    )
    assert isinstance(change_results, list)
    assert all(isinstance(coll, Collection) for coll in change_results)
    assert all(coll.archived is False for coll in change_results)


def test_collection_get_one(api: MetabaseApi):
    coll_to_get = 2
    coll = Collection.get(adapter=api, targets=[coll_to_get])
    assert isinstance(coll, list)
    assert all(isinstance(c, Collection) for c in coll)


def test_collection_get_many(api: MetabaseApi):
    colls_to_get = [3, 4]
    colls = Collection.get(adapter=api, targets=colls_to_get)
    assert isinstance(colls, list)
    assert all(isinstance(coll, Collection) for coll in colls)


def test_collection_get_all(api: MetabaseApi):
    colls = Collection.get(adapter=api)
    assert isinstance(colls, list)
    assert all(isinstance(coll, Collection) for coll in colls)


def test_get_collection_tree(api: MetabaseApi):
    coll_tree = Collection.get_tree(adapter=api)
    assert isinstance(coll_tree, list)
    assert all(isinstance(coll, dict) for coll in coll_tree)


def test_flatten_tree(api: MetabaseApi):
    collections = Collection.get_flat_list(adapter=api)
    assert isinstance(collections, list)
    assert all(isinstance(collection, dict) for collection in collections)


def test_graph(api: MetabaseApi):
    graph = Collection.graph(adapter=api)
    assert isinstance(graph, dict)
