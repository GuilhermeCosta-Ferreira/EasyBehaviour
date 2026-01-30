BEGIN;

INSERT INTO mice (group_id, mouse_number, cage_letter, dominant_hand, to_remove)
VALUES
    (44, 1, 'A', 'unknown', 1), -- vsx2 ablated
    (44, 2, 'A', 'unknown', 0),
    (44, 3, 'A', 'unknown', 0),
    (44, 4, 'A', 'unknown', 0),
    (44, 5, 'A', 'unknown', 0),
    (44, 1, 'B', 'unknown', 0),
    (44, 2, 'B', 'unknown', 0),
    (44, 3, 'B', 'unknown', 0),

    (46, 1, 'A', 'unknown', 0), -- controls
    (46, 2, 'A', 'unknown', 0),
    (46, 3, 'A', 'unknown', 0),
    (46, 4, 'A', 'unknown', 0),
    (46, 5, 'A', 'unknown', 0),
    (46, 1, 'B', 'unknown', 1),
    (46, 2, 'B', 'unknown', 1),
    (46, 3, 'B', 'unknown', 0),
    (46, 4, 'B', 'unknown', 0),
    (46, 5, 'B', 'unknown', 1),
    (46, 1, 'C', 'left', 0),
    (46, 2, 'C', 'right', 1),
    (46, 3, 'C', 'right', 1),
    (46, 4, 'C', 'left', 1),
    (46, 5, 'C', 'left', 1),

    (65, 1, 'A', 'unknown', 1), -- proprio treated
    (65, 2, 'A', 'unknown', 1),
    (65, 3, 'A', 'unknown', 1),
    (65, 4, 'A', 'unknown', 0),
    (65, 5, 'A', 'unknown', 1),
    (65, 1, 'B', 'unknown', 0),
    (65, 2, 'B', 'unknown', 1),
    (65, 3, 'B', 'unknown', 1),
    (65, 4, 'B', 'unknown', 0),
    (65, 5, 'B', 'unknown', 1),
    (65, 1, 'C', 'left', 0),
    (65, 2, 'C', 'right', 0),
    (65, 3, 'C', 'left', 0),

    (71, 1, 'A', 'right', 0), -- mdd_mdv treated
    (71, 2, 'A', 'right', 1),
    (71, 3, 'A', 'right', 0),
    (71, 4, 'A', 'right', 1),
    (71, 5, 'A', 'right', 0),
    (71, 1, 'B', 'right', 0),
    (71, 2, 'B', 'right', 0),
    (71, 3, 'B', 'right', 0),
    (71, 4, 'B', 'right', 0),
    (71, 5, 'B', 'right', 0),

    (73, 1, 'A', 'right', 0), -- triple treated
    (73, 2, 'A', 'left', 0),
    (73, 3, 'A', 'left', 0),
    (73, 4, 'A', 'left', 0),
    (73, 5, 'A', 'unknown', 1),
    (73, 1, 'B', 'right', 0),
    (73, 2, 'B', 'left', 0),
    (73, 3, 'B', 'left', 0),
    (73, 4, 'B', 'right', 0),
    (73, 5, 'B', 'right', 0);
COMMIT;
