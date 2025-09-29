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

    def get_instruments(self, symbol: str|list, chunksize: int=500) -> pd.DataFrame:
        if chunksize > 500:
            logger.warning("Schwab API limits the number of symbols per request. Using a chunksize of 500.")
            chunksize = 500
        symbols = symbol if isinstance(symbol, list) else [symbol]
        df = pd.DataFrame()  # Make sure 'pd' is pandas and not a local variable
        for i in range(0, len(symbols), chunksize):
            chunk = ','.join(symbols[i:i + chunksize])
            response = requests.get(f'{self.server_link}/instruments', 
                                    headers={'Authorization': f'Bearer {self.access_token}'},
                                    params={'symbol': chunk, 'projection': 'symbol-search'})
            if response.status_code != 200:
                logger.error(f"Error fetching instruments: {response.status_code} - {response.text}")
                return pd.DataFrame()  # Make sure 'pd' is pandas and not a local variable
            df_chunk = pd.json_normalize(response.json()['instruments'])
            df = pd.concat([df, df_chunk], ignore_index=True)
        return df
    
    def get_instrument_fundamental(self, symbol: str|list, chunksize: int=500):
        if chunksize > 500:
            logger.warning("Schwab API limits the number of symbols per request. Using a chunksize of 500.")
            chunksize = 500
        symbols = symbol if isinstance(symbol, list) else [symbol]
        df = pd.DataFrame()  # Make sure 'pd' is pandas and not a local variable
        for i in range(0, len(symbols), chunksize):
            chunk = ','.join(symbols[i:i + chunksize])
            response = requests.get(f'{self.server_link}/instruments', 
                                    headers={'Authorization': f'Bearer {self.access_token}'},
                                    params={'symbol': chunk, 'projection': 'fundamental'})
            if response.status_code != 200:
                logger.error(f"Error fetching instrument fundamentals: {response.status_code} - {response.text}")
                return pd.DataFrame()  # Make sure 'pd' is pandas and not a local variable
            data = response.json()
            instruments = data.get('instruments', [])
            if not instruments:
                logger.warning(f"No instruments found in response for symbols: {chunk}")
                continue
            fundamentals = [inst.get('fundamental', {}) for inst in instruments if 'fundamental' in inst]
            if not fundamentals:
                logger.warning(f"No fundamental data found for symbols: {chunk}")
                continue
            df_chunk = pd.json_normalize(fundamentals)
            df = pd.concat([df, df_chunk], ignore_index=True)
        return df

    def get_price_history(
            self, 
            symbol: str, 
            period_type: str, 
            period: str, 
            frequency_type: str, 
            frequency: str,
            start_date: str,
            end_date: str,
            need_extended_hours_data: bool=True,
            need_previous_close: bool=True
            ):
        response = requests.get(f'{self.server_link}/pricehistory',
                                headers={'Authorization': f'Bearer {self.access_token}'},
                                params={'symbol': symbol, 
                                        # 'periodType': period_type, 
                                        # 'period': period, 
                                        # 'frequencyType': frequency_type, 
                                        # 'frequency': frequency,
                                        # 'startDate': start_date,
                                        # 'endDate': end_date,
                                        'needExtendedHoursData': need_extended_hours_data,
                                        'needPreviousClose': need_previous_close
                                        })
        if response.status_code != 200:
            logger.error(f"Error fetching price history: {response.status_code} - {response.text}")
            return pd.DataFrame()  # Make sure 'pd' is pandas and not a local variable
        # df_chunk = pd.json_normalize(response.json()['priceHistory'])
        # df = pd.concat([df, df_chunk], ignore_index=True)
        return response.json()
 
if __name__ == "__main__":
    api = schwab_api_market()
    # df = api.get_instrument_fundamental(symbol=['AAPL', 'TSLA', 'MSFT'])
    df = api.get_price_history(symbol='AAPL', period_type='month', period='1', frequency_type='daily', frequency='1', start_date='2025-01-01', end_date='2025-01-31', need_extended_hours_data=True, need_previous_close=True)
    print(df)
