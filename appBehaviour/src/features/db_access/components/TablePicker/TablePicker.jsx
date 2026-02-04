
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

  const rules = [
    { table: "behaviors",  key: "behavior_id",  dict: behaviourDict },
    { table: "metrics",    key: "metric_id",    dict: metricDict },
    { table: "timepoints", key: "timepoint_id", dict: timepointDict },
    { table: "mice",       key: "mouse_id",     dict: miceDict },
  ];

  const translatedRows = rows.map(r => {
    const out = { ...r };

    for (const { table, key, dict } of rules) {
      if (safeSelectedTable !== table) {
        out[key] = dict?.[out[key]] ?? out[key];
      }
    }

    return out;
  });


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
