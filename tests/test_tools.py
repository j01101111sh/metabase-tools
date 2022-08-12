from datetime import datetime

import pytest

from metabase_tools import MetabaseTools


@pytest.fixture(scope="module")
def tools(host: str, credentials: dict) -> MetabaseTools:
    tools = MetabaseTools(
        metabase_url=host,
        credentials=credentials,
        cache_token=True,
        token_path="./metabase.token",
    )
    return tools


@pytest.fixture(scope="module")
def credentials() -> dict:
    from tests.metabase_details import CREDENTIALS

    return CREDENTIALS


@pytest.fixture(scope="module")
def host() -> str:
    from tests.metabase_details import HOST

    return HOST


def test_auth(tools: MetabaseTools):
    token = tools.get_token()
    assert token is not None


def test_download_native_queries(tools: MetabaseTools):
    file = tools.download_native_queries(save_path="./dev/files/")
    size = file.stat().st_size
    create_time = file.stat().st_ctime
    now = datetime.now().timestamp()
    assert size > 0  # File size greater than 0
    assert create_time - now < 2  # file was created in the last 2 seconds
    file.unlink()  # remove created file


def test_upload_native_queries_dry_run(tools: MetabaseTools):
    pass
    # mapping_path = Path("./dev/files/mapping.json")
    # results = tools.upload_native_queries(mapping_path=mapping_path, dry_run=True)
    # assert isinstance(results, list)
    # assert all(isinstance(result, dict) for result in results)
    # assert all(result["is_success"] for result in results)
