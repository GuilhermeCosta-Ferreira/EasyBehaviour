BEGIN;

INSERT INTO behavior_metrics (behavior_id, metric_id)
VALUES
    (1, 6), -- reaching
    (1, 7),
    (2, 1), -- ladder
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5);

COMMIT;
