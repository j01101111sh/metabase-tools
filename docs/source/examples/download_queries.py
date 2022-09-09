import metabase_tools as mt

host = ""
credentials = {}

tools = mt.MetabaseTools(
    metabase_url=host,
    credentials=credentials,
    cache_token=True,
    token_path=".",
)

mapping_file = tools.download_native_queries(root_folder="./temp/")
