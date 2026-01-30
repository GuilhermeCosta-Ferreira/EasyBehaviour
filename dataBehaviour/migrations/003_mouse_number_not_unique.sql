PRAGMA foreign_keys = OFF;
BEGIN;

CREATE TABLE IF NOT EXISTS mice_new (
  mouse_id INTEGER PRIMARY KEY,  -- unique for the all database
  group_id INTEGER NOT NULL REFERENCES groups(group_id),
  mouse_number INTEGER NOT NULL,
  cage_letter TEXT NOT NULL
      CHECK (cage_letter IN ('A','B','C')),
  dominant_hand TEXT NOT NULL DEFAULT 'unknown'
    CHECK (dominant_hand IN ('unknown', 'left', 'right')),
  to_remove INTEGER NOT NULL DEFAULT 0 CHECK (to_remove IN (0,1)),
  notes TEXT
);

INSERT INTO mice_new (mouse_id, group_id, mouse_number, cage_letter, dominant_hand, to_remove, notes)
SELECT mouse_id, group_id, mouse_number, cage_letter, dominant_hand, to_remove, notes
FROM mice;

DROP TABLE mice;
ALTER TABLE mice_new RENAME TO mice;

COMMIT;
PRAGMA foreign_keys = ON;
