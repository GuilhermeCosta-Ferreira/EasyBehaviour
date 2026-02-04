
import { useState } from "react";

import AppDropdown from "../../../../shared/ui/Dropdown/Dropdown";
import TableViewer from "../TableViewer/TableViewer";
import Button from "../../../../shared/ui/Button/Button";

import { useSqliteTableNames } from "../../../../shared/hooks/useDBNameResult";
import { useSafeTableName } from "../../../../shared/hooks/useSafeTableName";
import { useDBTableData } from "../../../../shared/hooks/useDBTableData";
import { useDictionary } from "../../../../shared/hooks/useDictionary";

import style from "./TablePicker.module.css"


function TablePicker() {
  const [selectedTable, setSelectedTable] = useState(null);

  const { names, loading: loadingNames, error: namesError } = useSqliteTableNames();
  const safeSelectedTable = useSafeTableName(selectedTable, names);

  const {
      columns,
      rows,
      loading: loadingTable,
      error: tableError,
      clear: clearTable,
    } = useDBTableData(safeSelectedTable);

  const { behaviourDict, metricDict, timepointDict, miceDict, loading, error } = useDictionary();
  const handleDeselect = () => {
      setSelectedTable(null);
      clearTable();
    };

  if (error) return <p>Error: {error}</p>;
  if (loading) return <p>Loading…</p>;

  const title = safeSelectedTable ? `Inspected Table: ${safeSelectedTable}` : "Inspect a Table";

  let translatedRows = rows

  if (safeSelectedTable !== "behaviors") {
    translatedRows = rows.map(r => ({
      ...r,
      // overwrite behavior_id instead of creating a new column
      behavior_id: behaviourDict[r.behavior_id] ?? r.behavior_id // or "(unknown)"
    }));
  }

  if (safeSelectedTable !== "metrics") {
    translatedRows = translatedRows.map(r => ({
      ...r,
      // overwrite behavior_id instead of creating a new column
      metric_id: metricDict[r.metric_id] ?? r.metric_id // or "(unknown)"
    }));
  }

  if (safeSelectedTable !== "timepoints") {
    translatedRows = translatedRows.map(r => ({
      ...r,
      // overwrite behavior_id instead of creating a new column
      timepoint_id: timepointDict[r.timepoint_id] ?? r.timepoint_id // or "(unknown)"
    }));
  }

  if (safeSelectedTable !== "mice") {
    translatedRows = translatedRows.map(r => ({
      ...r,
      // overwrite behavior_id instead of creating a new column
      mouse_id: miceDict[r.mouse_id] ?? r.mouse_id // or "(unknown)"
    }));
  }

  console.log(miceDict)
  //console.log(translatedRows);

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
          rows={translatedRows}
        ></TableViewer>)}
    </div>
  );
}

export default TablePicker;
