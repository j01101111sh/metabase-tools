import pytest

from metabase_tools.exceptions import InvalidParameters, RequestFailure
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.card_model import (
    CardItem,
    CardQueryResult,
    CardRelatedObjects,
)
from tests.conftest import server_version
from tests.helpers import random_string


@pytest.fixture(scope="module")
def cards(api: MetabaseApi) -> list[CardItem]:
    return api.cards.get()


@pytest.fixture(scope="module")
def new_card_def():
    new_card_def = {
        "visualization_settings": {
            "table.pivot_column": "QUANTITY",
            "table.cell_column": "ID",
        },
        "collection_id": 2,
        "name": "",
        "dataset_query": {
            "type": "native",
            "native": {
                "query": "--This card was created through the API\nSELECT ID, USER_ID, PRODUCT_ID, SUBTOTAL, TAX, TOTAL, DISCOUNT, CREATED_AT, QUANTITY\r\nFROM ORDERS\r\nLIMIT 100"
            },
            "database": 1,
        },
        "display": "table",
    }
    return new_card_def


def test_card_create_one(api: MetabaseApi, new_card_def: dict):
    card_one = new_card_def.copy()
    card_one["name"] = "Test Card - " + random_string(6, True)
    new_card_obj = api.cards.create(**card_one)
    assert isinstance(new_card_obj, CardItem)
    assert new_card_obj._adapter is not None


def test_card_update_one(cards: list[CardItem], run_id: str):
    item = cards[0]
    new_item = item.update(description=f"Updated {run_id}")
    assert isinstance(new_item, CardItem)
    assert new_item.description == f"Updated {run_id}"
    assert item._adapter is not None
    assert new_item._adapter is not None


def test_card_update_many(cards: list[CardItem], run_id: str):
    cards_to_update = cards[:2]
    change_result = [
        card.update(description=f"Updated {run_id}") for card in cards_to_update
    ]
    assert isinstance(change_result, list)
    assert all(isinstance(card, CardItem) for card in change_result)
    assert all(card.description == f"Updated {run_id}" for card in change_result)
    assert all(card._adapter is not None for card in change_result)


def test_card_archive_one(cards: list[CardItem]):
    card = cards[0]
    change_result = card.archive()
    assert isinstance(change_result, CardItem)
    assert change_result.archived is True
    assert change_result._adapter is not None


def test_card_archive_many(cards: list[CardItem]):
    items = cards[:2]
    change_result = [item.archive() for item in items]
    assert isinstance(change_result, list)
    assert all(isinstance(card, CardItem) for card in change_result)
    assert all(card.archived is True for card in change_result)
    assert all(card._adapter is not None for card in change_result)


def test_card_unarchive_one(cards: list[CardItem]):
    card = cards[0]
    change_result = card.unarchive()
    assert isinstance(change_result, CardItem)
    assert change_result.archived is False
    assert change_result._adapter is not None


def test_card_unarchive_many(cards: list[CardItem]):
    items = cards[:2]
    change_result = [item.unarchive() for item in items]
    assert isinstance(change_result, list)
    assert all(isinstance(card, CardItem) for card in change_result)
    assert all(card.archived is False for card in change_result)
    assert all(card._adapter is not None for card in change_result)


def test_card_get_one(api: MetabaseApi):
    card_to_get = [1]
    items = api.cards.get(targets=card_to_get)
    assert isinstance(items, list)
    assert all(isinstance(c, CardItem) for c in items)
    assert all(card._adapter is not None for card in items)


def test_card_get_many(api: MetabaseApi):
    cards_to_get = [1, 2]
    items = api.cards.get(targets=cards_to_get)
    assert isinstance(items, list)
    assert all(isinstance(card, CardItem) for card in items)
    assert all(card._adapter is not None for card in items)


def test_card_get_all(api: MetabaseApi):
    items = api.cards.get()
    assert isinstance(items, list)
    assert all(isinstance(card, CardItem) for card in items)
    assert all(card._adapter is not None for card in items)


