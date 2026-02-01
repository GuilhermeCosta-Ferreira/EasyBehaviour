PRAGMA foreign_keys = OFF;
BEGIN;

CREATE TABLE metrics_new (
  metric_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  unit TEXT NOT NULL DEFAULT '%',
  min_value INTEGER DEFAULT 0,
  max_value INTEGER DEFAULT 100,   -- ✅ nullable now (no NOT NULL)
  notes TEXT
);

INSERT INTO metrics_new (metric_id, name, unit, min_value, max_value, notes)
SELECT metric_id, name, unit, min_value, max_value, notes
FROM metrics;

DROP TABLE metrics;
ALTER TABLE metrics_new RENAME TO metrics;

COMMIT;
PRAGMA foreign_keys = ON;
