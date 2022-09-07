from json import loads
from time import sleep

import requests

from tests.helpers import (
    CREDENTIALS,
    EMAIL,
    FIRST,
    HOST,
    LAST,
    PASSWORD,
    SITE_NAME,
    random_string,
)


def check_status_code(response: requests.Response) -> requests.Response:
    if 200 <= response.status_code <= 299:
        return response
    raise requests.HTTPError(
        f"{response.status_code} - {response.reason}: {loads(response.text)['errors']}"
    )


def initial_setup():
    MAX_ATTEMPTS = 10
    WAIT_INTERVAL = 10
    token_response = None
    for _ in range(MAX_ATTEMPTS + 1):
        try:
            token_response = requests.get(HOST + "/api/session/properties")
            break
        except requests.exceptions.ConnectionError:
            # Wait and try again if connection doesn't work the first time
            sleep(WAIT_INTERVAL)

    if not token_response:
        raise requests.exceptions.ConnectionError

    setup_token = token_response.json()["setup-token"]
    response = requests.post(
        HOST + "/api/setup",
        json={
            "prefs": {"site_name": SITE_NAME},
            "user": {
                "email": EMAIL,
                "password": PASSWORD,
                "first_name": FIRST,
                "last_name": LAST,
                "site_name": SITE_NAME,
            },
            "token": setup_token,
        },
    )
    return check_status_code(response)


def get_session() -> requests.Session:
    session = requests.Session()
    post_request = requests.post(f"{HOST}/api/session", json=CREDENTIALS)
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
        response = session.post(f"{HOST}/api/user", json=user)
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
        response = session.post(f"{HOST}/api/collection", json=coll)
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
        response = session.post(f"{HOST}/api/card", json=card)
        responses.append(check_status_code(response=response))
    return responses


def create_databases(session: requests.Session):
    new_db = {
        "name": "Test DB",
        "engine": "h2",
        "details": {
            "db": "zip:/app/metabase.jar!/sample-dataset.db;USER=GUEST;PASSWORD=guest"
        },
    }
    return session.post(f"{HOST}/api/database", json=new_db)


if __name__ == "__main__":
    setup_response = initial_setup()
    session = get_session()
    user_responses = create_users(session)
    coll_responses = create_collections(session)
    card_responses = create_cards(session)
    db_responses = create_databases(session)
