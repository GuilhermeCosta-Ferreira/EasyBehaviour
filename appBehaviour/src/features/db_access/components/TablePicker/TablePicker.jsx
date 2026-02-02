import { useEffect, useState } from "react";
import { getWorkingDb } from "../../../../shared/db/connection";
import AppDropdown from "../../../../shared/ui/Dropdown/Dropdown";

function TablePicker() {
  const [error, setError] = useState(null);
  const [names, setNames] = useState([]);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      try {
        setError(null);

        const db = await getWorkingDb();
        const rows = await db.select(`
          SELECT name
          FROM sqlite_master
          WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
          ORDER BY name
          `);

        if (cancelled) return;

        setNames(rows.map((r) => r.name));
      } catch (e) {
        if (cancelled) return;
        setError(String(e));
      }
    })();

    return () => {
      cancelled = true;
    };
  }, []);

  if (error) return <p>Error: {error}</p>;

  return <AppDropdown
    className="scontainer"
    title="Select Tables"
    items={names}>
  </AppDropdown>;
}

export default TablePicker;
