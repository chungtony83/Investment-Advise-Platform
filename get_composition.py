import yfinance as yf
import pandas as pd

# Example: SPY ETF (S&P 500)
spy = yf.Ticker("SPY").get_funds_data()

spy.equity_holdings

# spy.funds_data