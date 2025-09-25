-- ===== Snapshots (track when you pulled the data)
CREATE TABLE ods.snapshot (
  id BIGSERIAL PRIMARY KEY,
  date_time TIMESTAMPTZ NOT NULL DEFAULT now()
);
