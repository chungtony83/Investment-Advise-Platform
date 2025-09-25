import requests
import os
from schwab_auth import SchwabAuth
from logging_config import logger
import pandas as pd  # Ensure pandas is imported and 'pd' is not redefined elsewhere
import datetime
import sqlalchemy as sa
from database_connect import connector


class schwab_api_market:
    def __init__(self):
        self.db_ods = connector(schema='ods')
        self.access_token = SchwabAuth().get_token()
        self.server_link = 'https://api.schwabapi.com/marketdata/v1'
    
    def get_quotes(self, symbol: str):
        response = requests.get(f'{self.server_link}/quotes', 
                                headers={'Authorization': f'Bearer {self.access_token}'},
                                params={'symbols': symbol})

        return response.json()

    def get_instruments(self, symbol: str|list, projection: str='symbol-search', chunksize: int=500) -> pd.DataFrame:
        if chunksize > 500:
            logger.warning("Schwab API limits the number of symbols per request. Using a chunksize of 500.")
            chunksize = 500
        symbols = symbol if isinstance(symbol, list) else [symbol]
        df = pd.DataFrame()  # Make sure 'pd' is pandas and not a local variable
        for i in range(0, len(symbols), chunksize):
            chunk = ','.join(symbols[i:i + chunksize])
            response = requests.get(f'{self.server_link}/instruments', 
                                    headers={'Authorization': f'Bearer {self.access_token}'},
                                    params={'symbol': chunk, 'projection': projection})
            if response.status_code != 200:
                logger.error(f"Error fetching instruments: {response.status_code} - {response.text}")
                return pd.DataFrame()  # Make sure 'pd' is pandas and not a local variable
            df_chunk = pd.json_normalize(response.json()['instruments'])
            df = pd.concat([df, df_chunk], ignore_index=True)
        return df

if __name__ == "__main__":
    api = schwab_api_market()
    df = api.get_instruments(symbol='AAPL', projection='symbol-search')
    print(df)
