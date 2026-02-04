export function makeRowTranslationRules(dicts) {
  return [
    { table: "behaviors",  key: "behavior_id",  dict: dicts.behaviourDict },
    { table: "metrics",    key: "metric_id",    dict: dicts.metricDict },
    { table: "timepoints", key: "timepoint_id", dict: dicts.timepointDict },
    { table: "mice",       key: "mouse_id",     dict: dicts.miceDict },
  ];
}
