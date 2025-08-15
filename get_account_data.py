
import requests
import os
from schwab_auth import SchwabAuth
from logging_config import logger
import pandas as pd
import datetime
import sqlalchemy as sa

class SchwabApi:
    def __init__(self):
        self.access_token = SchwabAuth().get_token()
        self.account_number_hash = requests.get('https://api.schwabapi.com/trader/v1/accounts/accountNumbers', headers={'Authorization': f'Bearer {self.access_token}'}).json()[0]['hashValue']
    
    def get_account_data(self):
        response = requests.get(f'https://api.schwabapi.com/trader/v1/accounts/{self.account_number_hash}', 
                                headers={'Authorization': f'Bearer {self.access_token}'}).json()
        df = pd.json_normalize(response['securitiesAccount'], sep='_').drop(columns=['positions'])
        df = df.rename(columns={
        'type': 'type',
        'accountNumber': 'account_number',
        'roundTrips': 'round_trips',
        'isDayTrader': 'is_day_trader',
        'isClosingOnlyRestricted': 'is_closing_only_restricted',
        'pfcbFlag': 'pfcb_flag'
        })
        df = df[['type', 'account_number', 'round_trips', 'is_day_trader', 'is_closing_only_restricted', 'pfcb_flag']]
        return df
    
    def get_account_balances(self):
        response = requests.get(f'https://api.schwabapi.com/trader/v1/accounts/{self.account_number_hash}', 
                                headers={'Authorization': f'Bearer {self.access_token}'}).json()
        df = pd.json_normalize(response['securitiesAccount'], sep='_')
        # df = pd.json_normalize(response['securitiesAccount']['positions'], sep='_')
        df = df.melt(id_vars=['accountNumber'], var_name='variable', value_name='value')
        df[['variable', 'sub_variable']] = df['variable'].str.split('_', expand=True)
        df['variable'] = df['variable'].replace({'initialBalances': 'initial', 'currentBalances': 'current', 'projectedBalances': 'projected'})
        df['sub_variable'] = df['sub_variable'].replace(
            {'accruedInterest': 'accrued_interest',
            'cashBalance': 'cash_balance',
            'bondValue': 'bond_value',
            'cashReceipts': 'cash_receipts',
            'liquidationValue': 'liquidation_value',
            'longOptionMarketValue': 'long_option_market_value',
            'longStockValue': 'long_stock_value',
            'moneyMarketFund': 'money_market_fund',
            'mutualFundValue': 'mutual_fund_value',
            'shortOptionMarketValue': 'short_option_market_value',
            'shortStockValue': 'short_stock_value',
            'isInCall': 'is_in_call',
            'unsettledCash': 'unsettled_cash',
            'cashDebitCallValue': 'cash_debit_call_value',
            'pendingDeposits': 'pending_deposits',
            'accountValue': 'account_value',
            'longMarketValue': 'long_market_value',
            'savings': 'savings',
            'shortMarketValue': 'short_market_value',
            'cashCall': 'cash_call',
            'longNonMarginableMarketValue': 'long_non_marginable_market_value',
            'totalCash': 'total_cash',
            'cashAvailableForTrading': 'cash_available_for_trading',
            'cashAvailableForWithdrawal': 'cash_available_for_withdrawal'})
        df = df.loc[df['sub_variable'].notnull()]
        df = df.pivot(index=['accountNumber', 'variable'], columns='sub_variable', values='value').reset_index()
        return df
    def get_account_orders(self, start_date:str, end_date:str):
        # yyyy-MM-dd'T'HH:mm:ss.SSSZ
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        response = requests.get(f'https://api.schwabapi.com/trader/v1/accounts/{self.account_number_hash}/orders', 
                                headers={'Authorization': f'Bearer {self.access_token}'},
                                params= {'fromEnteredTime': start_date,
                                         'toEnteredTime': end_date,
                                         'maxResults': 3000})
        return response.json()
    
    def get_account_transactions(self, start_date:str, end_date:str) -> pd.DataFrame:
        # yyyy-MM-dd'T'HH:mm:ss.SSSZ
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        response = requests.get(f'https://api.schwabapi.com/trader/v1/accounts/{self.account_number_hash}/transactions', 
                                headers={'Authorization': f'Bearer {self.access_token}'},
                                params= {'startDate': start_date,
                                         'endDate': end_date,
                                         'types': 'TRADE'})
        result = pd.json_normalize(response.json(), 
                           record_path=['transferItems'], 
                           meta=['activityId', 'time', 'accountNumber', 'type', 'tradeDate', 'positionId', 'orderId', 'netAmount'],
                           errors='ignore')
        result = result[['activityId', 'time', 'accountNumber', 'type', 'tradeDate', 'positionId', 'orderId', 'netAmount', 'symbol', 'quantity', 'price', 'commission', 'description']]
        return result 

if __name__ == '__main__':
    api = SchwabApi()
    df = api.get_account_balances()

       
    df = df.melt(id_vars=['accountNumber'], var_name='variable', value_name='value')
    df[['variable', 'sub_variable']] = df['variable'].str.split('_', expand=True)
    df['variable'] = df['variable'].replace({'initialBalances': 'initial', 'currentBalances': 'current', 'projectedBalances': 'projected'})
    df['sub_variable'] = df['sub_variable'].replace(
        {'accruedInterest': 'accrued_interest',
         'cashBalance': 'cash_balance',
         'bondValue': 'bond_value',
         'cashReceipts': 'cash_receipts',
         'liquidationValue': 'liquidation_value',
         'longOptionMarketValue': 'long_option_market_value',
         'longStockValue': 'long_stock_value',
         'moneyMarketFund': 'money_market_fund',
         'mutualFundValue': 'mutual_fund_value',
         'shortOptionMarketValue': 'short_option_market_value',
         'shortStockValue': 'short_stock_value',
         'isInCall': 'is_in_call',
         'unsettledCash': 'unsettled_cash',
         'cashDebitCallValue': 'cash_debit_call_value',
         'pendingDeposits': 'pending_deposits',
         'accountValue': 'account_value',
         'longMarketValue': 'long_market_value',
         'savings': 'savings',
         'shortMarketValue': 'short_market_value',
         'cashCall': 'cash_call',
         'longNonMarginableMarketValue': 'long_non_marginable_market_value',
         'totalCash': 'total_cash',
         'cashAvailableForTrading': 'cash_available_for_trading',
         'cashAvailableForWithdrawal': 'cash_available_for_withdrawal'})
    df = df.loc[df['sub_variable'].notnull()]
    df = df.pivot(index=['accountNumber', 'variable'], columns='sub_variable', values='value').reset_index()
    # df = pd.read_json(response.json(), orient='records')
    # # df.columns = df.columns.str.split('.').str[-1]
    # print(df)
    # df = api.get_account_transactions(start_date='2025-01-27', end_date='2025-03-31')
    # # df = pd.json_normalize(response, max_level=None)
    # df_expanded = pd.json_normalize(df['transferItems'], )

    