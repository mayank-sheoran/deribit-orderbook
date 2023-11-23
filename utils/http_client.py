import os

import requests

def getAuth_Sid_Refresh_AccessToken():
    baseHttpUrl = str(os.environ.get("DERIBIT_BASE_HTTP_URL"))
    clientId = os.environ.get("CLIENT_ID")
    clientSecret = os.environ.get("CLIENT_SECRET")
    params = {
        "client_id": clientId,
        "client_secret": clientSecret,
        "grant_type": "client_credentials"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.get(baseHttpUrl + '/public/auth', params=params, headers=headers)
    if response.status_code == 200:
        result = response.json()['result']
        return result['sid'], result['refresh_token'], result['access_token']
    else:
        print("Failed Auth Response text:", response.text)