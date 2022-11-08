import random
from types import LambdaType

import pytest
from packaging.version import Version

from metabase_tools.exceptions import MetabaseApiException
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.alert_model import AlertItem


@pytest.fixture(scope="module")
def items(api: MetabaseApi) -> list[AlertItem]:
    return [item for item in api.alerts.get()]


class TestModelMethodsCommonPass:
    def test_update(self, items: list[AlertItem], run_id: str):
        target = random.choice(items)
        result = target.update(
            card={
                "id": target.card["id"],
                "include_csv": True,
                "include_xls": True,
                "dashboard_card_id": None,
            }
        )
        assert isinstance(result, AlertItem)  # check item class
        assert result.card["include_csv"] and result.card["include_xls"]
        assert target.id == result.id  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_archive(self, items: list[AlertItem]):
        target = random.choice(items)
        result = target.archive()
        _ = target.unarchive()
        assert isinstance(result, AlertItem)  # check item class
        assert result.archived is True  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_unarchive(self, items: list[AlertItem]):
        target = random.choice(items)
        result = target.unarchive()
        assert isinstance(result, AlertItem)  # check item class
        assert result.archived is False  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_refresh(self, items: list[AlertItem], random_string: LambdaType):
        target = random.choice(items)
        result = target.update(name="Updated " + random_string(5))
        target = target.refresh()
        assert isinstance(target, AlertItem)  # check item class
        assert target.name == result.name  # check action result
        assert isinstance(target._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            target._adapter.server_version, Version
        )  # check adapter initialized


class TestModelMethodsCommonFail:
    def test_update_fail(self, items: list[AlertItem]):
        target = random.choice(items)
        with pytest.raises(MetabaseApiException):
            _ = target.update(card=1)  # type: ignore

    def test_archive_fail(self, api: MetabaseApi):
        target = api.alerts.get()[0]
        target.id = -1
        with pytest.raises(MetabaseApiException):
            _ = target.archive()  # type: ignore

    def test_unarchive_fail(self, api: MetabaseApi):
        target = api.alerts.get()[0]
        target.id = -1
        with pytest.raises(MetabaseApiException):
            _ = target.unarchive()  # type: ignore

    def test_delete_fail(self, items: list[AlertItem]):
        target = random.choice(items)
        with pytest.raises(NotImplementedError):
            _ = target.delete()  # type: ignore


class TestEndpointMethodsCommonPass:
    def test_create(self, api: MetabaseApi, random_string: LambdaType):
        definition = {
            "alert_condition": "rows",
            "card": {
                "id": 1,
                "include_csv": True,
                "include_xls": False,
                "dashboard_card_id": None,
            },
            "channels": [
                {
                    "schedule_type": "daily",
                    "schedule_hour": 0,
                    "channel_type": "email",
                    "schedule_frame": None,
                    "recipients": [
                        {
                            "id": 1,
                            "email": "jim@dundermifflin.com",
                            "first_name": "Jim",
                            "last_name": "Halpert",
                            "common_name": "Jim Halpert",
                        }
                    ],
                    "pulse_id": 1,
                    "id": 1,
                    "schedule_day": None,
                    "enabled": True,
                }
            ],
            "alert_first_only": False,
            "alert_above_goal": None,
        }
        result = api.alerts.create(**definition)
        assert isinstance(result, AlertItem)  # check item class
        assert result.card["id"] == 1  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter is initialized correctly

    def test_get_one(self, api: MetabaseApi, items: list[AlertItem]):
        item_ids = [item.id for item in items if isinstance(item.id, int)]
        target = random.sample(item_ids, 1)
        result = api.alerts.get(targets=target)
        assert isinstance(result, list)  # check item class
        assert all(isinstance(item, AlertItem) for item in result)  # check item class
        assert all(item.id in target for item in result)  # check action result
        assert len(result) == len(target)  # check action result
        assert all(
            isinstance(item._adapter, MetabaseApi) for item in result
        )  # check adapter set
        assert all(
            item._adapter and isinstance(item._adapter.server_version, Version)
            for item in result
        )  # check adapter initialized

    def test_get_many(self, api: MetabaseApi, items: list[AlertItem]):
        item_ids = [item.id for item in items if isinstance(item.id, int)]
        target = random.sample(item_ids, 2)
        result = api.alerts.get(targets=target)
        assert isinstance(result, list)  # check item class
        assert all(isinstance(item, AlertItem) for item in result)  # check item class
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
        result = api.alerts.get()
        assert isinstance(result, list)  # check item class
        assert all(isinstance(item, AlertItem) for item in result)  # check item class
        assert len(result) >= 1  # check action result
        assert all(
            isinstance(item._adapter, MetabaseApi) for item in result
        )  # check adapter set
        assert all(
            item._adapter and isinstance(item._adapter.server_version, Version)
            for item in result
        )  # check adapter initialized

    def test_search(self, api: MetabaseApi, items: list[AlertItem]):
        params = [{"id": random.choice(items).id}]
        result = api.alerts.search(search_params=params, search_list=items)
        assert isinstance(result, list)  # check item class
        assert all(
            isinstance(result, AlertItem) for result in result
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
            _ = api.alerts.create(name="Test fail")  # type: ignore

    def test_get_fail(self, api: MetabaseApi):
        target = {"id": 1}
        with pytest.raises(TypeError):
            _ = api.alerts.get(targets=target)  # type: ignore

    def test_search_fail(self, api: MetabaseApi, items: list[AlertItem]):
        params = [{"id": -1}]
        result = api.alerts.search(search_params=params, search_list=items)
        assert len(result) == 0


class TestEndpointMethodsUniquePass:
    def test_get_by_card(self, api: MetabaseApi, items: list[AlertItem]):
        card_id = items[0].card["id"]
        result = api.alerts.get_by_card(targets=[card_id])
        assert isinstance(result, list)  # check item class
        assert all(isinstance(item, AlertItem) for item in result)  # check item class
        assert all(
            isinstance(item._adapter, MetabaseApi) for item in result
        )  # check adapter set
        assert all(
            item._adapter and isinstance(item._adapter.server_version, Version)
            for item in result
        )  # check adapter initialized


class TestEndpointMethodsUniqueFail:
    pass


class TestModelMethodsUniquePass:
    pass


class TestModelMethodsUniqueFail:
    pass
