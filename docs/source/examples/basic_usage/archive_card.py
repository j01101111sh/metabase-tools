import metabase_tools

metabase_url = "http://localhost:3000"
credentials = {"username": "jim@dundermifflin.com", "password": "BAZouVa3saWgW89z"}
api = metabase_tools.MetabaseApi(metabase_url=metabase_url, credentials=credentials)

targets = [1]  # ID of the card to fetch
card = api.cards.get()[0]  # Return list so [0] will extract the item from that list
archived_card = card.archive()  # Returns CardItem
