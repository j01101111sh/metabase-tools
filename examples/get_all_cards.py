import metabase_tools as mt
from tests import helpers

api = mt.MetabaseApi(
    metabase_url=helpers.HOST,
    credentials=helpers.CREDENTIALS,
    cache_token=True,
)

card_1 = api.cards.get()
