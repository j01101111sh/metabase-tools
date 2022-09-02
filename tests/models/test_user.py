import pytest

from metabase_tools import MetabaseApi, User
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


def test_user_create_one(api: MetabaseApi, new_def: dict):
    def_one = new_def.copy()
    def_one["name"] = "Test " + random_string(6)
    new_obj = User.create(adapter=api, payloads=[def_one])
    assert isinstance(new_obj, list)
    assert all(isinstance(o, User) for o in new_obj)


def test_user_create_many(api: MetabaseApi, new_def: dict):
    def_one = new_def.copy()
    def_one["first_name"] = random_string(6)
    def_one["email"] = f"{def_one['first_name']}@DunderMifflin.com"
    def_two = new_def.copy()
    def_two["first_name"] = random_string(6)
    def_two["email"] = f"{def_two['first_name']}@DunderMifflin.com"
    new_defs = [def_one, def_two]
    new_objs = User.create(adapter=api, payloads=new_defs)
    assert isinstance(new_objs, list)
    assert all(isinstance(o, User) for o in new_objs)


def test_user_update_one(api: MetabaseApi):
    new_name = random_string(6)
    change = {"id": 3, "first_name": new_name}
    results = User.update(adapter=api, payload=[change])
    assert isinstance(results, list)
    assert all(isinstance(o, User) for o in results)
    assert all(o.first_name == new_name for o in results)


def test_user_update_many(api: MetabaseApi):
    new_name = random_string(6)
    change_one = {"id": 3, "first_name": new_name}
    change_two = {"id": 4, "first_name": new_name}
    new_defs = [change_one, change_two]
    results = User.update(adapter=api, payload=new_defs)
    assert isinstance(results, list)
    assert all(isinstance(o, User) for o in results)
    assert all(o.first_name == new_name for o in results)


def test_user_disable_one(api: MetabaseApi):
    targets = [2]
    results = User.disable(adapter=api, targets=targets)
    assert isinstance(results, dict)
    assert all(isinstance(v, dict) for _, v in results.items())
    assert all(v["success"] for _, v in results.items())


def test_user_disable_many(api: MetabaseApi):
    targets = [3, 4]
    results = User.disable(adapter=api, targets=targets)
    assert isinstance(results, dict)
    assert all(isinstance(v, dict) for _, v in results.items())
    assert all(v["success"] for _, v in results.items())


def test_user_enable_one(api: MetabaseApi):
    targets = [2]
    results = User.disable(adapter=api, targets=targets)
    results = User.enable(adapter=api, targets=targets)
    assert isinstance(results, list)
    assert all(isinstance(o, User) for o in results)
    assert all(o.is_active for o in results)


def test_user_enable_many(api: MetabaseApi):
    targets = [3, 4]
    results = User.disable(adapter=api, targets=targets)
    results = User.enable(adapter=api, targets=targets)
    assert isinstance(results, list)
    assert all(isinstance(o, User) for o in results)
    assert all(o.is_active for o in results)


def test_user_get_one(api: MetabaseApi):
    user_to_get = [1]
    user = User.get(adapter=api, targets=user_to_get)
    assert isinstance(user, list)
    assert all(isinstance(u, User) for u in user)


def test_user_get_many(api: MetabaseApi):
    users_to_get = [1, 2, 3]
    users = User.get(adapter=api, targets=users_to_get)
    assert isinstance(users, list)
    assert all(isinstance(user, User) for user in users)


def test_user_get_all(api: MetabaseApi):
    users = User.get(adapter=api)
    assert isinstance(users, list)
    assert all(isinstance(user, User) for user in users)


def test_user_current(api: MetabaseApi):
    user = User.current(adapter=api)
    assert isinstance(user, User)


def test_user_resend(api: MetabaseApi):
    targets = [2]
    result = User.resend_invite(adapter=api, targets=targets)
    assert isinstance(result, list)
    assert all(isinstance(r, dict) for r in result)


def test_user_reset_password(api: MetabaseApi):
    payloads = [{"id": 2, "password": "asdfoin33kn23fkmsdf"}]
    result = User.update_password(adapter=api, payloads=payloads)
    assert isinstance(result, list)
    assert all(isinstance(r, User) for r in result)
    assert len(payloads) == len(result)


def test_user_qbnewb(api: MetabaseApi):
    targets = [2]
    result = User.qbnewb(adapter=api, targets=targets)
    assert isinstance(result, list)
    assert all(isinstance(r, dict) for r in result)
    assert len(targets) == len(result)
