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


def test_card_create_one(api):
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
    new_card_obj = Card.post(adapter=api, payloads=new_card_def)
    assert isinstance(new_card_obj, Card)


def test_card_update_one(api):
    dt = datetime.now().isoformat(timespec='seconds')
    card_changes = {
        'id': 1,
        'description': f'Updated {dt}'
    }
    change_result = Card.put(adapter=api, payloads=card_changes)
    assert isinstance(change_result, Card)


def test_card_list_all(api):
    cards = Card.get(adapter=api)
    assert isinstance(cards, list)
    assert all(isinstance(card, Card) for card in cards)
