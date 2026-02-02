import { useEffect, useState, useCallback } from "react";
import { getWorkingDb } from "../db/connection"; // adjust this path

export function useSqliteTableData(safeTableName) {
  const [columns, setColumns] = useState([]);
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const clear = useCallback(() => {
    setColumns([]);
    setRows([]);
    setLoading(false);
    setError(null);
  }, []);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      if (!safeTableName) {
        clear();
        return;
      }

      try {
        setLoading(true);
        setError(null);

        const db = await getWorkingDb();

        const info = await db.select(`PRAGMA table_info("${safeTableName}")`);
        if (cancelled) return;

        setColumns(info.map((c) => c.name));

        const data = await db.select(`SELECT * FROM "${safeTableName}" LIMIT 200`);
        if (cancelled) return;

        setRows(data);
      } catch (e) {
        if (!cancelled) setError(String(e));
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [safeTableName, clear]);

  return { columns, rows, loading, error, clear };
}
