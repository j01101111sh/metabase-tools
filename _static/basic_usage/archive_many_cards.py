import metabase_tools

metabase_url = "http://localhost:3000"
credentials = {"username": "jim@dundermifflin.com", "password": "BAZouVa3saWgW89z"}
api = metabase_tools.MetabaseApi(metabase_url=metabase_url, credentials=credentials)

targets = [1, 2, 3]  # IDs of the cards to fetch
cards = api.cards.get()
archived_cards = [card.archive() for card in cards]
