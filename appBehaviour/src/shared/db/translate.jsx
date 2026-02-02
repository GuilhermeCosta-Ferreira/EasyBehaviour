import { getWorkingDb } from './connection';

export async function translateDict() {
  const db = await getWorkingDb();

  // adjust column names if yours differ
  const behaviour_rows = await db.select(
    `SELECT behavior_id AS id, name FROM behaviors`
  );

  // { "1": "Walk", "2": "Run", ... }
  const behaviour_dict = Object.fromEntries(
    behaviour_rows.map(r => [r.id, r.name])
  );

  // adjust column names if yours differ
  const metric_rows = await db.select(
    `SELECT metric_id AS id, name FROM metrics`
  );

  const metric_dict = Object.fromEntries(
    metric_rows.map(r => [r.id, r.name])
  );

  // adjust column names if yours differ
  const timepoint_rows = await db.select(
    `SELECT timepoint_id AS id, label as name FROM timepoints`
  );

  const timepoint_dict = Object.fromEntries(
    timepoint_rows.map(r => [r.id, r.name])
  );

  // adjust column names if yours differ
  const mice_rows = await db.select(
    `SELECT mouse_id AS id, mouse_number AS name, cage_letter AS cage FROM mice`
  );

  const mice_dict = Object.fromEntries(
    mice_rows.map((r) => [r.id, `${r.name}${r.cage}`])
  );

  return {behaviour_dict, metric_dict, timepoint_dict, mice_dict};
}
