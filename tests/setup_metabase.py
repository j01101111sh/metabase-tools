import json
from random import choice
from string import ascii_letters, digits

import requests

from tests.metabase_details import (
    CREDENTIALS,
    EMAIL,
    FIRST,
    HOST,
    LAST,
    PASSWORD,
    SITE_NAME,
)


def initial_setup():
    token_response = requests.get(HOST + "/api/session/properties")
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
    if 200 >= response.status_code <= 299:
        return response
    raise requests.HTTPError(
        f"{response.status_code} - {response.reason}: {json.loads(response.text)['errors']}"
    )


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
        "email": f"dev@DunderMifflin.com",
        "password": "".join(choice(ascii_letters + digits) for _ in range(20)),
    }
    std = {
        "first_name": "Standard",
        "last_name": "Setup",
        "email": f"std@DunderMifflin.com",
        "password": "".join(choice(ascii_letters + digits) for _ in range(20)),
    }
    uat = {
        "first_name": "UAT",
        "last_name": "Setup",
        "email": f"uat@DunderMifflin.com",
        "password": "".join(choice(ascii_letters + digits) for _ in range(20)),
    }
    responses = []
    for user in [dev, std, uat]:
        response = session.post(f"{HOST}/api/user", json=user)
        if 200 >= response.status_code <= 299:
            responses.append(response)
        else:
            raise requests.HTTPError(
                f"{user['email']} - error {response.status_code} - {response.reason}: {json.loads(response.text)['errors']}"
            )
    return responses


def create_databases():
    pass


def create_collections():
    pass


def create_cards():
    pass


if __name__ == "__main__":
    setup_response = initial_setup()
    session = get_session()
    user_responses = create_users(session)
