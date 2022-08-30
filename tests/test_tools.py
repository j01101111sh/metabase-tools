from datetime import datetime
from pathlib import Path
from typing import NoReturn

import pytest
from typing_extensions import assert_never

from metabase_tools import MetabaseTools
from tests.helpers import random_string


@pytest.fixture(scope="module")
def tools(host: str, credentials: dict, result_path, run_id) -> MetabaseTools:
    token_path = f"{result_path}/{run_id}_tools.token"
    tools = MetabaseTools(
        metabase_url=host,
        credentials=credentials,
        cache_token=True,
        token_path=token_path,
    )
    return tools


def test_auth(tools: MetabaseTools):
    assert tools.test_for_auth()


def test_download_native_queries(tools: MetabaseTools, result_path):
    file = tools.download_native_queries(root_folder=f"{result_path}/data/")
    assert file.stat().st_size > 0  # File size greater than 0
    assert (
        file.stat().st_ctime - datetime.now().timestamp() < 2
    )  # file was created in the last 2 seconds


def test_upload(tools: MetabaseTools):
    mapping_path = Path("./tests/data/mapping.json")
    test_card_path = Path("./tests/data/Development/Accounting/Test Card.sql")
    with open(test_card_path, "r", newline="", encoding="utf-8") as file:
        current = file.read()
    with open(test_card_path, "a", newline="", encoding="utf-8") as file:
        file.write("\n-- " + random_string(6))
    try:
        results = tools.upload_native_queries(
            mapping_path=mapping_path,
            file_extension="sql",
            dry_run=False,
            stop_on_error=False,
        )
    except:
        assert_never(NoReturn)
    finally:
        with open(test_card_path, "w", newline="", encoding="utf-8") as file:
            file.write(current)
    assert isinstance(results, list)
    assert all(isinstance(result, dict) for result in results)
    assert all(result["is_success"] for result in results)


def test_upload_dry(tools: MetabaseTools):
    mapping_path = Path("./tests/data/mapping.json")
    test_card_path = Path("./tests/data/Development/Accounting/Test Card.sql")
    with open(test_card_path, "r", newline="", encoding="utf-8") as file:
        current = file.read()
    with open(test_card_path, "a", newline="", encoding="utf-8") as file:
        file.write("\n-- " + random_string(6))
    try:
        results = tools.upload_native_queries(
            mapping_path=mapping_path,
            file_extension="sql",
            dry_run=True,
            stop_on_error=False,
        )
    except:
        assert_never(NoReturn)
    finally:
        with open(test_card_path, "w", newline="", encoding="utf-8") as file:
            file.write(current)
    assert isinstance(results, dict)
    assert "updates" in results and len(results["updates"]) > 0
    assert "creates" in results
    assert "errors" in results and len(results["errors"]) == 0


def test_upload_stop(tools: MetabaseTools):
    mapping_path = Path("./tests/data/mapping.json")
    test_card_path = Path("./tests/data/Development/Accounting/Test Card.sql")
    with open(test_card_path, "r", newline="", encoding="utf-8") as file:
        current = file.read()
    with open(test_card_path, "a", newline="", encoding="utf-8") as file:
        file.write("\n-- " + random_string(6))
    try:
        results = tools.upload_native_queries(
            mapping_path=mapping_path,
            file_extension="sql",
            dry_run=False,
            stop_on_error=True,
        )
    except:
        assert_never(NoReturn)
    finally:
        with open(test_card_path, "w", newline="", encoding="utf-8") as file:
            file.write(current)
    assert isinstance(results, list)
    assert all(isinstance(result, dict) for result in results)
    assert all(result["is_success"] for result in results)


def test_upload_dry_stop(tools: MetabaseTools):
    mapping_path = Path("./tests/data/mapping.json")
    test_card_path = Path("./tests/data/Development/Accounting/Test Card.sql")
    with open(test_card_path, "r", newline="", encoding="utf-8") as file:
        current = file.read()
    with open(test_card_path, "a", newline="", encoding="utf-8") as file:
        file.write("\n-- " + random_string(6))
    try:
        results = tools.upload_native_queries(
            mapping_path=mapping_path,
            file_extension="sql",
            dry_run=True,
            stop_on_error=True,
        )
    except:
        assert_never(NoReturn)
    finally:
        with open(test_card_path, "w", newline="", encoding="utf-8") as file:
            file.write(current)
    assert isinstance(results, dict)
    assert "updates" in results and len(results["updates"]) > 0
    assert "creates" in results
    assert "errors" in results and len(results["errors"]) == 0
