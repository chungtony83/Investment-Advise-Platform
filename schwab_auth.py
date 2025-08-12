import requests
import os
import base64
import urllib.parse
from datetime import datetime, timedelta
import warnings
import dotenv

class SchwabAuth:
    def __init__(self, redirect_uri = "https://127.0.0.1"):
        dotenv.load_dotenv()
        self.client_id = os.getenv("SCHWAB_CLIENT_ID")
        self.client_secret = os.getenv("SCHWAB_CLIENT_SECRET")
        self.refresh_token = os.getenv("SCHWAB_REFRESH_TOKEN")
        self.access_token = os.getenv("SCHWAB_ACCESS_TOKEN")
        self.redirect_uri = redirect_uri

    def update_client_id_secret(self, update=False) -> None:
        client_id = input("Enter your Schwab Client ID: ").strip()
        client_secret = input("Enter your Schwab Client Secret: ").strip()
        dotenv.set_key(dotenv.find_dotenv(), "SCHWAB_CLIENT_ID", client_id)
        dotenv.set_key(dotenv.find_dotenv(), "SCHWAB_CLIENT_SECRET", client_secret)
        return 

    def update_refresh_token(self) -> None:

        # 1. Construct the authorization URL with response_type=code
        auth_url = f"https://api.schwabapi.com/v1/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}"

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
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        headers = {
            'Authorization': f'Basic {base64.b64encode(bytes(f"{self.client_id}:{self.client_secret}", "utf-8")).decode("utf-8")}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(token_url, data=data, headers=headers)
        tokens = response.json()

        # 5. Extract and print tokens
        if 'access_token' in tokens:
            access_token_expire = (datetime.now() + timedelta(seconds=tokens['expires_in'])).strftime("%Y-%m-%d %H:%M:%S")
            refresh_token_expire =  (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
            dotenv.set_key(dotenv.find_dotenv(), "SCHWAB_ACCESS_TOKEN", tokens['access_token'])
            dotenv.set_key(dotenv.find_dotenv(), "SCHWAB_REFRESH_TOKEN", tokens['refresh_token'])
            dotenv.set_key(dotenv.find_dotenv(), "SCHWAB_ACCESS_TOKEN_EXPIRES_TIMES", access_token_expire)
            dotenv.set_key(dotenv.find_dotenv(), "SCHWAB_REFRESH_TOKEN_EXPIRES_TIMES", refresh_token_expire)
            print("Access token & Refresh token updated successfully.")
        else:
            print("Error exchanging authorization code:", tokens)
            return
        
        return 

    def update_access_token(self,) -> None:

        token_url = "https://api.schwabapi.com/v1/oauth/token"

        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        headers = {
            'Authorization': f'Basic {base64.b64encode(bytes(f"{self.client_id}:{self.client_secret}", "utf-8")).decode("utf-8")}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(token_url, headers=headers, data=data)
        tokens = response.json()

        if "access_token" in tokens:
            access_token_expire = (datetime.now() + timedelta(seconds=tokens['expires_in'])).strftime("%Y-%m-%d %H:%M:%S")
            dotenv.set_key(dotenv.find_dotenv(), "SCHWAB_ACCESS_TOKEN", tokens['access_token'])
            dotenv.set_key(dotenv.find_dotenv(), "SCHWAB_ACCESS_TOKEN_EXPIRES_TIMES", access_token_expire)
            print("Access token refreshed successfully.")
            return 
        else:
            print("Error refreshing token:", tokens)
            return 

    def get_latest_access_token(self):
        """
        Refreshes tokens if expired and returns the latest access token.
        """

        if not self.client_id or not self.client_secret:
            print("Client ID or Secret missing.")
            self.update_client_id_secret()
        if not self.access_token or not access_token_expire:
            self.update_access_token()
        if not self.refresh_token or not refresh_token_expire:
            self.update_refresh_token()

        if access_token_expire:
            expire_time = datetime.strptime(access_token_expire, "%Y-%m-%d %H:%M:%S")
            if now > expire_time - timedelta(seconds=60):
                self.update_access_token()
        if refresh_token_expire:
            expire_time = datetime.strptime(refresh_token_expire, "%Y-%m-%d %H:%M:%S")
            if now > expire_time:
                print("Refresh token expired. Re-authenticate.")
                self.update_refresh_token()
                return None
            elif now > expire_time - timedelta(days=2):
                warnings.warn(f"Refresh token expires soon: {expire_time}", UserWarning)
        dotenv.load_dotenv()
        return os.getenv("SCHWAB_ACCESS_TOKEN")

if __name__ == "__main__":
    # Example usage
    auth = SchwabAuth()
    # Uncomment below to manually refresh tokens
    # auth.get_refresh_token()
    # auth.get_access_token()