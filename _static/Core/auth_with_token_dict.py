import metabase_tools

metabase_url = "http://localhost:3000"
credentials = {"token": "6117922c-541b-4f58-815e-637c6f362920"}
api = metabase_tools.MetabaseApi(metabase_url=metabase_url, credentials=credentials)
