import metabase_tools

metabase_url = "http://localhost:3000"
credentials = {"username": "jim@dundermifflin.com", "password": "BAZouVa3saWgW89z"}
api = metabase_tools.MetabaseApi(metabase_url=metabase_url, credentials=credentials)
