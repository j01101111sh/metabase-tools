import metabase_tools

metabase_url = "http://localhost:3000"
token_path = "./metabase.token"
api = metabase_tools.MetabaseApi(metabase_url=metabase_url, token_path=token_path)
