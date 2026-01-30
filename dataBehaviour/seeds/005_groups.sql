BEGIN;

INSERT INTO groups (group_id, name, nr_of_cages, nr_of_mice, notes)
VALUES
    (44, 'Injured Vsx Ablated Untreated', 2, 8, NULL),
    (46, 'Injured Untreated (Control)', 3, 15, '4 died, but baselines where recorded, so accounted here'),
    (65, 'Injured Propriospinal Treated', 3, 13, NULL),
    (71, 'Injured MdD & MdV Treated', 2, 10, NULL),
    (73, 'Injured Triple Treated', 2, 9, 'Propriospinal & MdD & MdV. 1 Died before BL, so not accounted here');

COMMIT;
