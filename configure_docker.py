import requests

HOST = 'http://localhost:3000'
FIRST = 'Jim'
LAST = 'Halpert'
EMAIL = 'jim@dundermifflin.com'
PASSWORD = 'Whg6R96c*^fc{um>'
SITE_NAME = 'testing-site'

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
