CREATE TYPE account_type_enum AS ENUM ('CASH', 'MARGIN');

CREATE TYPE balance_type_enum AS ENUM ('initial', 'current', 'projected');

CREATE TABLE IF NOT EXISTS securities_account (
    account_number INTEGER PRIMARY KEY,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    account_type account_type_enum NOT NULL,
    round_trips INTEGER,
    is_day_trader BOOLEAN DEFAULT FALSE,
    is_closing_only_restricted BOOLEAN DEFAULT FALSE,
    pfcb_flag BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS account_balances (
    account_number INTEGER NOT NULL REFERENCES securities_account(account_number),
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    balance_type balance_type_enum NOT NULL,
    cash_available_for_trading NUMERIC(10,2),
    cash_available_for_withdrawal NUMERIC(10,2),
    cash_call NUMERIC(10,2),
    long_non_marginable_market_value NUMERIC(10,2),
    total_cash NUMERIC(10,2),
    cash_debit_call_value NUMERIC(10,2),
    unsettled_cash NUMERIC(10,2),
    accrued_interest NUMERIC(10,2),
    cash_balance NUMERIC(10,2),
    bond_value NUMERIC(10,2),
    cash_receipts NUMERIC(10,2),
    liquidation_value NUMERIC(10,2),
    long_option_market_value NUMERIC(10,2),
    long_stock_value NUMERIC(10,2),
    money_market_fund NUMERIC(10,2),
    mutual_fund_value NUMERIC(10,2),
    short_option_market_value NUMERIC(10,2),
    short_stock_value NUMERIC(10,2),
    is_in_call NUMERIC(10,2),
    pending_deposits NUMERIC(10,2),
    account_value NUMERIC(10,2),
    PRIMARY KEY (account_number, update_time, balance_type)
);

