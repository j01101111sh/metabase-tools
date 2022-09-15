from datetime import datetime
from pathlib import Path
from platform import python_version

import pytest

from metabase_tools import MetabaseApi
from tests import helpers

_run_id = datetime.now().strftime("%y%m%dT%H%M%S")
_python_version = python_version().replace(".", "_")
_result_path = Path(f"./temp/test-{_run_id}/python_{_python_version}")


@pytest.fixture(scope="package")
def api(host, credentials):
    token_path = f"{_result_path}/{_run_id}.token"
    return MetabaseApi(
        metabase_url=host,
        credentials=credentials,
        cache_token=True,
        token_path=token_path,
    )
