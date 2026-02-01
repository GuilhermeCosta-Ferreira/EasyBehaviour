BEGIN;

INSERT INTO observations (mouse_id, timepoint_id, behavior_id, metric_id, value)
VALUES
    (9, 2, 2, 1, 3), -- adding for g46 A1 ladder one row
    (9, 2, 2, 2, 3),
    (9, 2, 2, 3, 2),
    (9, 2, 2, 4, 15),
    (9, 2, 2, 5, NULL);

COMMIT;
