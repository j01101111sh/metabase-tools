import pytest

from metabase_tools import Card, MetabaseApi
from tests.helpers import random_string


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
    new_card_obj = Card.create(adapter=api, payloads=[card_one])
    assert isinstance(new_card_obj, list)
    assert all(isinstance(card, Card) for card in new_card_obj)


def test_card_create_many(api: MetabaseApi, new_card_def: dict):
    card_one = new_card_def.copy()
    card_one["name"] = "Test Card - " + random_string(6, True)
    card_two = new_card_def.copy()
    card_two["name"] = "Test Card - " + random_string(6, True)
    new_cards = [card_one, card_two]
    new_card_objs = Card.create(adapter=api, payloads=new_cards)
    assert isinstance(new_card_objs, list)
    assert all(isinstance(card, Card) for card in new_card_objs)


def test_card_update_one(api: MetabaseApi, run_id: str):
    card_change = {"id": 1, "description": f"Updated {run_id}"}
    change_result = Card.update(adapter=api, payloads=[card_change])
    assert isinstance(change_result, list)
    assert all(isinstance(card, Card) for card in change_result)
    assert all(card.description == f"Updated {run_id}" for card in change_result)


def test_card_update_many(api: MetabaseApi, run_id: str):
    card_changes = {"id": 1, "description": f"Updated {run_id}"}
    cards = Card.get(adapter=api)
    cards_to_update = [card.id for card in cards][:2]
    updates = []
    for card in cards_to_update:
        new_card = card_changes.copy()
        new_card.update(id=card)
        updates.append(new_card)
    change_result = Card.update(adapter=api, payloads=updates)
    assert isinstance(change_result, list)
    assert all(isinstance(card, Card) for card in change_result)
    assert all(card.description == f"Updated {run_id}" for card in change_result)


def test_card_archive_one(api: MetabaseApi):
    card_to_archive = [1]
    change_result = Card.archive(adapter=api, targets=card_to_archive)
    assert isinstance(change_result, list)
    assert all(isinstance(card, Card) for card in change_result)
    assert all(card.archived is True for card in change_result)


def test_card_archive_many(api: MetabaseApi):
    cards = Card.get(adapter=api)
    cards_to_archive = [card.id for card in cards][:2]
    change_results = Card.archive(adapter=api, targets=cards_to_archive)
    assert isinstance(change_results, list)
    assert all(isinstance(cr, Card) for cr in change_results)
    assert all(cr.archived for cr in change_results)


def test_card_unarchive_one(api: MetabaseApi):
    card_to_archive = [1]
    change_result = Card.archive(adapter=api, targets=card_to_archive, unarchive=True)
    assert isinstance(change_result, list)
    assert all(isinstance(card, Card) for card in change_result)
    assert all(card.archived is False for card in change_result)


def test_card_unarchive_many(api: MetabaseApi):
    cards = Card.get(adapter=api)
    cards_to_unarchive = [card.id for card in cards][:2]
    change_results = Card.archive(
        adapter=api, targets=cards_to_unarchive, unarchive=True
    )
    assert isinstance(change_results, list)
    assert all(isinstance(cr, Card) for cr in change_results)
    assert all(not cr.archived for cr in change_results)


def test_card_get_one(api: MetabaseApi):
    card_to_get = [1]
    card = Card.get(adapter=api, targets=card_to_get)
    assert isinstance(card, list)
    assert all(isinstance(c, Card) for c in card)


def test_card_get_many(api: MetabaseApi):
    cards_to_get = [1, 1]
    cards = Card.get(adapter=api, targets=cards_to_get)
    assert isinstance(cards, list)
    assert all(isinstance(card, Card) for card in cards)


def test_card_get_all(api: MetabaseApi):
    cards = Card.get(adapter=api)
    assert isinstance(cards, list)
    assert all(isinstance(card, Card) for card in cards)


def test_card_related_one(api: MetabaseApi):
    related = Card.related(adapter=api, targets=[1])
    assert isinstance(related, list)
    assert len(related) == 1
    assert all(isinstance(item, dict) for item in related)


def test_card_related_many(api: MetabaseApi):
    related = Card.related(adapter=api, targets=[1, 2])
    assert isinstance(related, list)
    assert len(related) == 2
    assert all(isinstance(item, dict) for item in related)


@pytest.mark.skip(reason="Not implemented in test environment")
def test_card_embeddable(api: MetabaseApi):
    embeddable = Card.embeddable(adapter=api)
    assert isinstance(embeddable, list)
    assert all(isinstance(card, Card) for card in embeddable)


def test_card_favorite_one(api: MetabaseApi):
    card_to_favorite = [1]
    favorite = Card.favorite(adapter=api, targets=card_to_favorite)
    assert isinstance(favorite, list)
    assert all(isinstance(result, dict) for result in favorite)
    assert len(card_to_favorite) == len(favorite)


def test_card_favorite_many(api: MetabaseApi):
    cards_to_favorite = [1, 2]
    favorites = Card.favorite(adapter=api, targets=cards_to_favorite)
    assert isinstance(favorites, list)
    assert all(isinstance(result, dict) for result in favorites)
    assert len(cards_to_favorite) == len(favorites)


def test_card_unfavorite_one(api: MetabaseApi):
    card_to_unfavorite = [1]
    unfavorite = Card.unfavorite(adapter=api, targets=card_to_unfavorite)
    assert isinstance(unfavorite, list)
    assert all(isinstance(result, dict) for result in unfavorite)
    assert len(card_to_unfavorite) == len(unfavorite)


def test_card_unfavorite_many(api: MetabaseApi):
    cards_to_unfavorite = [1, 2]
    unfavorites = Card.unfavorite(adapter=api, targets=cards_to_unfavorite)
    assert isinstance(unfavorites, list)
    assert all(isinstance(result, dict) for result in unfavorites)
    assert len(cards_to_unfavorite) == len(unfavorites)


@pytest.mark.skip(reason="Not implemented in test environment")
def test_card_share_one(api: MetabaseApi):
    card_to_share = [1]
    shared = Card.share(adapter=api, targets=card_to_share)
    assert isinstance(shared, list)
    assert all(isinstance(result, dict) for result in shared)
    assert len(card_to_share) == len(shared)


@pytest.mark.skip(reason="Not implemented in test environment")
def test_card_unshare_one(api: MetabaseApi):
    card_to_unshare = [1]
    unshared = Card.unshare(adapter=api, targets=card_to_unshare)
    assert isinstance(unshared, list)
    assert all(isinstance(result, dict) for result in unshared)
    assert len(card_to_unshare) == len(unshared)
