from datetime import datetime
from pathlib import Path
from random import choice
from string import ascii_lowercase

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
    folder_timestamp = datetime.now().strftime("%y%m%dT%H%M%S")
    file = tools.download_native_queries(root_folder=f"./temp/data{folder_timestamp}")
    size = file.stat().st_size
    create_time = file.stat().st_ctime
    now = datetime.now().timestamp()
    assert size > 0  # File size greater than 0
    assert create_time - now < 2  # file was created in the last 2 seconds


def test_upload_native_queries(tools: MetabaseTools):
    mapping_path = Path("./tests/data/mapping.json")
    test_card_path = Path("./tests/data/Development/Accounting/Test Card.sql")
    with open(test_card_path, "r", newline="", encoding="utf-8") as file:
        current = file.read()
    with open(test_card_path, "a", newline="", encoding="utf-8") as file:
        file.write("\n-- " + "".join(choice(ascii_lowercase) for _ in range(6)))
    results = tools.upload_native_queries(
        mapping_path=mapping_path, dry_run=False, stop_on_error=True
    )
    with open(test_card_path, "w", newline="", encoding="utf-8") as file:
        file.write(current)
    assert isinstance(results, list)
    assert all(isinstance(result, dict) for result in results)
    assert all(result["is_success"] for result in results)
