import pandas as pd
from get_market_data import schwab_api_market
from database_connect import connector
from logging_config import logger
from database_connect import connector

def stock_list_market_data():
    db_ods = connector(schema='ods')
    db_dwd = connector(schema='dwd')
    
    # Fetch watch list symbols from the data warehouse
    watch_list_df = db_dwd.query_dataframe("SELECT symbol FROM watch_list;")
    if watch_list_df.empty:
        logger.warning("Watch list is empty. No symbols to fetch market data for.")
        return
    
    symbols = watch_list_df['symbol'].tolist()
    
    api = schwab_api_market()
    market_data_df = api.get_instruments(symbol=symbols, projection='symbol-search')
    
    if market_data_df.empty:
        logger.error("Failed to fetch market data from Schwab API.")
        return
    
    # Insert the fetched market data into the ODS schema
    # db_ods.insert_dataframe(market_data_df, table_name='market_data', if_exists='replace', chunksize=100)
    # logger.info("Market data updated successfully.")
    return market_data_df

if __name__ == "__main__":
    df = watch_list_market_data()
    print(df)