BEGIN;

INSERT INTO metrics (name, unit, min_value, max_value)
VALUES
    ('Trial Nº', '#', 1, NULL),
    ('Nr of Accurate Steps', '#', 0, NULL),
    ('Nr of Non-Accurate Steps', '#', 0, NULL),
    ('Nr of Slips', '#', 0, NULL),
    ('Trial Duration', 's', 0, NULL),
    ('Nr of Trials', '#', 0, NULL),
    ('Nr of Hits', '#', 0, NULL);
COMMIT;
