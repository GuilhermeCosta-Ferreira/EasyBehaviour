
import { useEffect, useMemo, useState } from "react";
import { getWorkingDb } from "../../../../shared/db/connection";

import AppDropdown from "../../../../shared/ui/Dropdown/Dropdown";
import TableViewer from "../TableViewer/TableViewer";
import Button from "../../../../shared/ui/Button/Button";

import { useSqliteTableNames } from "../../../../shared/hooks/useDBNameResult";
import { useSafeTableName } from "../../../../shared/hooks/useSafeTableName";
import { useSqliteTableData } from "../../../../shared/hooks/useDBTableData";
import { useBehaviorDictionary } from "../../../../shared/hooks/useBehaviourDictionary";

import style from "./TablePicker.module.css"


function TablePicker() {
  const [selectedTable, setSelectedTable] = useState(null);

  const { dict: behaviourDict, loading, error, reload } = useBehaviorDictionary();
  const { names, loading: loadingNames, error: namesError } = useSqliteTableNames();
  const safeSelectedTable = useSafeTableName(selectedTable, names);

  const {
      columns,
      rows,
      loading: loadingTable,
      error: tableError,
      clear: clearTable,
    } = useSqliteTableData(safeSelectedTable);


  const handleDeselect = () => {
      setSelectedTable(null);
      clearTable();
    };

  if (error) return <p>Error: {error}</p>;
  if (loading) return <p>Loading…</p>;

  const title = safeSelectedTable ? `Inspected Table: ${safeSelectedTable}` : "Inspect a Raw Table";

  let translatedRows = rows
  if (safeSelectedTable !== "behaviors") {
    translatedRows = rows.map(r => ({
      ...r,
      // overwrite behavior_id instead of creating a new column
      behavior_id: behaviourDict[r.behavior_id] ?? r.behavior_id // or "(unknown)"
    }));
  }

  console.log(translatedRows);

  return (
    <div>
      <div className={`scontainer ${style.input}`}>
        <AppDropdown
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

      {!loading && safeSelectedTable && (
        <TableViewer
          className="scontainer"
          columns={columns}
          rows={translatedRows}
        ></TableViewer>)}
    </div>
  );
}

export default TablePicker;
