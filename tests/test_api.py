from pathlib import Path

from packaging.version import Version
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


def test_auth_credential_success(host, credentials):
    api = MetabaseApi(
        metabase_url=host, credentials=credentials, token_path="./missing.token"
    )
    assert api.test_for_auth()


def test_auth_credential_fail(host, email):
    bad_credentials = {"username": email, "password": "badpass"}
    with pytest.raises(AuthenticationFailure):
        _ = MetabaseApi(
            metabase_url=host, credentials=bad_credentials, token_path="./missing.token"
        )


def test_auth_token_success(host, token, email):
    api = MetabaseApi(
        metabase_url=host, credentials=token, token_path="./missing.token"
    )
    test_response = api.get(endpoint="/user/current")
    if isinstance(test_response, dict):
        assert test_response.get("email") == email
    else:
        assert False


def test_auth_token_fail(host):
    bad_credentials = {"token": "badtoken"}
    with pytest.raises(AuthenticationFailure):
        api = MetabaseApi(
            metabase_url=host, credentials=bad_credentials, token_path="./missing.token"
        )
        _ = api.get(endpoint="/user/current")


def test_auth_token_file_success(api, host, result_path, run_id):
    _ = api
    token_path = Path(f"{result_path}/{run_id}.token")
    new_api = MetabaseApi(metabase_url=host, token_path=token_path)
    assert new_api.test_for_auth()


def test_auth_token_file_fail(host):
    with pytest.raises(AuthenticationFailure):
        _ = MetabaseApi(metabase_url=host, token_path="./missing.token")


def test_auth_without_protocol(host, credentials):
    api = MetabaseApi(metabase_url=host[7:], credentials=credentials)
    assert api.test_for_auth()


def test_cache_token(host, credentials, result_path, run_id, token):
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


def test_fail_on_no_credentials(host):
    with pytest.raises(AuthenticationFailure):
        _ = MetabaseApi(metabase_url=host)


def test_url_ends_in_slash(host, credentials):
    api = MetabaseApi(metabase_url=f"{host}/", credentials=credentials)
    assert api.test_for_auth()


def test_url_ends_in_api(host, credentials):
    api = MetabaseApi(metabase_url=f"{host}/api", credentials=credentials)
    assert api.test_for_auth()


def test_url_ends_in_api_and_slash(host, credentials):
    api = MetabaseApi(metabase_url=f"{host}/api/", credentials=credentials)
    assert api.test_for_auth()


def test_bad_cached_token_erased(host, credentials, caplog):
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


def test_bad_passed_token(host, caplog):
    bad_token = {"token": "badtoken"}
    with pytest.raises(AuthenticationFailure):
        _ = MetabaseApi(metabase_url=host, credentials=bad_token)
    assert "Failed to authenticate with token passed" in caplog.text


def test_bad_passed_token_with_fallback(host, credentials, caplog):
    credentials["token"] = "badtoken"
    api = MetabaseApi(metabase_url=host, credentials=credentials)
    assert api.test_for_auth()
    assert "Failed to authenticate with token passed" in caplog.text
    assert "Authenticated with login" in caplog.text


def test_server_version(api: MetabaseApi):
    assert isinstance(api.server_version, Version)
