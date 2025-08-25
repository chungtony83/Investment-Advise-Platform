import pandas as pd
from schwab_api import SchwabApi
from database_connect import connector
from logging_config import logger
import datetime
api = SchwabApi()
column_mapping = {
    'accountNumber': 'account_number',
    'type': 'account_type',
    'roundTrips': 'round_trips',
    'isDayTrader': 'is_day_trader',
    'isClosingOnlyRestricted': 'is_closing_only_restricted',
    'pfcbFlag': 'pfcb_flag',
    'hashValue':'hash_value'
}

def data_securities_account():
    json_data = api.get_api_data('accounts')[0]
    df = pd.json_normalize(json_data['securitiesAccount'])
    
if __name__ == "__main__":
    api = SchwabApi()
    json_data = api.get_api_data('accounts')[0]
    df = pd.json_normalize(json_data['securitiesAccount'])\
        [['accountNumber', 'type', 'roundTrips', 'isDayTrader', 'isClosingOnlyRestricted', 'pfcbFlag']]
    df = df.merge(pd.json_normalize(api.get_api_data('account_numbers')[0]), left_on='accountNumber', right_on='accountNumber')


    
    