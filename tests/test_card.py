import random
from types import LambdaType

import pytest
from packaging.version import Version

from metabase_tools.exceptions import MetabaseApiException
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.card_model import (
    CardItem,
    CardQueryResult,
    CardRelatedObjects,
)


@pytest.fixture(scope="module")
def items(api: MetabaseApi) -> list[CardItem]:
    return [item for item in api.cards.get()]


class TestModelMethodsCommonPass:
    def test_update(self, items: list[CardItem], run_id: str):
        target = random.choice(items)
        result = target.update(description=f"Updated {run_id}")
        assert isinstance(result, CardItem)  # check item class
        assert result.description == f"Updated {run_id}"  # check action result
        assert target.id == result.id  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_archive(self, items: list[CardItem]):
        target = random.choice(items)
        result = target.archive()
        _ = target.unarchive()
        assert isinstance(result, CardItem)  # check item class
        assert result.archived is True  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_unarchive(self, items: list[CardItem]):
        target = random.choice(items)
        result = target.unarchive()
        assert isinstance(result, CardItem)  # check item class
        assert result.archived is False  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_refresh(self, items: list[CardItem], random_string: LambdaType):
        target = random.choice(items)
        result = target.update(description="Updated " + random_string(5))
        target = target.refresh()
        assert isinstance(target, CardItem)  # check item class
        assert target.description == result.description  # check action result
        assert isinstance(target._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            target._adapter.server_version, Version
        )  # check adapter initialized


class TestModelMethodsCommonFail:
    def test_update_fail(self, items: list[CardItem]):
        target = random.choice(items)
        with pytest.raises(MetabaseApiException):
            _ = target.update(visualization_settings="invalid")  # type: ignore

    def test_archive_fail(self, api: MetabaseApi):
        target = api.cards.get()[0]
        target.id = -1
        with pytest.raises(MetabaseApiException):
            _ = target.archive()  # type: ignore

    def test_unarchive_fail(self, api: MetabaseApi):
        target = api.cards.get()[0]
        target.id = -1
        with pytest.raises(MetabaseApiException):
            _ = target.unarchive()  # type: ignore

    def test_delete_fail(self, items: list[CardItem]):
        target = random.choice(items)
        with pytest.raises(NotImplementedError):
            _ = target.delete()  # type: ignore


