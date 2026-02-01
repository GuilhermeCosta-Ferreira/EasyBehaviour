PRAGMA foreign_keys = OFF;
BEGIN;

-- 1) Create the new table with the desired schema
CREATE TABLE timepoints_new (
  timepoint_id INTEGER PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,
  label TEXT,
  event_type TEXT,
  weeks_after_event INTEGER,   -- <-- now explicitly INTEGER
  notes TEXT
);

-- 2) Copy data across
INSERT INTO timepoints_new (timepoint_id, code, label, event_type, weeks_after_event, notes)
SELECT timepoint_id, code, label, event_type, weeks_after_event, notes
FROM timepoints;

-- 3) Swap tables
DROP TABLE timepoints;
ALTER TABLE timepoints_new RENAME TO timepoints;

COMMIT;
PRAGMA foreign_keys = ON;
