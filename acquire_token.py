import json
import requests

token = None


def get_token():
    global token
    if not token:
        with open("secrets.json", "r") as json_file:
            secrets = json.load(json_file)

        # Get your FarmBot Web App token.
        headers = {'content-type': 'application/json'}
        user = {'user': {'email': secrets["username"], 'password': secrets["password"]}}
        response = requests.post('https://my.farmbot.io/api/tokens',
                                 headers=headers, json=user)
        token = response.json()['token']['encoded']
    return token


def get_headers():
    headers = {'Authorization': 'Bearer ' + get_token(),
               'content-type': "application/json"}
    return headers
