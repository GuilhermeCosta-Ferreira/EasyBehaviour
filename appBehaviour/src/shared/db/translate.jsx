import { getWorkingDb } from './connection';

export async function behaviorDictionary() {
  const db = await getWorkingDb();

  // adjust column names if yours differ
  const rows = await db.select(
    `SELECT behavior_id AS id, name FROM behaviors`
  );

  // { "1": "Walk", "2": "Run", ... }
  const dict = Object.fromEntries(
    rows.map(r => [r.id, r.name])
  );

  return dict;
}
