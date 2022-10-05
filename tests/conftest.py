import os
from datetime import datetime
from pathlib import Path
from platform import python_version
from random import choice
from string import ascii_letters

import pytest
import requests

from metabase_tools import MetabaseApi
from tests.setup_metabase import metabase_config

_run_id = os.environ.get("GITHUB_RUN_ID", datetime.now().strftime("%y%m%dT%H%M%S"))
_python_version = python_version().replace(".", "_")

properties = requests.get("http://localhost:3000/api/session/properties").json()
if isinstance(properties, dict):
    _mb_version = properties["version"]["tag"].replace(".", "_")
else:
    _mb_version = os.environ.get("MB_VERSION", "unknown").replace(".", "_")

_result_path = Path(f"./temp/test-{_run_id}/py_{_python_version}/mb_{_mb_version}")


@pytest.fixture(scope="function")
def random_string() -> object:
    return lambda l: "".join(choice(ascii_letters) for _ in range(l))


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
    return metabase_config["credentials"]


@pytest.fixture(scope="session")
def host():
    return metabase_config["host"]


@pytest.fixture(scope="session")
def email():
    return metabase_config["email"]


@pytest.fixture(scope="session")
def password():
    return metabase_config["password"]


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