class TestEndpointMethodsCommonPass:
    def test_create(self, api: MetabaseApi, random_string: LambdaType):
        name = "Test Card - " + random_string(6)
        definition = {
            "visualization_settings": {
                "table.pivot_column": "QUANTITY",
                "table.cell_column": "ID",
            },
            "collection_id": 2,
            "name": name,
            "dataset_query": {
                "type": "native",
                "native": {
                    "query": "--This card was created through the API\nSELECT ID, USER_ID, PRODUCT_ID, SUBTOTAL, TAX, TOTAL, DISCOUNT, CREATED_AT, QUANTITY\r\nFROM ORDERS\r\nLIMIT 100\n"
                },
                "database": 1,
            },
            "display": "table",
        }
        result = api.cards.create(**definition)
        assert isinstance(result, CardItem)  # check item class
        assert result.name == name  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert isinstance(
            result._adapter.server_version, Version
        )  # check adapter is initialized correctly

    def test_get_one(self, api: MetabaseApi, items: list[CardItem]):
        item_ids = [item.id for item in items if isinstance(item.id, int)]
        target = random.sample(item_ids, 1)
        result = api.cards.get(targets=target)
        assert isinstance(result, list)  # check item class
        assert all(isinstance(item, CardItem) for item in result)  # check item class
        assert all(item.id in target for item in result)  # check action result
        assert len(result) == len(target)  # check action result
        assert all(
            isinstance(item._adapter, MetabaseApi) for item in result
        )  # check adapter set
        assert all(
            item._adapter and isinstance(item._adapter.server_version, Version)
            for item in result
        )  # check adapter initialized

    def test_get_many(self, api: MetabaseApi, items: list[CardItem]):
        item_ids = [item.id for item in items if isinstance(item.id, int)]
        target = random.sample(item_ids, 2)
        result = api.cards.get(targets=target)
        assert isinstance(result, list)  # check item class
        assert all(isinstance(item, CardItem) for item in result)  # check item class
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
        result = api.cards.get()
        assert isinstance(result, list)  # check item class
        assert all(isinstance(item, CardItem) for item in result)  # check item class
        assert len(result) >= 1  # check action result
        assert all(
            isinstance(item._adapter, MetabaseApi) for item in result
        )  # check adapter set
        assert all(
            item._adapter and isinstance(item._adapter.server_version, Version)
            for item in result
        )  # check adapter initialized

    def test_search(self, api: MetabaseApi, items: list[CardItem]):
        params = [{"name": random.choice(items).name}]
        result = api.cards.search(search_params=params, search_list=items)
        assert isinstance(result, list)  # check item class
        assert all(
            isinstance(result, CardItem) for result in result
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
            _ = api.cards.create(name="Test fail")  # type: ignore

    def test_get_fail(self, api: MetabaseApi):
        target = {"id": 1}
        with pytest.raises(TypeError):
            _ = api.cards.get(targets=target)  # type: ignore

    def test_search_fail(self, api: MetabaseApi, items: list[CardItem]):
        params = [{"name": f"{random.choice(items).name}z"}]
        result = api.cards.search(search_params=params, search_list=items)
        assert len(result) == 0


class TestEndpointMethodsUniquePass:
    def test_embeddable(self, api: MetabaseApi, items: list[CardItem]):
        _ = api.settings.enable_embedding.update(True)  # Ensure embedding is enabled
        target = random.choice(items)
        _ = target.update(enable_embedding=True)  # Ensure at least 1 card has enabled
        result = api.cards.embeddable()
        assert isinstance(result, list)  # check item class
        assert all(isinstance(item, CardItem) for item in result)  # check item class
        assert len(result) >= 1  # check action result
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
    def test_related(self, items: list[CardItem]):
        target = random.choice(items)
        result = target.related()
        assert isinstance(result, CardRelatedObjects)  # check item class

    @pytest.mark.xfail(raises=NotImplementedError)
    def test_favorite(self, items: list[CardItem]):
        target = random.choice(items)
        try:
            _ = target.unfavorite()
        except:
            pass
        finally:
            result = target.favorite()
        assert isinstance(result, CardItem)  # check item class
        assert result.is_favorite  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert result._adapter and isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    @pytest.mark.xfail(raises=NotImplementedError)
    def test_unfavorite(self, items: list[CardItem]):
        target = random.choice(items)
        try:
            _ = target.favorite()
        except:
            pass
        finally:
            result = target.unfavorite()
        assert isinstance(result, CardItem)  # check item class
        assert not result.is_favorite  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert result._adapter and isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_share(self, api: MetabaseApi, items: list[CardItem]):
        _ = api.settings.enable_public_sharing.update(True)  # Ensure sharing is enabled
        target = random.choice(items)
        result = target.share()
        assert isinstance(result, CardItem)  # check item class
        assert result.public_uuid is not None  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert result._adapter and isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_unshare(self, api: MetabaseApi, items: list[CardItem]):
        _ = api.settings.enable_public_sharing.update(True)  # Ensure sharing is enabled
        target = random.choice(items)
        _ = target.share()
        result = target.unshare()
        assert isinstance(result, CardItem)  # check item class
        assert result.public_uuid is None  # check action result
        assert isinstance(result._adapter, MetabaseApi)  # check adapter set
        assert result._adapter and isinstance(
            result._adapter.server_version, Version
        )  # check adapter initialized

    def test_query(self, items: list[CardItem]):
        target = random.choice(items)
        result = target.query()
        assert isinstance(result, CardQueryResult)


class TestModelMethodsUniqueFail:
    @pytest.mark.xfail(raises=NotImplementedError)
    def test_favorite_fail(self, items: list[CardItem]):
        target = random.choice(items)
        with pytest.raises(MetabaseApiException):
            _ = target.favorite()
            result = target.favorite()

    @pytest.mark.xfail(raises=NotImplementedError)
    def test_unfavorite_fail(self, items: list[CardItem]):
        target = random.choice(items)
        with pytest.raises(MetabaseApiException):
            _ = target.unfavorite()
            result = target.unfavorite()
