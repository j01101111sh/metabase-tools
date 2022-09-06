import random

import pytest

from metabase_tools import MetabaseApi, UserItem
from tests.helpers import random_string


@pytest.fixture(scope="function")
def new_def():
    first_name = random_string(6)
    return {
        "first_name": first_name,
        "last_name": "Test",
        "email": f"{first_name}@DunderMifflin.com",
        "password": random_string(20),
    }


@pytest.fixture(scope="module")
def users(api: MetabaseApi) -> list[UserItem]:
    return api.users.get()[1:]


def test_user_create_one(api: MetabaseApi, new_def: dict):
    def_one = new_def.copy()
    def_one["name"] = "Test " + random_string(6)
    new_obj = api.users.create(payloads=[def_one])
    assert isinstance(new_obj, list)
    assert all(isinstance(o, UserItem) for o in new_obj)


def test_user_create_many(api: MetabaseApi, new_def: dict):
    def_one = new_def.copy()
    def_one["first_name"] = random_string(6)
    def_one["email"] = f"{def_one['first_name']}@DunderMifflin.com"
    def_two = new_def.copy()
    def_two["first_name"] = random_string(6)
    def_two["email"] = f"{def_two['first_name']}@DunderMifflin.com"
    new_defs = [def_one, def_two]
    new_objs = api.users.create(payloads=new_defs)
    assert isinstance(new_objs, list)
    assert all(isinstance(o, UserItem) for o in new_objs)


def test_user_update_one(users: list[UserItem]):
    item = random.choice(users)
    new_name = random_string(6)
    change = {"id": item.id, "first_name": new_name}
    results = item.update(payload=change)
    assert isinstance(results, UserItem)
    assert results.first_name == new_name


def test_user_disable_one(users: list[UserItem]):
    item = random.choice(users)
    try:
        _ = item.enable()
    except:
        pass
    results = item.disable()
    assert isinstance(results, dict)
    assert all(isinstance(v, dict) for v in results.values())
    assert all(v["success"] is True for v in results.values())


def test_user_enable_one(users: list[UserItem]):
    item = random.choice(users)
    try:
        _ = item.disable()
    except:
        pass
    results = item.enable()
    assert isinstance(results, UserItem)
    assert results.is_active is True


def test_user_get_one(api: MetabaseApi):
    user_to_get = [1]
    user = api.users.get(targets=user_to_get)
    assert isinstance(user, list)
    assert all(isinstance(u, UserItem) for u in user)
    assert len(user_to_get) == len(user)


def test_user_get_many(api: MetabaseApi):
    targets = [1, 2, 3]
    results = api.users.get(targets=targets)
    assert isinstance(results, list)
    assert all(isinstance(user, UserItem) for user in results)
    assert len(targets) == len(results)


def test_user_get_all(api: MetabaseApi):
    users = api.users.get()
    assert isinstance(users, list)
    assert all(isinstance(user, UserItem) for user in users)


def test_user_current(api: MetabaseApi):
    user = api.users.current()
    assert isinstance(user, UserItem)


def test_user_resend(users: list[UserItem]):
    item = random.choice(users)
    result = item.resend_invite()
    assert isinstance(result, dict)
    assert result["success"] is True


def test_user_reset_password(users: list[UserItem]):
    item = random.choice(users)
    payload = {"id": 2, "password": "asdfoin33kn23fkmsdf"}
    result = item.update_password(payload=payload)
    assert isinstance(result, UserItem)


def test_user_qbnewb(users: list[UserItem]):
    item = random.choice(users)
    result = item.qbnewb()
    assert isinstance(result, dict)
    assert result["success"] is True
