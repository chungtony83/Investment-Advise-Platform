import requests
import os
from schwab_auth import SchwabAuth
from logging_config import logger
import pandas as pd
import datetime
import sqlalchemy as sa

class schwab_api_market:
    def __init__(self):
        self.access_token = SchwabAuth().get_token()
        self.server_link = 'https://api.schwabapi.com/marketdata/v1'
    
    def get_quotes(self, symbol: str):
        response = requests.get(f'{self.server_link}/quotes', 
                                headers={'Authorization': f'Bearer {self.access_token}'},
                                params={'symbols': symbol})

        return response.json()

    def get_instruments(self, symbol: str):
        response = requests.get(f'{self.server_link}/instruments', 
                                headers={'Authorization': f'Bearer {self.access_token}'},
                                params={'symbols': symbol})

        return response.json()

if __name__ == "__main__":
    api = schwab_api_market()
    df = api.get_quotes('$DJI')
    print(df)