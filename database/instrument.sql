CREATE TYPE asset_type_enum AS ENUM ('BOND', 'EQUITY', 'ETF', 'EXTENDED', 'FOREX', 'FUTURE', 'FUTURE_OPTION', 'FUNDAMENTAL', 'INDEX', 'INDICATOR', 'MUTUAL_FUND', 'OPTION', 'UNKNOWN');

-- ====== INSTRUMENTS (one row per symbol/asset_type)
CREATE TABLE ods.instrument (
    id BIGSERIAL PRIMARY KEY,
    cusip TEXT,
    symbol TEXT,
    description TEXT,
    exchange TEXT,
    assetType asset_type_enum,
    type asset_type_enum,
    snapshot_id BIGINT NOT NULL REFERENCES ods.snapshot(id) ON DELETE CASCADE
);
