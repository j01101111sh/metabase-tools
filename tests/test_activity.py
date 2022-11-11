import random
from types import LambdaType

import pytest
from packaging.version import Version

from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.activity_model import ActivityItem


@pytest.fixture(scope="module")
def items(api: MetabaseApi) -> list[ActivityItem]:
    return [item for item in api.activity.get()]


class TestModelMethodsCommonPass:
    pass


class TestModelMethodsCommonFail:
    pass


class TestEndpointMethodsCommonPass:
    def test_get(self, api: MetabaseApi):
        result = api.activity.get()
        assert isinstance(result, list)  # check item class
        assert all(
            isinstance(item, ActivityItem) for item in result
        )  # check item class
        assert len(result) >= 1  # check action result
        assert all(
            isinstance(item._adapter, MetabaseApi) for item in result
        )  # check adapter set
        assert all(
            item._adapter and isinstance(item._adapter.server_version, Version)
            for item in result
        )  # check adapter initialized

    def test_search(self, api: MetabaseApi):
        result = api.activity.search({"database_id": 1})
        assert isinstance(result, list)  # check item class
        assert all(
            isinstance(item, ActivityItem) for item in result
        )  # check item class
        assert len(result) >= 1  # check action result


class TestEndpointMethodsCommonFail:
    pass


class TestEndpointMethodsUniquePass:
    pass


class TestEndpointMethodsUniqueFail:
    pass


class TestModelMethodsUniquePass:
    pass


class TestModelMethodsUniqueFail:
    pass
