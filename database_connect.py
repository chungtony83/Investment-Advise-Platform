import pandas as pd
from sqlalchemy import create_engine, text
import os
import dotenv
from logging_config import logger
from typing import Literal

dotenv.load_dotenv()
dotenv_path = dotenv.find_dotenv()

class connector:
    def __init__(self, user=os.getenv("POSTGRES_DB_USERNAME"), password=os.getenv("POSTGRES_DB_PASSWORD"), address='localhost', port=5432, db_name='investment_advisor_ods'):
        if not user:
            user = input("Enter your PostgreSQL username: ").strip()
            dotenv.set_key(dotenv_path, "POSTGRES_DB_USERNAME", user)
        if not password:
            password = input("Enter your PostgreSQL password: ").strip()
            dotenv.set_key(dotenv_path, "POSTGRES_DB_PASSWORD", password)
        self.engine = create_engine(f'postgresql://{user}:{password}@{address}:{port}/{db_name}')
        self.connection = self.engine.connect()
        pass

    def query_data(self, query: str):
        cursor = self.connection.execute(text(query))
        result = cursor.fetchall()
        return result
    
    def query_dataframe(self, query: str) -> pd.DataFrame:
        """Executes a SQL query and returns the result as a DataFrame."""
        try:
            df = pd.read_sql_query(query, self.connection)
            return df
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return pd.DataFrame()
    
    def query_columns(self, table_name: str) -> list:
        """Returns a list of column names for the specified table."""
        try:
            query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';"
            df = pd.read_sql_query(query, self.connection)
            return df['column_name'].tolist()
        except Exception as e:
            logger.error(f"Error fetching columns for table '{table_name}': {e}")
            return []
    
    def insert_dataframe(self, df: pd.DataFrame, table_name: str, if_exists: Literal['fail', 'replace', 'append'] = "append", chunksize: int|None = None) -> None:
        """
        Inserts a DataFrame into the specified SQL table.
        Supports chunked insertion for large DataFrames via the chunksize parameter.
        """
        try:
            if chunksize is not None:
                df.to_sql(table_name, self.engine, if_exists=if_exists, index=False, chunksize=chunksize)
            else:
                df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            logger.info(f"Successfully inserted DataFrame into table '{table_name}'.")
        except Exception as e:
            logger.error(f"Error inserting DataFrame into table '{table_name}': {e}")

    def insert_record(self, table_name: str, record: dict) -> None:
        """
        Inserts a single record (as a dict) into the specified SQL table.
        """
        try:
            df = pd.DataFrame([record])
            self.insert_dataframe(df, table_name)
            logger.info(f"Successfully inserted record into table '{table_name}'.")
        except Exception as e:
            logger.error(f"Error inserting record into table '{table_name}': {e}")
    
    def get_snapshot_id(self,) -> int:
        cursor = self.connection.execute(text("INSERT INTO snapshot DEFAULT VALUES RETURNING id;"))
        row = cursor.fetchone()
        if row is None:
            logger.error("No snapshot ID returned from database.")
            return -1
        return row[0]
        
if __name__ == "__main__":
    db = connector()
    query = "SELECT * FROM your_table_name LIMIT 10;"
    df = db.query_dataframe(query)
    print(df.head())