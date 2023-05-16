import requests
from base64 import b64encode

url = 'https://accounts.spotify.com/api/token'

def get_token(client, secret):
    joined = ':'.join([client, secret])
    bytes = joined.encode('ascii')
    encoded = b64encode(bytes)
    doneAuth = encoded.decode('ascii')
    
    body = {'grant_type' : 'client_credentials'}
    toke = {
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + doneAuth
    }

    resp = requests.post(url=url, data=body, headers=toke)
    return resp.json()['access_token']