import random

import pytest
from packaging.version import Version

from metabase_tools.exceptions import InvalidParameters, RequestFailure
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.user_model import UserItem
from tests.helpers import PASSWORD, random_string


@pytest.fixture(scope="function")
def items(api: MetabaseApi) -> list[UserItem]:
    return [item for item in api.users.get() if item.id != 1]


class TestModelMethodsCommonPass:
    def test_update(self, items: list[UserItem], run_id: str):
        target = random.choice(items)
        result = target.update(first_name=run_id)
        assert isinstance(result, UserItem)  # check item class
        assert result.first_name == run_id  # check action result
        assert target.id == result.id  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_archive(self, items: list[UserItem]):
        target = random.choice(items)
        result = target.archive()
        assert isinstance(result, UserItem)  # check item class
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_unarchive(self, items: list[UserItem]):
        target = random.choice(items)
        result = target.unarchive()
        assert isinstance(result, UserItem)  # check item class
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_refresh(self, items: list[UserItem]):
        target = random.choice(items)
        result = target.update(first_name=random_string(5))
        target = target.refresh()
        assert isinstance(target, UserItem)  # check item class
        assert target.first_name == result.first_name  # check action result
        assert isinstance(target._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            target._adapter.server_version, Version
        )  # check adapter initialized

    def test_disable(self, api: MetabaseApi, items: list[UserItem]):
        target = random.choice(items)
        target.disable()
        with pytest.raises(RequestFailure):
            _ = api.users.get(targets=[target.id if isinstance(target.id, int) else 2])


class TestModelMethodsCommonFail:
    def test_update_fail(self, items: list[UserItem]):
        target = random.choice(items)
        with pytest.raises(RequestFailure):
            _ = target.update(email="four")  # type: ignore

    def test_archive_fail(self, api: MetabaseApi):
        target = api.users.get()[0]
        target.id = -1
        with pytest.raises(RequestFailure):
            _ = target.archive()  # type: ignore

    def test_unarchive_fail(self, api: MetabaseApi):
        target = api.users.get()[0]
        target.id = -1
        with pytest.raises(RequestFailure):
            _ = target.unarchive()  # type: ignore


class TestEndpointMethodsCommonPass:
    def test_create(self, api: MetabaseApi, server_version: Version):
        name = random_string(6, True)
        definition = {
            "first_name": name,
            "last_name": "Test",
            "email": f"{name}@DunderMifflin.com",
            "password": random_string(20),
        }
        result = api.users.create(**definition)
        assert isinstance(result, UserItem)  # check item class
        assert result.first_name == name  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter is initialized correctly

    def test_get_one(self, api: MetabaseApi, items: list[UserItem]):
        item_ids = [item.id for item in items if isinstance(item.id, int)]
        target = random.sample(item_ids, 1)
        result = api.users.get(targets=target)
        assert isinstance(result, list)  # check item class
        assert all(isinstance(item, UserItem) for item in result)  # check item class
        assert all(item.id in target for item in result)  # check action result
        assert len(result) == len(target)  # check action result
        assert all(
            isinstance(item._adapter, MetabaseApi) for item in result
        )  # check adapter set
        assert all(
            item._adapter and isinstance(item._adapter.server_version, Version)
            for item in result
        )  # check adapter initialized

    def test_get_many(self, api: MetabaseApi, items: list[UserItem]):
        item_ids = [item.id for item in items if isinstance(item.id, int)]
        target = random.sample(item_ids, 2)
        result = api.users.get(targets=target)
        assert isinstance(result, list)  # check item class
        assert all(isinstance(item, UserItem) for item in result)  # check item class
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
        result = api.users.get()
        assert isinstance(result, list)  # check item class
        assert all(isinstance(item, UserItem) for item in result)  # check item class
        assert len(result) >= 1  # check action result
        assert all(
            isinstance(item._adapter, MetabaseApi) for item in result
        )  # check adapter set
        assert all(
            item._adapter and isinstance(item._adapter.server_version, Version)
            for item in result
        )  # check adapter initialized

    def test_search(self, api: MetabaseApi, items: list[UserItem]):
        params = [{"name": random.choice(items).name}]
        result = api.users.search(search_params=params, search_list=items)
        assert isinstance(result, list)  # check item class
        assert all(
            isinstance(result, UserItem) for result in result
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
            _ = api.users.create(name="Test fail")  # type: ignore

    def test_get_fail(self, api: MetabaseApi):
        target = {"id": 1}
        with pytest.raises(InvalidParameters):
            _ = api.users.get(targets=target)  # type: ignore

    def test_search_fail(self, api: MetabaseApi, items: list[UserItem]):
        params = [{"name": random.choice(items).name + "z"}]
        result = api.users.search(search_params=params, search_list=items)
        assert len(result) == 0


class TestEndpointMethodsUniquePass:
    def test_user_current(self, api: MetabaseApi):
        user = api.users.current()
        assert isinstance(user, UserItem)


class TestEndpointMethodsUniqueFail:
    pass


class TestModelMethodsUniquePass:
    def test_user_resend(self, items: list[UserItem]):
        item = random.choice(items)
        result = item.resend_invite()
        assert isinstance(result, dict)
        assert result["success"] is True

    def test_user_reset_password(self, items: list[UserItem]):
        item = random.choice(items)
        payload = {"id": item.id, "password": PASSWORD}
        result = item.update_password(payload=payload)
        assert isinstance(result, UserItem)

    @pytest.mark.xfail(raises=NotImplementedError)
    def test_user_qbnewb(self, items: list[UserItem]):
        item = random.choice(items)
        result = item.qbnewb()
        assert isinstance(result, dict)
        assert result["success"] is True


class TestModelMethodsUniqueFail:
    pass
