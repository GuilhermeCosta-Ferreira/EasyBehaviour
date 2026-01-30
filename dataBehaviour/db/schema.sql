BEGIN;
CREATE TABLE IF NOT EXISTS behaviors (
  behavior_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE          -- 'reaching', 'ladder', ...
);

CREATE TABLE IF NOT EXISTS groups (
  group_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  nr_of_cages INTEGER NOT NULL, -- like 1 cage, 2 cages, metrics
  nr_of_mice INTEGER NOT NULL, -- initial number of mice for first aqquisition
  notes TEXT
);

CREATE TABLE IF NOT EXISTS mice (
  mouse_id INTEGER PRIMARY KEY,  -- unique for the all database
  group_id INTEGER NOT NULL REFERENCES groups(group_id),
  mouse_number INTEGER NOT NULL,
  cage_letter TEXT NOT NULL
      CHECK (cage_letter IN ('A','B','C')),
  dominant_hand TEXT NOT NULL DEFAULT 'unknown'
    CHECK (dominant_hand IN ('unknown', 'left', 'right')),
  to_remove INTEGER NOT NULL DEFAULT 0 CHECK (to_remove IN (0,1)),
  notes TEXT,
  UNIQUE (group_id, mouse_number)
);

CREATE TABLE IF NOT EXISTS timepoints (
  timepoint_id INTEGER PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,              -- e.g. 'baseline', 'post_ablation', 'post_injury_w1'
  label TEXT,
  event_type TEXT, -- "injury", "ablation", "unspecified"
  weeks_after_event, -- -1 (baselines); 1 (week 1), etc
  notes TEXT
);

CREATE TABLE IF NOT EXISTS metrics (
  metric_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,              -- e.g. 'accuracy', 'distance'
  unit TEXT NOT NULL DEFAULT "%",
  min_value INTEGER NOT NULL DEFAULT 0,
  max_value INTEGER NOT NULL DEFAULT 100,
  notes TEXT
);

-- This is the rulebook: which metrics are allowed for which behavior
CREATE TABLE IF NOT EXISTS behavior_metrics (
  behavior_id INTEGER NOT NULL REFERENCES behaviors(behavior_id),
  metric_id   INTEGER NOT NULL REFERENCES metrics(metric_id),
  PRIMARY KEY (behavior_id, metric_id)
);


CREATE TABLE IF NOT EXISTS observations (
  mouse_id INTEGER NOT NULL REFERENCES mice(mouse_id),
  timepoint_id INTEGER NOT NULL REFERENCES timepoints(timepoint_id),
  behavior_id INTEGER NOT NULL REFERENCES behaviors(behavior_id),
  metric_id INTEGER NOT NULL REFERENCES metrics(metric_id),
  value REAL NOT NULL,
  notes TEXT,

  PRIMARY KEY (mouse_id, timepoint_id, behavior_id, metric_id),

  -- This enforces: metric must be allowed for that behavior
  FOREIGN KEY (behavior_id, metric_id)
    REFERENCES behavior_metrics(behavior_id, metric_id)
);

-- allows for faster queries
CREATE INDEX idx_obs_timepoint ON observations(timepoint_id);
CREATE INDEX idx_obs_metric ON observations(metric_id);
CREATE INDEX idx_mice_group ON mice(group_id);

COMMIT;
