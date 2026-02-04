import { makeRowTranslationRules } from "../../../../shared/db/translation/rules"
import { translateRows } from "../../../../shared/db/translation/translate"
import { useDBTableData } from "../../../../shared/hooks/useDBTableData"
import { useDictionary } from "../../../../shared/hooks/useDictionary"

import Toggle from "../../../../shared/ui/Toggle/Toggle"
import style from "./SelectionMenu.module.css"



function SelectionMenu() {
  // 1. Extacts the data from the observations columns
  const { columns, rows, loading, error, clear } = useDBTableData("observations")
  const { behaviourDict, metricDict, timepointDict, miceDict, loadingD, errorD, reload } = useDictionary();

  // 2. Get the translated rows
  const rules = makeRowTranslationRules({ behaviourDict, metricDict, timepointDict, miceDict });
  const translatedRows = translateRows({ rows, selectedTable: "observations", rules });

  // 2. Gets all the unique values per column
  function getColumnUnique(columnName, rows) {
    const values = rows.map(r => r[columnName]);
    const unique = [...new Set(values)];

    return unique
  }
  const unique_array = columns.map(m => [m, getColumnUnique(m, translatedRows)])

  // 3. Filter for non filterable columns: value and notes
  const NON_FILTERABLE = new Set(["value", "notes"]);
  const filtered_columns = unique_array.filter(([colName]) => !NON_FILTERABLE.has(colName));

  return (
    <div className={`scontainer ${style.menuContainer}`}>
      <div className={`${style.menu}`}>
        {filtered_columns.map(([col, values]) => (
          <Toggle
            title={col}
            options={values}
          />
        ))}
      </div>
    </div>
  )
}

export default SelectionMenu
