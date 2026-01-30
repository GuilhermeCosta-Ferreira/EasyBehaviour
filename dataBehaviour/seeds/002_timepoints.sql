BEGIN;

INSERT INTO timepoints (code, label, event_type, weeks_after_event)
VALUES
    ('baseline', 'Baseline', 'unspecified', -1),
    ('post_ablation_w1', 'W1 Post Ablation', 'ablation', 1),
    ('post_injury_w1', 'W1 Post Injury', 'injury', 1),
    ('post_injury_w4', 'W4 Post Injury', 'injury', 4),
    ('post_injury_w8', 'W8 Post Injury', 'injury', 8);

COMMIT;
