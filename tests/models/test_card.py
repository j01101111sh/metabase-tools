from datetime import datetime

import pytest
from metabase_tools import Card, MetabaseApi


@pytest.fixture(scope='module')
def api(host, credentials):
    return MetabaseApi(metabase_url=host, credentials=credentials, cache_token=True, token_path='./metabase.token')


@pytest.fixture(scope='module')
def credentials():
    from tests.metabase_details import CREDENTIALS
    return CREDENTIALS


@pytest.fixture(scope='module')
def host():
    from tests.metabase_details import HOST
    return HOST


@pytest.fixture(scope='module')
def new_card_def():
    new_card_def = {
        'visualization_settings': {
            'table.pivot_column': 'QUANTITY',
            'table.cell_column': 'ID'
        },
        'collection_id': 2,
        'name': 'Test Card',
        'dataset_query': {
            'type': 'native',
            'native': {
                'query': '--This card was created through the API\nSELECT ID, USER_ID, PRODUCT_ID, SUBTOTAL, TAX, TOTAL, DISCOUNT, CREATED_AT, QUANTITY\r\nFROM ORDERS\r\nLIMIT 100'
            },
            'database': 1
        },
        'display': 'table'
    }
    return new_card_def


def test_card_create_one(api: MetabaseApi, new_card_def: dict):
    new_card_obj = Card.post(adapter=api, payloads=new_card_def)
    assert isinstance(new_card_obj, list)
    assert all(isinstance(card, Card) for card in new_card_obj)


def test_card_create_many(api: MetabaseApi, new_card_def: dict):
    new_cards = [new_card_def, new_card_def]
    new_card_objs = Card.post(adapter=api, payloads=new_cards)
    assert isinstance(new_card_objs, list)
    assert all(isinstance(card, Card) for card in new_card_objs)


def test_card_update_one(api: MetabaseApi):
    dt = datetime.now().isoformat(timespec='seconds')
    card_changes = {
        'id': 1,
        'description': f'Updated {dt}'
    }
    change_result = Card.put(adapter=api, payloads=card_changes)
    assert isinstance(change_result, list)
    assert all(isinstance(card, Card) for card in change_result)
    assert all(card.description == f'Updated {dt}' for card in change_result)


def test_card_update_many(api: MetabaseApi):
    dt = datetime.now().isoformat(timespec='seconds')
    card_changes = {
        'id': 1,
        'description': f'Updated {dt}'
    }
    cards = Card.get(adapter=api)
    cards_to_update = [card.id for card in cards][:2]
    updates = []
    for card in cards_to_update:
        new_card = card_changes.copy()
        new_card.update(id=card)
        updates.append(new_card)
    change_result = Card.put(adapter=api, payloads=card_changes)
    assert isinstance(change_result, list)
    assert all(isinstance(card, Card) for card in change_result)
    assert all(card.description == f'Updated {dt}' for card in change_result)


def test_card_archive_one(api: MetabaseApi):
    card_to_archive = 1
    change_result = Card.archive(adapter=api, targets=card_to_archive)
    assert isinstance(change_result, list)
    assert all(isinstance(card, Card) for card in change_result)
    assert all(card.archived == True for card in change_result)


def test_card_archive_many(api: MetabaseApi):
    cards = Card.get(adapter=api)
    cards_to_archive = [card.id for card in cards][:2]
    change_results = Card.archive(adapter=api, targets=cards_to_archive)
    assert isinstance(change_results, list)
    assert all(isinstance(cr, Card) for cr in change_results)
    assert all(cr.archived for cr in change_results)


def test_card_unarchive_one(api: MetabaseApi):
    card_to_archive = 1
    change_result = Card.archive(
        adapter=api, targets=card_to_archive, unarchive=True)
    assert isinstance(change_result, list)
    assert all(isinstance(card, Card) for card in change_result)
    assert all(card.archived == False for card in change_result)


def test_card_unarchive_many(api: MetabaseApi):
    cards = Card.get(adapter=api)
    cards_to_unarchive = [card.id for card in cards][:2]
    change_results = Card.archive(
        adapter=api, targets=cards_to_unarchive, unarchive=True)
    assert isinstance(change_results, list)
    assert all(isinstance(cr, Card) for cr in change_results)
    assert all(not cr.archived for cr in change_results)


def test_card_get_one(api: MetabaseApi):
    # TODO
    pass


def test_card_get_many(api: MetabaseApi):
    # TODO
    pass


def test_card_get_all(api: MetabaseApi):
    cards = Card.get(adapter=api)
    assert isinstance(cards, list)
    assert all(isinstance(card, Card) for card in cards)
