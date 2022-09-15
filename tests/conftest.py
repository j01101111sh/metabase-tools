import os
from datetime import datetime
from pathlib import Path
from platform import python_version

import pytest

from metabase_tools import MetabaseApi
from tests import helpers

_run_id = datetime.now().strftime("%y%m%dT%H%M%S")
_python_version = python_version().replace(".", "_")
_mb_verison = os.environ.get("MB_VERSION", "unknown").replace(".", "_")
_result_path = Path(f"./temp/test-{_run_id}/py_{_python_version}/mb_{_mb_verison}")


@pytest.fixture(scope="session")
def run_id() -> str:
    return _run_id


@pytest.fixture(scope="session")
def result_path() -> Path:
    return _result_path


@pytest.fixture(scope="package")
def api(host, credentials):
    token_path = f"{_result_path}/{_run_id}.token"
    return MetabaseApi(
        metabase_url=host,
        credentials=credentials,
        cache_token=True,
        token_path=token_path,
    )


@pytest.fixture(scope="package")
def server_version(api: MetabaseApi):
    return api.server_version


@pytest.fixture(scope="session")
def credentials():
    return helpers.CREDENTIALS


@pytest.fixture(scope="session")
def host():
    return helpers.HOST


@pytest.fixture(scope="session")
def email():
    return helpers.EMAIL


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item):
    config = item.config
    logging_plugin = config.pluginmanager.get_plugin("logging-plugin")

    test_result_path = (
        item.nodeid.split(".py", 1)[0].replace("tests/", "logs/") + f"/{item.name}"
    )

    full_fname = Path(f"{_result_path}/{test_result_path}.log")
    logging_plugin.set_log_path(full_fname)
    yield
