
import { useEffect, useMemo, useState } from "react";
import { getWorkingDb } from "../../../../shared/db/connection";

import AppDropdown from "../../../../shared/ui/Dropdown/Dropdown";
import TableViewer from "../TableViewer/TableViewer";
import Button from "../../../../shared/ui/Button/Button";

import style from "./TablePicker.module.css"


function TablePicker() {
  const [error, setError] = useState(null);

  const [names, setNames] = useState([]);
  const [selectedTable, setSelectedTable] = useState(null);

  const [rows, setRows] = useState([]);
  const [columns, setColumns] = useState([]);
  const [loading, setLoading] = useState(false);

  // 1. Load list of tables once
  useEffect(() => {
    let cancelled = false;

    (async () => {
      try {
        setError(null);
        const db = await getWorkingDb();

        const tables = await db.select(`
          SELECT name
          FROM sqlite_master
          WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
          ORDER BY name
        `);

        if (cancelled) return;

        const tableNames = tables.map((r) => r.name);
        setNames(tableNames);

        // optional: auto-select first table
        // setSelectedTable(tableNames[0] ?? null);
      } catch (e) {
        if (!cancelled) setError(String(e));
      }
    })();

    return () => {
      cancelled = true;
    };
  }, []);



  // 2. Validate selected table name against the known names list
  const safeSelectedTable = useMemo(() => {
    if (!selectedTable) return null;
    return names.includes(selectedTable) ? selectedTable : null;
  }, [selectedTable, names]);



  // 3. Load selected table whenever it changes
  useEffect(() => {
    let cancelled = false;

    (async () => {
      if (!safeSelectedTable) {
        setRows([]);
        setColumns([]);
        return;
      }

      try {
        setLoading(true);
        setError(null);

        const db = await getWorkingDb();

        // Get column names
        const info = await db.select(`PRAGMA table_info("${safeSelectedTable}")`);
        if (cancelled) return;

        const cols = info.map((c) => c.name);
        setColumns(cols);

        // Load some rows (limit for performance)
        const data = await db.select(`SELECT * FROM "${safeSelectedTable}" LIMIT 200`);
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
  }, [safeSelectedTable]);



  const handleDeselect = () => {
      setSelectedTable(null);
      setRows([]);
      setColumns([]);
      setLoading(false);
    };



  if (error) return <p>Error: {error}</p>;
  const title = safeSelectedTable ? `Inspected Table: ${safeSelectedTable}` : "Inspect a Raw Table";

  return (
    <div>
      <div className={style.input}>
        <AppDropdown
          className="scontainer"
          title={title}
          items={names}
          onSelect={setSelectedTable}
        />
        <Button onClick={handleDeselect}>X</Button>
      </div>

      {loading && <p>Loading…</p>}

      {!loading && safeSelectedTable && (
        <TableViewer
          className="scontainer"
          columns={columns}
          rows={rows}
        ></TableViewer>)}
      </div>
  );
}

export default TablePicker;
