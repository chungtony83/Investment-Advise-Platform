import pandas as pd
from schwab_api import SchwabApi
from database_connect import connector
from logging_config import logger
import datetime
api = SchwabApi()
column_mapping = {
    'accountNumber': 'account_number',
    'securitiesAccount.accountNumber': 'account_number',
    'type': 'account_type',
    'roundTrips': 'round_trips',
    'isDayTrader': 'is_day_trader',
    'isClosingOnlyRestricted': 'is_closing_only_restricted',
    'pfcbFlag': 'pfcb_flag',
    'hashValue':'hash_value',
    'longQuantity': 'long_quantity',
    'shortQuantity': 'short_quantity',
    'averagePrice': 'average_price',
    'averageLongPrice': 'average_long_price',
    'taxLotAverageLongPrice': 'taxlot_average_long_price',
    'currentDayProfitLoss': 'current_day_profit_loss',
    'currentDayProfitLossPercentage': 'current_day_profit_loss_percentage',
    'longOpenProfitLoss': 'long_open_profit_loss',
    'marketValue': 'market_value',
    'maintenanceRequirement': 'maintenance_requirement',
    'previousSessionLongQuantity': 'previous_session_long_quantity',
    'currentDayCost': 'current_day_cost',
    'assetType': 'asset_type',
    'type': 'etf_type',
    'netChange': 'net_change',
    'maturityDate': 'maturity_date',
    'variableRate': 'variable_rate',
    
}

ods_db = connector(db_name='investment_advisor_ods')
def get_account_data():
    json_data_account = api.get_api_data('accounts')[0]
    json_data_account_numbers = api.get_api_data('account_numbers')[0]
    snapshot_id = ods_db.get_snapshot_id()
    
    # Securities Account
    df_securities_account = pd.json_normalize(json_data_account['securitiesAccount'])\
        [['accountNumber', 'type', 'roundTrips', 'isDayTrader', 'isClosingOnlyRestricted', 'pfcbFlag']]
    df_securities_account = df_securities_account.merge(pd.json_normalize(json_data_account_numbers), left_on='accountNumber', right_on='accountNumber')
    
    # Positions
    df_positions = pd.json_normalize(json_data_account,record_path=['securitiesAccount', 'positions'], meta=[['securitiesAccount', 'accountNumber']], max_level=0)
    df_positions = df_positions.rename(columns=column_mapping)
    # Instruments
    df_instruments = pd.json_normalize(df_positions['instrument'].tolist())
    df_instruments = df_instruments.rename(columns=column_mapping)
    
    df_positions['cusip'] = df_instruments['cusip']
    df_positions = df_positions.merge(ods_db.query_dataframe("SELECT id as instrument_id, cusip FROM instrument;"), on='cusip', how='left')
    df_positions = df_positions.merge(ods_db.query_dataframe("SELECT id as account_id, account_number FROM securities_account;"), left_on='account_number', right_on='account_number', how='left')
    df_positions['snapshot_id'] = snapshot_id
    
    return df_securities_account, df_instruments, df_positions

def save_to_database():
    df_securities_account, df_instruments, df_positions = get_account_data()
    
    ods_db.update_record('securities_account', df_securities_account.to_dict(orient='list'), df_securities_account[['account_number']].to_dict(orient='list'))
    
    ods_db.insert_dataframe(df_instruments, 'instrument', if_exists='append', chunksize=100)
    ods_db.insert_dataframe(df_positions, 'position', if_exists='append', chunksize=100)
    
if __name__ == "__main__":
    json_data_account = api.get_api_data('accounts')[0]
    json_data_account_numbers = api.get_api_data('account_numbers')[0]
    # df_securities_account = pd.json_normalize(json_data_account['securitiesAccount'])\
    #     [['accountNumber', 'type', 'roundTrips', 'isDayTrader', 'isClosingOnlyRestricted', 'pfcbFlag']]
    # df_securities_account = df_securities_account.merge(pd.json_normalize(json_data_account_numbers), left_on='accountNumber', right_on='accountNumber')
    
    # df_positions = pd.json_normalize(json_data_account,record_path=['securitiesAccount', 'positions'], meta=[['securitiesAccount', 'accountNumber']], max_level=0)
    # df_positions = df_positions.rename(columns=column_mapping)
    
    
    # df_instruments = pd.json_normalize(df_positions['instrument'].tolist())
    # df_instruments = df_instruments.rename(columns=column_mapping)
    df_securities_account, df_instruments, df_positions = get_account_data()
    


    
    