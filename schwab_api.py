import requests
import os
from schwab_auth import SchwabAuth
from logging_config import logger
import pandas as pd
import datetime
import sqlalchemy as sa
from typing import List

class SchwabApi:
    def __init__(self, ):
        self.access_token = SchwabAuth().get_token()
        self.account_number_hash = '' ## Got this from database
        self.server_mapping = {
        'trader' : 'https://api.schwabapi.com/trader/v1',
        'market' : 'https://api.schwabapi.com/marketdata/v1'
        }
        self.url_mapping = {
            'account_numbers': f"{self.server_mapping['trader']}/accounts/accountNumbers",
            'accounts': f"{self.server_mapping['trader']}/accounts/{self.account_number_hash}",
            'orders': f"{self.server_mapping['trader']}/accounts/{self.account_number_hash}/orders",
            'transactions': f"{self.server_mapping['trader']}/accounts/{self.account_number_hash}/transactions",
        }
        self.url_keys = self.url_mapping.keys()
        
        self.default_params = {
            'accounts': {'fields': 'positions'},
            'orders': {''}
        }

    def get_api_data(self, endpoint:str, params:dict = {}) -> dict:
        if endpoint not in self.url_keys:
            logger.error(f"Invalid endpoint: {endpoint}. Available endpoints: {list(self.url_keys)}")
            raise ValueError(f"Invalid endpoint: {endpoint}. Available endpoints: {list(self.url_keys)}")
        
        url = self.url_mapping[endpoint]
        headers = {"Authorization": f"Bearer {self.access_token}"}
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        return r.json()

        
if __name__ == '__main__':
    api = SchwabApi()
    data = api.get_api_data('accounts', params = {'fields':'positions'})
    print(data)
