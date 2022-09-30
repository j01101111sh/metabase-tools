import random

import pytest
from packaging.version import Version

from metabase_tools.exceptions import InvalidParameters, RequestFailure
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.database_model import DatabaseItem
from tests.helpers import random_string


@pytest.fixture(scope="module")
def items(api: MetabaseApi) -> list[DatabaseItem]:
    return [item for item in api.databases.get() if item.id != 1]


class TestModelMethodsCommonPass:
    def test_update(self, items: list[DatabaseItem], run_id: str):
        target = random.choice(items)
        result = target.update(description=f"Updated {run_id}")
        assert isinstance(result, DatabaseItem)  # check item class
        assert result.description == f"Updated {run_id}"  # check action result
        assert target.id == result.id  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_archive(self, items: list[DatabaseItem]):
        target = random.choice(items)
        result = target.archive()
        assert isinstance(result, DatabaseItem)  # check item class
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_unarchive(self, items: list[DatabaseItem]):
        target = random.choice(items)
        result = target.unarchive()
        assert isinstance(result, DatabaseItem)  # check item class
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_refresh(self, items: list[DatabaseItem]):
        target = random.choice(items)
        result = target.update(description="Updated " + random_string(5))
        target = target.refresh()
        assert isinstance(target, DatabaseItem)  # check item class
        assert target.description == result.description  # check action result
        assert isinstance(target._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            target._adapter.server_version, Version
        )  # check adapter initialized

    def test_database_delete(
        self, api: MetabaseApi, server_version: Version, items: list[DatabaseItem]
    ):
        target = random.choice(items)
        target.delete()
        new_db = {
            "name": "Test DB",
            "engine": "h2",
            "details": {
                "db": "zip:/app/metabase.jar!/sample-dataset.db;USER=GUEST;PASSWORD=guest"
            },
        }
        if server_version >= Version("v0.42"):
            new_db["details"]["db"] = new_db["details"]["db"].replace(
                "sample-dataset", "sample-database"
            )
        created_db = api.databases.create(**new_db)
        assert isinstance(created_db, DatabaseItem)


class TestModelMethodsCommonFail:
    def test_update_fail(self, items: list[DatabaseItem]):
        target = random.choice(items)
        with pytest.raises(RequestFailure):
            _ = target.update(engine=3)  # type: ignore

    def test_archive_fail(self, api: MetabaseApi):
        target = api.databases.get()[0]
        target.id = -1
        with pytest.raises(RequestFailure):
            _ = target.archive()  # type: ignore

    def test_unarchive_fail(self, api: MetabaseApi):
        target = api.databases.get()[0]
        target.id = -1
        with pytest.raises(RequestFailure):
            _ = target.unarchive()  # type: ignore


class TestEndpointMethodsCommonPass:
    def test_create(self, api: MetabaseApi, server_version: Version):
        name = "Test - " + random_string(6, True)
        definition = {
            "name": name,
            "engine": "h2",
            "details": {
                "db": "zip:/app/metabase.jar!/sample-dataset.db;USER=GUEST;PASSWORD=guest"
            },
        }
        if server_version >= Version("v0.42"):
            definition["details"]["db"] = definition["details"]["db"].replace(
                "sample-dataset", "sample-database"
            )
        result = api.databases.create(**definition)
        assert isinstance(result, DatabaseItem)  # check item class
        assert result.name == name  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter is initialized correctly

    def test_get_one(self, api: MetabaseApi, items: list[DatabaseItem]):
        item_ids = [item.id for item in items if isinstance(item.id, int)]
        target = random.sample(item_ids, 1)
        result = api.databases.get(targets=target)
        assert isinstance(result, list)  # check item class
        assert all(
            isinstance(item, DatabaseItem) for item in result
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

    def test_get_many(self, api: MetabaseApi, items: list[DatabaseItem]):
        item_ids = [item.id for item in items if isinstance(item.id, int)]
        target = random.sample(item_ids, 2)
        result = api.databases.get(targets=target)
        assert isinstance(result, list)  # check item class
        assert all(
            isinstance(item, DatabaseItem) for item in result
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
        result = api.databases.get()
        assert isinstance(result, list)  # check item class
        assert all(
            isinstance(item, DatabaseItem) for item in result
        )  # check item class
        assert len(result) >= 1  # check action result
        assert all(
            isinstance(item._adapter, MetabaseApi) for item in result
        )  # check adapter set
        assert all(
            item._adapter and isinstance(item._adapter.server_version, Version)
            for item in result
        )  # check adapter initialized

    def test_search(self, api: MetabaseApi, items: list[DatabaseItem]):
        params = [{"name": random.choice(items).name}]
        result = api.databases.search(search_params=params, search_list=items)
        assert isinstance(result, list)  # check item class
        assert all(
            isinstance(result, DatabaseItem) for result in result
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
        with pytest.raises(InvalidParameters):
            _ = api.databases.create(name="Test fail")  # type: ignore

    def test_get_fail(self, api: MetabaseApi):
        target = {"id": 1}
        with pytest.raises(InvalidParameters):
            _ = api.databases.get(targets=target)  # type: ignore

    def test_search_fail(self, api: MetabaseApi, items: list[DatabaseItem]):
        params = [{"name": random.choice(items).name + "z"}]
        result = api.databases.search(search_params=params, search_list=items)
        assert len(result) == 0


class TestEndpointMethodsUniquePass:
    pass


class TestEndpointMethodsUniqueFail:
    pass


class TestModelMethodsUniquePass:
    pass


class TestModelMethodsUniqueFail:
    pass
