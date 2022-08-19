import pytest

from metabase_tools import MetabaseApi, User


@pytest.fixture(scope="module")
def api(host, credentials):
    return MetabaseApi(
        metabase_url=host,
        credentials=credentials,
        cache_token=True,
        token_path="./metabase.token",
    )


@pytest.fixture(scope="module")
def credentials():
    from tests.metabase_details import CREDENTIALS

    return CREDENTIALS


@pytest.fixture(scope="module")
def host():
    from tests.metabase_details import HOST

    return HOST


def test_user_get_one(api: MetabaseApi):
    user_to_get = [1]
    user = User.get(adapter=api, targets=user_to_get)
    assert isinstance(user, list)
    assert all(isinstance(u, User) for u in user)


def test_user_get_many(api: MetabaseApi):
    users_to_get = [1, 1]
    users = User.get(adapter=api, targets=users_to_get)
    assert isinstance(users, list)
    assert all(isinstance(user, User) for user in users)


def test_user_get_all(api: MetabaseApi):
    users = User.get(adapter=api)
    assert isinstance(users, list)
    assert all(isinstance(user, User) for user in users)
