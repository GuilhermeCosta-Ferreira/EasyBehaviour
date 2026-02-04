import { useDBTableData } from "../../../../shared/hooks/useDBTableData"

import AppDropdown from "../../../../shared/ui/Dropdown/Dropdown"
import Toggle from "../../../../shared/ui/Toggle/Toggle"

import style from "./SelectionMenu.module.css"

function SelectionMenu() {
  // Extacts the data from the observations columns
  const { columns, rows, loading, error, clear } = useDBTableData("observations")

  return (
    <div className={style.menu}>
      <Toggle
        className="scontainer"
        title='Testing Toggle'
        options={columns}
        />
      <AppDropdown
        title={"Select the Behaviour to Analyse"}
        items={columns}
        className="scontainer"
      />
    </div>
  )
}

export default SelectionMenu
