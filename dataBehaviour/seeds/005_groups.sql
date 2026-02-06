BEGIN;

INSERT INTO groups (group_id, name, study_type, was_treated, was_injured, nr_of_cages, nr_of_mice, notes)
VALUES
    (44, 'Injured Vsx Ablated Untreated', 'injury', 0, 1, 2, 8, NULL),
    (46, 'Injured Untreated (Control)', 'injury', 0, 1, 3, 15, '4 died, but baselines where recorded, so accounted here'),
    (65, 'Injured Propriospinal Treated', 'injury', 1, 1, 3, 13, NULL),
    (71, 'Injured MdD & MdV Treated', 'injury', 1, 1, 2, 10, NULL),
    (73, 'Injured Triple Treated', 'injury', 1, 1, 2, 9, 'Propriospinal & MdD & MdV. 1 Died before BL, so not accounted here')
ON CONFLICT(group_id) DO UPDATE SET
    name        = excluded.name,
    study_type  = excluded.study_type,
    was_treated = excluded.was_treated,
    was_injured = excluded.was_injured,
    nr_of_cages = excluded.nr_of_cages,
    nr_of_mice  = excluded.nr_of_mice,
    notes       = excluded.notes;

COMMIT;
