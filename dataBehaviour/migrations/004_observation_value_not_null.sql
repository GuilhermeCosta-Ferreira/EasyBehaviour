PRAGMA foreign_keys = OFF;
BEGIN;

CREATE TABLE IF NOT EXISTS observations_new (
  mouse_id INTEGER NOT NULL REFERENCES mice(mouse_id),
  timepoint_id INTEGER NOT NULL REFERENCES timepoints(timepoint_id),
  behavior_id INTEGER NOT NULL REFERENCES behaviors(behavior_id),
  metric_id INTEGER NOT NULL REFERENCES metrics(metric_id),
  value REAL,
  notes TEXT,

  PRIMARY KEY (mouse_id, timepoint_id, behavior_id, metric_id),

  -- This enforces: metric must be allowed for that behavior
  FOREIGN KEY (behavior_id, metric_id)
    REFERENCES behavior_metrics(behavior_id, metric_id)
);

INSERT INTO observations_new (mouse_id, timepoint_id, behavior_id, metric_id, value, notes)
SELECT mouse_id, timepoint_id, behavior_id, metric_id, value, notes
FROM observations;

DROP TABLE observations;
ALTER TABLE observations_new RENAME TO observations;

COMMIT;
PRAGMA foreign_keys = ON;
