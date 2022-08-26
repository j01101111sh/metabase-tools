from datetime import datetime
from pathlib import Path

import pytest

_run_id = datetime.now().strftime("%y%m%dT%H%M%S")
_result_path = Path(f"./temp/test-{_run_id}")


@pytest.fixture(scope="session")
def run_id() -> str:
    return _run_id


@pytest.fixture(scope="session")
def result_path() -> Path:
    return _result_path


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
