export function translateRows({ rows, selectedTable, rules }) {
  return rows.map(r => {
    const out = { ...r };

    for (const { table, key, dict } of rules) {
      if (selectedTable !== table) {
        out[key] = dict?.[out[key]] ?? out[key];
      }
    }

    return out;
  });
}
