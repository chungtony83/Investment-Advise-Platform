CREATE TABLE ods.price_history (
    instrument_id BIGINT NOT NULL REFERENCES ods.instrument(id) ON DELETE CASCADE,
    date_time TIMESTAMP NOT NULL,
    open NUMERIC(18,6) NOT NULL,
    high NUMERIC(18,6) NOT NULL,
    low NUMERIC(18,6) NOT NULL,
    close NUMERIC(18,6) NOT NULL,
    volume BIGINT NOT NULL,
    fetch_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (instrument_id, date_time)
)