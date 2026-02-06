BEGIN;

INSERT INTO timepoints (code, label, event_type, weeks_after_event)
VALUES
    ('baseline', 'Baseline', 'unspecified', -1),
    ('post_ablation_w1', 'W1 Post Ablation', 'ablation', 1),
    ('post_ablation_w4', 'W4 Post Ablation', 'ablation', 4),
    ('post_injury_w1', 'W1 Post Injury', 'injury', 1),
    ('post_injury_w4', 'W4 Post Injury', 'injury', 4),
    ('post_injury_w8', 'W8 Post Injury', 'injury', 8)
ON CONFLICT(code) DO UPDATE SET
    label        = excluded.label,
    event_type  = excluded.event_type,
    weeks_after_event = excluded.weeks_after_event;

COMMIT;