def test_card_related_one(cards: list[CardItem]):
    card = cards[0]
    related = card.related()
    assert isinstance(related, CardRelatedObjects)


def test_card_related_many(cards: list[CardItem]):
    items = cards[:2]
    related = [card.related() for card in items]
    assert isinstance(related, list)
    assert len(related) == len(items)
    assert all(isinstance(item, CardRelatedObjects) for item in related)


def test_card_embeddable(api: MetabaseApi, cards: list[CardItem]):
    _ = api.settings.enable_embedding.update(True)
    card = cards[0]
    _ = card.update(enable_embedding=True)
    embeddable = api.cards.embeddable()
    assert isinstance(embeddable, list)
    assert all(isinstance(card, CardItem) for card in embeddable)
    assert all(card._adapter is not None for card in embeddable)


@pytest.mark.xfail(raises=NotImplementedError)
def test_card_favorite_one(cards: list[CardItem]):
    card_to_favorite = cards[0]
    try:
        _ = card_to_favorite.unfavorite()
    except:
        pass
    finally:
        favorite = card_to_favorite.favorite()
    assert isinstance(favorite, CardItem)


@pytest.mark.xfail(raises=NotImplementedError)
def test_card_favorite_many(cards: list[CardItem]):
    card_to_favorite = cards[:2]
    favorites = []
    for card in card_to_favorite:
        try:
            _ = card.unfavorite()
        except:
            pass
        finally:
            new = card.favorite()
            favorites.append(new)
    assert isinstance(favorites, list)
    assert all(isinstance(card, CardItem) for card in favorites)


@pytest.mark.xfail(raises=NotImplementedError)
def test_card_unfavorite_one(cards: list[CardItem]):
    card_to_unfavorite = cards[0]
    try:
        _ = card_to_unfavorite.favorite()
    except:
        pass
    finally:
        favorite = card_to_unfavorite.unfavorite()
    assert isinstance(favorite, CardItem)


@pytest.mark.xfail(raises=NotImplementedError)
def test_card_unfavorite_many(cards: list[CardItem]):
    card_to_unfavorite = cards[:2]
    unfavorites = []
    for card in card_to_unfavorite:
        try:
            _ = card.unfavorite()
        except:
            pass
        finally:
            new = card.favorite()
            unfavorites.append(new)
    assert isinstance(unfavorites, list)
    assert all(isinstance(card, CardItem) for card in unfavorites)


def test_card_share_one(api: MetabaseApi, cards: list[CardItem]):
    _ = api.settings.enable_public_sharing.update(True)
    card = cards[0]
    shared = card.share()
    assert isinstance(shared, CardItem)
    unshared = card.unshare()
    assert isinstance(unshared, CardItem)


def test_card_invalid_get(api: MetabaseApi):
    targets = {}
    with pytest.raises(InvalidParameters):
        _ = api.cards.get(targets=targets)  # type: ignore


def test_card_invalid_create(api: MetabaseApi):
    with pytest.raises(InvalidParameters):
        _ = api.cards.create(name="Test fail")  # type: ignore


def test_card_invalid_delete(cards: list[CardItem]):
    card = cards[0]
    with pytest.raises(NotImplementedError):
        _ = card.delete()  # type: ignore


def test_card_invalid_archive(api: MetabaseApi):
    card = api.cards.get()[0]
    card.id = -1
    with pytest.raises(RequestFailure):
        _ = card.archive()  # type: ignore


def test_card_query_one(cards: list[CardItem]):
    card = cards[0]
    results = card.query()
    assert isinstance(results, CardQueryResult)


def test_card_search(api: MetabaseApi, cards: list[CardItem]):
    params = [{"name": "Accounting"}]
    results = api.cards.search(search_params=params, search_list=cards)
    assert len(results) == len(params)
    assert isinstance(results, list)
    assert all(isinstance(result, CardItem) for result in results)
    assert all(card._adapter is not None for card in results)
