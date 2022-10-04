import shutil
from json import loads
from pathlib import Path
from random import choice
from string import ascii_letters
from time import sleep

import requests
from packaging.version import Version

metabase_config = {
    "host": "http://localhost:3000",
    "first": "Jim",
    "last": "Halpert",
    "email": "jim@dundermifflin.com",
    "password": "BAZouVa3saWgW89z",
    "site_name": "testing-site",
    "credentials": {
        "username": "jim@dundermifflin.com",
        "password": "BAZouVa3saWgW89z",
    },
}


def random_string(chars) -> str:
    return "".join(choice(ascii_letters) for _ in range(chars))


def check_status_code(response: requests.Response) -> requests.Response:
    if 200 <= response.status_code <= 299:
        return response
    raise requests.HTTPError(
        f"{response.status_code} - {response.reason}: {loads(response.text)['errors']}"
    )


def initial_setup():
    MAX_ATTEMPTS = 12
    TIMEOUT = 5
    WAIT_INTERVAL = 5
    token_response = None
    for x in range(MAX_ATTEMPTS + 1):
        print(f"Attempt #{x+1}:")
        try:
            token_response = requests.get(
                metabase_config["host"] + "/api/session/properties", timeout=TIMEOUT
            )
            print("Success!")
            break
        except requests.exceptions.ConnectionError:
            # Wait and try again if connection doesn't work the first time
            print(f"ConnectionError encountered. Waiting {WAIT_INTERVAL} seconds...")
            sleep(WAIT_INTERVAL)
        except requests.exceptions.ReadTimeout:
            print(f"ReadTimeout encountered. Trying again...")

    if not token_response:
        raise requests.exceptions.ConnectionError

    setup_token = token_response.json()["setup-token"]
    response = requests.post(
        metabase_config["host"] + "/api/setup",
        json={
            "prefs": {"site_name": metabase_config["site_name"]},
            "user": {
                "email": metabase_config["email"],
                "password": metabase_config["password"],
                "first_name": metabase_config["first"],
                "last_name": metabase_config["last"],
                "site_name": metabase_config["site_name"],
            },
            "token": setup_token,
        },
    )
    return check_status_code(response)


def get_session() -> requests.Session:
    session = requests.Session()
    post_request = requests.post(
        f"{metabase_config['host']}/api/session", json=metabase_config["credentials"]
    )
    token = post_request.json()["id"]
    headers = {
        "Content-Type": "application/json",
        "X-Metabase-Session": token,
    }
    session.headers.update(headers)
    return session


def create_users(session: requests.Session):
    dev = {
        "first_name": "Dev",
        "last_name": "Setup",
        "email": "dev@DunderMifflin.com",
        "password": random_string(20),
    }
    std = {
        "first_name": "Standard",
        "last_name": "Setup",
        "email": "std@DunderMifflin.com",
        "password": random_string(20),
    }
    uat = {
        "first_name": "UAT",
        "last_name": "Setup",
        "email": "uat@DunderMifflin.com",
        "password": random_string(20),
    }
    responses = []
    for user in [dev, std, uat]:
        response = session.post(f"{metabase_config['host']}/api/user", json=user)
        responses.append(check_status_code(response=response))
    for user in range(50):
        definition = std.copy()
        definition["first_name"] += str(user)
        definition["email"] = f"std{user}@DunderMifflin.com"
        response = session.post(f"{metabase_config['host']}/api/user", json=definition)
        responses.append(check_status_code(response=response))
    return responses


def create_collections(session: requests.Session):
    dev = {
        "name": "Development",
        "color": "#FFFFFF",
    }
    uat = {
        "name": "UAT",
        "color": "#FFFFFF",
    }
    prod = {
        "name": "Production",
        "color": "#FFFFFF",
    }
    accounting = {"name": "Accounting", "color": "#FFFFFF", "parent_id": 2}
    responses = []
    for coll in [dev, uat, prod, accounting]:
        response = session.post(f"{metabase_config['host']}/api/collection", json=coll)
        responses.append(check_status_code(response=response))
    return responses


