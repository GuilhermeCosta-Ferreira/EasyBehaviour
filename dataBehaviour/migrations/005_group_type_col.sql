PRAGMA foreign_keys = OFF;
BEGIN;

CREATE TABLE IF NOT EXISTS groups_new (
  group_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  study_type TEXT, -- like injury or ablation
  was_treated INTEGER, -- 0: no 1: yes
  was_injured INTEGER,
  nr_of_cages INTEGER NOT NULL, -- like 1 cage, 2 cages, metrics
  nr_of_mice INTEGER NOT NULL, -- initial number of mice for first aqquisition
  notes TEXT
);

INSERT INTO groups_new (group_id, name, nr_of_cages, nr_of_mice, notes)
SELECT group_id, name, nr_of_cages, nr_of_mice, notes
FROM groups;

DROP TABLE groups;
ALTER TABLE groups_new RENAME TO groups;

COMMIT;
PRAGMA foreign_keys = ON;
