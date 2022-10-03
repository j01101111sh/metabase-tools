import random
from types import LambdaType

import pytest
from packaging.version import Version

from metabase_tools.exceptions import MetabaseApiException
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.collection_model import CollectionItem


@pytest.fixture(scope="module")
def items(api: MetabaseApi) -> list[CollectionItem]:
    return [
        item
        for item in api.collections.get()
        if item.id != "root" and item.personal_owner_id is None
    ]


class TestModelMethodsCommonPass:
    def test_update(self, items: list[CollectionItem], run_id: str):
        target = random.choice(items)
        result = target.update(description=f"Updated {run_id}")
        assert isinstance(result, CollectionItem)  # check item class
        assert result.description == f"Updated {run_id}"  # check action result
        assert target.id == result.id  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_archive(self, items: list[CollectionItem]):
        target = random.choice(items)
        result = target.archive()
        _ = target.unarchive()
        assert isinstance(result, CollectionItem)  # check item class
        assert result.archived is True  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_unarchive(self, items: list[CollectionItem]):
        target = random.choice(items)
        result = target.unarchive()
        assert isinstance(result, CollectionItem)  # check item class
        assert result.archived is False  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_refresh(self, items: list[CollectionItem], random_string: LambdaType):
        target = random.choice(items)
        result = target.update(description="Updated " + random_string(5))
        target = target.refresh()
        assert isinstance(target, CollectionItem)  # check item class
        assert target.description == result.description  # check action result
        assert isinstance(target._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            target._adapter.server_version, Version
        )  # check adapter initialized


class TestModelMethodsCommonFail:
    def test_update_fail(self, items: list[CollectionItem]):
        target = random.choice(items)
        with pytest.raises(MetabaseApiException):
            _ = target.update(color=3)  # type: ignore

    def test_archive_fail(self, api: MetabaseApi):
        target = api.collections.get()[0]
        target.id = -1
        with pytest.raises(MetabaseApiException):
            _ = target.archive()  # type: ignore

    def test_unarchive_fail(self, api: MetabaseApi):
        target = api.collections.get()[0]
        target.id = -1
        with pytest.raises(MetabaseApiException):
            _ = target.unarchive()  # type: ignore

    def test_delete_fail(self, items: list[CollectionItem]):
        target = random.choice(items)
        with pytest.raises(NotImplementedError):
            _ = target.delete()  # type: ignore


class TestEndpointMethodsCommonPass:
    def test_create(self, api: MetabaseApi, random_string: LambdaType):
        name = "Test - " + random_string(6)
        definition = {
            "name": name,
            "color": "#FFFFFF",
        }
        result = api.collections.create(**definition)
        assert isinstance(result, CollectionItem)  # check item class
        assert result.name == name  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter is initialized correctly

    def test_get_one(self, api: MetabaseApi, items: list[CollectionItem]):
        item_ids = [item.id for item in items if isinstance(item.id, int)]
        target = random.sample(item_ids, 1)
        result = api.collections.get(targets=target)
        assert isinstance(result, list)  # check item class
        assert all(
            isinstance(item, CollectionItem) for item in result
        )  # check item class
        assert all(item.id in target for item in result)  # check action result
        assert len(result) == len(target)  # check action result
        assert all(
            isinstance(item._adapter, MetabaseApi) for item in result
        )  # check adapter set
        assert all(
            item._adapter and isinstance(item._adapter.server_version, Version)
            for item in result
        )  # check adapter initialized

    def test_get_many(self, api: MetabaseApi, items: list[CollectionItem]):
        item_ids = [item.id for item in items if isinstance(item.id, int)]
        target = random.sample(item_ids, 2)
        result = api.collections.get(targets=target)
        assert isinstance(result, list)  # check item class
        assert all(
            isinstance(item, CollectionItem) for item in result
        )  # check item class
        assert all(item.id in target for item in result)  # check action result
        assert len(result) == len(target)  # check action result
        assert all(
            isinstance(item._adapter, MetabaseApi) for item in result
        )  # check adapter set
        assert all(
            item._adapter and isinstance(item._adapter.server_version, Version)
            for item in result
        )  # check adapter initialized

    def test_get_all(self, api: MetabaseApi):
        result = api.collections.get()
        assert isinstance(result, list)  # check item class
        assert all(
            isinstance(item, CollectionItem) for item in result
        )  # check item class
        assert len(result) >= 1  # check action result
        assert all(
            isinstance(item._adapter, MetabaseApi) for item in result
        )  # check adapter set
        assert all(
            item._adapter and isinstance(item._adapter.server_version, Version)
            for item in result
        )  # check adapter initialized

    def test_search(self, api: MetabaseApi, items: list[CollectionItem]):
        params = [{"name": random.choice(items).name}]
        result = api.collections.search(search_params=params, search_list=items)
        assert isinstance(result, list)  # check item class
        assert all(
            isinstance(result, CollectionItem) for result in result
        )  # check item class
        assert len(result) == len(params)  # check action result
        assert all(
            isinstance(item._adapter, MetabaseApi) for item in result
        )  # check adapter set
        assert all(
            item._adapter and isinstance(item._adapter.server_version, Version)
            for item in result
        )  # check adapter initialized


class TestEndpointMethodsCommonFail:
    def test_create_fail(self, api: MetabaseApi):
        with pytest.raises(MetabaseApiException):
            _ = api.collections.create(name="Test fail")  # type: ignore

    def test_get_fail(self, api: MetabaseApi):
        target = {"id": 1}
        with pytest.raises(TypeError):
            _ = api.collections.get(targets=target)  # type: ignore

    def test_search_fail(self, api: MetabaseApi, items: list[CollectionItem]):
        params = [{"name": random.choice(items).name + "z"}]
        result = api.collections.search(search_params=params, search_list=items)
        assert len(result) == 0


class TestEndpointMethodsUniquePass:
    def test_tree(self, api: MetabaseApi):
        coll_tree = api.collections.get_tree()
        assert isinstance(coll_tree, list)
        assert all(isinstance(coll, dict) for coll in coll_tree)

    def test_flatten_tree(self, api: MetabaseApi):
        collections = api.collections.get_flat_list()
        assert isinstance(collections, list)
        assert all(isinstance(collection, dict) for collection in collections)

    def test_graph(self, api: MetabaseApi):
        graph = api.collections.graph()
        assert isinstance(graph, dict)


class TestEndpointMethodsUniqueFail:
    pass


class TestModelMethodsUniquePass:
    def test_contents(self, items: list[CollectionItem]):
        item = random.choice(items)
        result = item.get_contents()
        assert isinstance(result, list)
        assert all(isinstance(record, dict) for record in result)

    def test_contents_archived(self, items: list[CollectionItem]):
        item = random.choice(items)
        result = item.get_contents(archived=True)
        assert isinstance(result, list)
        assert all(isinstance(record, dict) for record in result)


class TestModelMethodsUniqueFail:
    pass
