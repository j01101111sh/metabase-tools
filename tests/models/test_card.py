import pytest
from metabase_tools import Card, MetabaseApi
from tests.metabase_details import CREDENTIALS, HOST


@pytest.fixture(scope='module')
def api():
    return MetabaseApi(metabase_url=HOST, credentials=CREDENTIALS)


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


def test_card_list_all(api):
    cards = Card.get(adapter=api)
    assert isinstance(cards, list)
    assert all(isinstance(card, Card) for card in cards)
