import metabase_tools

metabase_url = "http://localhost:3000"
credentials = {"username": "jim@dundermifflin.com", "password": "BAZouVa3saWgW89z"}
api = metabase_tools.MetabaseApi(metabase_url=metabase_url, credentials=credentials)

all_cards = api.cards.get()

for card in all_cards:
    print(f"{card.id} - {card.name}")

targets = [1, 2, 3]  # IDs of the card to fetch
some_cards = api.cards.get(targets=targets)

for card in some_cards:
    print(f"{card.id} - {card.name}")
