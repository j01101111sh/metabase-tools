import requests

from metabase_details import EMAIL, FIRST, HOST, LAST, PASSWORD, SITE_NAME

response = requests.get(HOST + '/api/session/properties')
setup_token = response.json()['setup-token']
response = requests.post(
    HOST + '/api/setup',
    json={
        'prefs': {'site_name': SITE_NAME},
        'user': {
            'email': EMAIL,
            'password': PASSWORD,
            'first_name': FIRST,
            'last_name': LAST,
            'site_name': SITE_NAME,
        },
        'token': setup_token,
    },
)
