from pathlib import Path

import pytest
from packaging.version import Version

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


class TestApiGeneral:
    def test_auth_credential_success(self, host: str, credentials: dict):
        api = MetabaseApi(
            metabase_url=host, credentials=credentials, token_path="./missing.token"
        )
        assert api.test_for_auth()

    def test_auth_credential_fail(self, host: str, email: str):
        bad_credentials = {"username": email, "password": "badpass"}
        with pytest.raises(AuthenticationFailure):
            _ = MetabaseApi(
                metabase_url=host,
                credentials=bad_credentials,
                token_path="./missing.token",
            )

    def test_auth_token_success(self, host: str, token: dict, email: str):
        api = MetabaseApi(
            metabase_url=host, credentials=token, token_path="./missing.token"
        )
        test_response = api.get(endpoint="/user/current")
        if isinstance(test_response, dict):
            assert test_response.get("email") == email
        else:
            assert False

    def test_auth_token_fail(self, host: str):
        bad_credentials = {"token": "badtoken"}
        with pytest.raises(AuthenticationFailure):
            api = MetabaseApi(
                metabase_url=host,
                credentials=bad_credentials,
                token_path="./missing.token",
            )
            _ = api.get(endpoint="/user/current")

    def test_auth_token_file_success(
        self, api: MetabaseApi, host: str, result_path: str, run_id: str
    ):
        _ = api
        token_path = Path(f"{result_path}/{run_id}.token")
        new_api = MetabaseApi(metabase_url=host, token_path=token_path)
        assert new_api.test_for_auth()

    def test_auth_token_file_fail(self, host: str):
        with pytest.raises(AuthenticationFailure):
            _ = MetabaseApi(metabase_url=host, token_path="./missing.token")

    def test_auth_without_protocol(self, host: str, credentials: dict):
        api = MetabaseApi(metabase_url=host[7:], credentials=credentials)
        assert api.test_for_auth()

    def test_cache_token(
        self, host: str, credentials: dict, result_path: str, run_id: str, token: dict
    ):
        token_path = f"{result_path}/{run_id}.token"
        api = MetabaseApi(
            metabase_url=host,
            credentials=credentials,
            cache_token=True,
            token_path=token_path,
        )
        with open(token_path, "r", encoding="utf-8") as file:
            cached_token = {"token": file.read()}
        assert cached_token == token
        assert api.test_for_auth()

    def test_fail_on_no_credentials(self, host: str):
        with pytest.raises(AuthenticationFailure):
            _ = MetabaseApi(metabase_url=host)

    def test_url_ends_in_slash(self, host: str, credentials: dict):
        api = MetabaseApi(metabase_url=f"{host}/", credentials=credentials)
        assert api.test_for_auth()

    def test_url_ends_in_api(self, host: str, credentials: dict):
        api = MetabaseApi(metabase_url=f"{host}/api", credentials=credentials)
        assert api.test_for_auth()

    def test_url_ends_in_api_and_slash(self, host: str, credentials: dict):
        api = MetabaseApi(metabase_url=f"{host}/api/", credentials=credentials)
        assert api.test_for_auth()

    def test_bad_cached_token_erased(self, host: str, credentials: dict, caplog):
        bad_token = "badtoken"
        bad_token_path = Path("bad_token.token")
        with open(bad_token_path, "w", encoding="utf-8") as file:
            file.write(bad_token)
        api = MetabaseApi(
            metabase_url=host, credentials=credentials, token_path=bad_token_path
        )
        assert api.test_for_auth()
        assert not bad_token_path.exists()
        assert "Deleting token file" in caplog.text

    def test_bad_passed_token(self, host: str, caplog):
        bad_token = {"token": "badtoken"}
        with pytest.raises(AuthenticationFailure):
            _ = MetabaseApi(metabase_url=host, credentials=bad_token)
        assert "Failed to authenticate with token passed" in caplog.text

    def test_bad_passed_token_with_fallback(self, host: str, credentials: dict, caplog):
        credentials["token"] = "badtoken"
        api = MetabaseApi(metabase_url=host, credentials=credentials)
        assert api.test_for_auth()
        assert "Failed to authenticate with token passed" in caplog.text
        assert "Authenticated with login" in caplog.text

    def test_server_version(self, api: MetabaseApi):
        assert isinstance(api.server_version, Version)
