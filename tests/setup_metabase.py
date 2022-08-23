import requests

from tests.metabase_details import EMAIL, FIRST, HOST, LAST, PASSWORD, SITE_NAME


def initial_setup():
    response = requests.get(HOST + "/api/session/properties")
    setup_token = response.json()["setup-token"]
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


def create_users():
    pass


def create_databases():
    pass


def create_collections():
    pass


def create_cards():
    pass


if __name__ == "__main__":
    initial_setup()