def create_cards(session: requests.Session):
    accounting = {
        "visualization_settings": {
            "table.pivot_column": "QUANTITY",
            "table.cell_column": "ID",
        },
        "collection_id": 2,
        "name": "Accounting",
        "dataset_query": {
            "type": "native",
            "native": {
                "query": "--This card was created through the API\nSELECT ID, USER_ID, PRODUCT_ID, SUBTOTAL, TAX, TOTAL, DISCOUNT, CREATED_AT, QUANTITY\r\nFROM ORDERS\r\nLIMIT 100"
            },
            "database": 1,
        },
        "display": "table",
    }
    test = {
        "visualization_settings": {
            "table.pivot_column": "QUANTITY",
            "table.cell_column": "ID",
        },
        "collection_id": 2,
        "name": "Test",
        "dataset_query": {
            "type": "native",
            "native": {
                "query": "--This card was created through the API\nSELECT ID, USER_ID, PRODUCT_ID, SUBTOTAL, TAX, TOTAL, DISCOUNT, CREATED_AT, QUANTITY\r\nFROM ORDERS\r\nLIMIT 100"
            },
            "database": 1,
        },
        "display": "table",
    }
    name_error = {  # This should cause a name error when the download is attempting to write the file name
        "visualization_settings": {
            "table.pivot_column": "QUANTITY",
            "table.cell_column": "ID",
        },
        "collection_id": 2,
        "name": "Name/Error #1",
        "dataset_query": {
            "type": "native",
            "native": {
                "query": "--This card was created through the API\nSELECT ID, USER_ID, PRODUCT_ID, SUBTOTAL, TAX, TOTAL, DISCOUNT, CREATED_AT, QUANTITY\r\nFROM ORDERS\r\nLIMIT 100"
            },
            "database": 1,
        },
        "display": "table",
    }
    responses = []
    for card in [accounting, test, name_error]:
        response = session.post(f"{metabase_config['host']}/api/card", json=card)
        responses.append(check_status_code(response=response))
    return responses


def create_databases(session: requests.Session, server_version: Version):
    new_db = {
        "name": "Test DB",
        "engine": "h2",
        "details": {
            "db": "zip:/app/metabase.jar!/sample-dataset.db;USER=GUEST;PASSWORD=guest"
        },
    }
    if server_version >= Version("v0.42"):
        new_db["details"]["db"] = new_db["details"]["db"].replace(
            "sample-dataset", "sample-database"
        )

    results = [session.post(f"{metabase_config['host']}/api/database", json=new_db)]
    for x in range(3):
        definition = new_db.copy()
        definition["name"] += str(x)
        results.append(
            session.post(f"{metabase_config['host']}/api/database", json=definition)
        )


def cleanup_cache_and_logs():
    cleanup_targets = [
        Path("./.mypy_cache/"),
        Path("./.pytest_cache/"),
        Path("./docs/build/"),
        Path("./htmlcov/"),
        Path("./metabase_tools/__pycache__/"),
        Path("./metabase_tools/endpoints/__pycache__/"),
        Path("./metabase_tools/models/__pycache__/"),
        Path("./temp/"),
        Path("./tests/__pycache__/"),
        Path("./tests/models/__pycache__/"),
        Path("./.coverage"),
    ]
    for item in cleanup_targets:
        if item.exists() and item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
        elif item.exists():
            item.unlink()
        else:
            pass
    pass


def get_server_version(session: requests.Session) -> Version:
    result = session.get(f"{metabase_config['host']}/api/session/properties").json()
    if isinstance(result, dict):
        return Version(result["version"]["tag"])
    raise ValueError


def set_server_settings(session: requests.Session) -> list[requests.Response]:
    embed_result = session.put(
        f"{metabase_config['host']}/api/setting/enable-embedding"
    )
    email_result = set_email_settings(session)
    return [embed_result, email_result]


def set_email_settings(session: requests.Session) -> requests.Response:
    settings = {
        "email-from-address": metabase_config["email"],
        "email-smtp-host": "mailhog",
        "email-smtp-port": 1025,
    }
    email_result = session.put(f"{metabase_config['host']}/api/email", json=settings)
    return email_result


if __name__ == "__main__":
    cleanup_cache_and_logs()
    setup_response = initial_setup()
    session = get_session()
    server_version = get_server_version(session)
    server_settings = set_server_settings(session)
    user_responses = create_users(session)
    coll_responses = create_collections(session)
    card_responses = create_cards(session)
    db_responses = create_databases(session, server_version)
