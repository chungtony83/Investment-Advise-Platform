import requests
import os
import base64
import urllib.parse
import subprocess
from datetime import datetime, timedelta
import warnings
from cryptography.fernet import Fernet
import json
import time


path = os.getenv("SCHWAB_TOKEN_ENCRYP_KEY")

key = Fernet(open(path, "rb").read())

def get_refresh_token() -> None:
    client_id = key.decrypt(open('./tokens/client_id.enc', 'rb').read()).decode()
    client_secret = key.decrypt(open('./tokens/client_secret.enc', 'rb').read()).decode()
    redirect_uri = "https://127.0.0.1"  # Must match exactly what's registered in your Schwab Developer Portal

    # 1. Construct the authorization URL with response_type=code
    auth_url = f"https://api.schwabapi.com/v1/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}"

    print(f"Click to authenticate: {auth_url}")

    # 2. Capture the redirected URL from user input
    returned_link = input("Paste the redirect URL here:")

    # 3. Parse the 'code' parameter from the redirect
    parsed_url = urllib.parse.urlparse(returned_link)
    parsed_query = urllib.parse.parse_qs(parsed_url.query)
    auth_code = parsed_query.get('code', [None])[0]

    if not auth_code:
        print("Could not find 'code' parameter in the redirect URL.")
        return

    # 4. Exchange the authorization code for access tokens
    token_url = "https://api.schwabapi.com/v1/oauth/token"

    # Option A: Pass client_id and client_secret in the POST body
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {'Authorization': f'Basic {base64.b64encode(bytes(f"{client_id}:{client_secret}", "utf-8")).decode("utf-8")}', 'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(token_url, data=data, headers=headers)
    tokens = response.json()

    # 5. Extract and print tokens
    if 'access_token' in tokens:
        expires_times = {'access_token': (datetime.now() + timedelta(seconds=tokens['expires_in'])).strftime("%Y-%m-%d %H:%M:%S"),
                         'refresh_token': (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")}
        json.dump(expires_times, open('./tokens/expires_times.json', 'w'))
        with open(f'./tokens/access_token.enc', 'wb') as f: f.write(key.encrypt(tokens['access_token'].encode()))
        with open(f'./tokens/refresh_token.enc', 'wb') as f: f.write(key.encrypt(tokens['refresh_token'].encode()))
        print("Access token & Refresh token updated successfully.")
    else:
        print("Error exchanging authorization code:", tokens)
        return
    
    return 

def get_access_token() -> None:
    client_id = key.decrypt(open('./tokens/client_id.enc', 'rb').read()).decode()
    client_secret = key.decrypt(open('./tokens/client_secret.enc', 'rb').read()).decode()
    refresh_token = key.decrypt(open('./tokens/refresh_token.enc', 'rb').read()).decode()

    token_url = "https://api.schwabapi.com/v1/oauth/token"

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }

    headers = {'Authorization': f'Basic {base64.b64encode(bytes(f"{client_id}:{client_secret}", "utf-8")).decode("utf-8")}', 'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(token_url, headers=headers, data=data)
    tokens = response.json()

    if "access_token" in tokens:
        expires_times = json.load(open('./tokens/expires_times.json', 'r'))
        expires_times['access_token'] = (datetime.now() + timedelta(seconds=tokens['expires_in'])).strftime("%Y-%m-%d %H:%M:%S")
        json.dump(expires_times, open('./tokens/expires_times.json', 'w'))
        with open(f'./tokens/access_token.enc', 'wb') as f: f.write(key.encrypt(tokens['access_token'].encode()))
        print("Access token refreshed successfully.")
        return 
    else:
        print("Error refreshing token:", tokens)
        return 

def get_auth_token(manual_update_access_code = False, manual_update_refresh_code = False) -> str:
    expires_times = json.load(open('./tokens/expires_times.json', 'r'))
    access_token_expires_time = datetime.strptime(expires_times['access_token'], "%Y-%m-%d %H:%M:%S")
    refresh_token_expired_time = datetime.strptime(expires_times['refresh_token'], "%Y-%m-%d %H:%M:%S")
    if datetime.now() > refresh_token_expired_time - timedelta(days=2):
        warnings.warn(f"Refresh token will expire in 2 days, expire date is: {access_token_expires_time.strftime('%Y-%m-%d %H:%M:%S')}", UserWarning)
    if manual_update_access_code is False and manual_update_refresh_code is False:
        if datetime.now() > access_token_expires_time - timedelta(seconds=60):
            get_access_token()
    elif manual_update_access_code is True:
        get_access_token()
    elif manual_update_refresh_code is True:
        get_refresh_token()

    return key.decrypt(open('./tokens/access_token.enc', 'rb').read()).decode()
    
if __name__ == "__main__":
    # access_token, refresh_token = get_auth(manual_update_refresh=True)
    # get_access_token()
    # get_refresh_token()
    # expires_times = json.load(open('./tokens/expires_times.json', 'r'))
    # print(os.environ['SCHWAB_REFRESH_TOKEN'])
    # print(os.environ['SCHWAB_ACCESS_TOKEN'])
    # client_id = key.decrypt(open('./tokens/client_id.enc', 'rb').read()).decode()
    # token = key.decrypt(open('./tokens/refresh_token.enc', 'rb').read()).decode()
    token = get_auth_token(manual_update_refresh_code=True)