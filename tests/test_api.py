from pathlib import Path

import packaging.version
import pytest

from metabase_tools import MetabaseApi
from metabase_tools.exceptions import AuthenticationFailure


@pytest.fixture
def token(host, credentials, result_path, run_id):
    token_path = f"{result_path}/{run_id}.token"
    _ = MetabaseApi(
        metabase_url=host,
        credentials=credentials,
        cache_token=True,
        token_path=token_path,
    )
    with open(token_path, "r", encoding="utf-8") as file:
        return {"token": file.read()}


def test_server_version(api: MetabaseApi):
    assert isinstance(api.server_version, packaging.version.Version)
