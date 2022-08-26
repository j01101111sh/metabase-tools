from typing import NoReturn

import pytest
from typing_extensions import assert_never

from metabase_tools import MetabaseApi
from metabase_tools.exceptions import AuthenticationFailure


@pytest.fixture
def credentials():
    from tests.metabase_details import CREDENTIALS

    return CREDENTIALS


@pytest.fixture
def host():
    from tests.metabase_details import HOST

    return HOST


@pytest.fixture
def email():
    from tests.metabase_details import EMAIL

    return EMAIL


@pytest.fixture
def token(host, credentials):
    api = MetabaseApi(metabase_url=host, credentials=credentials, cache_token=True)
    with open("./metabase.token", "r") as f:
        return {"token": f.read()}


def test_auth_credential_success(host, credentials):
    api = MetabaseApi(
        metabase_url=host, credentials=credentials, token_path="./missing.token"
    )
    assert api.test_for_auth()


def test_auth_credential_fail(host, email):
    bad_credentials = {"username": email, "password": "badpass"}
    with pytest.raises(AuthenticationFailure):
        api = MetabaseApi(
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
        assert_never(NoReturn)


def test_auth_token_fail(host):
    bad_credentials = {"token": "badtoken"}
    with pytest.raises(AuthenticationFailure):
        api = MetabaseApi(
            metabase_url=host, credentials=bad_credentials, token_path="./missing.token"
        )
        test_data = api.get(endpoint="/user/current")


def test_auth_token_file_success(host, token):
    api = MetabaseApi(metabase_url=host, credentials=token)
    assert api.test_for_auth()


def test_auth_token_file_fail(host):
    with pytest.raises(AuthenticationFailure):
        api = MetabaseApi(metabase_url=host, token_path="./missing.token")


def test_auth_without_protocol(host, credentials):
    api = MetabaseApi(metabase_url=host[7:], credentials=credentials)
    assert api.test_for_auth()
