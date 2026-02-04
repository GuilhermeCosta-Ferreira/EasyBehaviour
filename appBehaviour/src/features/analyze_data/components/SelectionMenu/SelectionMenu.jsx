import { makeRowTranslationRules } from "../../../../shared/db/translation/rules"
import { translateRows } from "../../../../shared/db/translation/translate"
import { useDBTableData } from "../../../../shared/hooks/useDBTableData"
import { useDictionary } from "../../../../shared/hooks/useDictionary"

import Toggle from "../../../../shared/ui/Toggle/Toggle"
import style from "./SelectionMenu.module.css"



function SelectionMenu({filterCall}) {
  // 1. Extacts the data from the observations columns
  const { columns, rows, loading, error, clear } = useDBTableData("observations")
  const { behaviourDict, metricDict, timepointDict, miceDict, loadingD, errorD, reload } = useDictionary();

  // 2. Get the translated rows
  const rules = makeRowTranslationRules({ behaviourDict, metricDict, timepointDict, miceDict });
  const translatedRows = translateRows({ rows, selectedTable: "observations", rules });

  // 3. Gets all the unique values per column
  function getColumnUnique(columnName, rows) {
    const values = rows.map(r => r[columnName]);
    const unique = [...new Set(values)];

    return unique
  }
  const unique_translated_array = columns.map(m => [m, getColumnUnique(m, translatedRows)])
  const unique_array = columns.map(m => [m, getColumnUnique(m, rows)])

  // 4. Filter for non filterable columns: value and notes
  const NON_FILTERABLE = new Set(["value", "notes"]);
  const filtered_translated_columns = unique_translated_array.filter(([colName]) => !NON_FILTERABLE.has(colName));
  const filtered_columns = unique_array.filter(([colName]) => !NON_FILTERABLE.has(colName));

  return (
    <div className={`scontainer ${style.menuContainer}`}>
      <div className={`${style.menu}`}>
        {filtered_translated_columns.map(([col, values], index) => (
            <Toggle
              title={col}
              options={values}
              originalValues={filtered_columns?.[index]?.[1] ?? []}
              filterCall={filterCall}
              key={`toggle-${col}`}
            />
        ))}
      </div>
    </div>
  )
}

export default SelectionMenu
