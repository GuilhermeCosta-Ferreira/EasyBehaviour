import DBImport from "../IOButtons/DBImport";
import DBExport from "../IOButtons/DBExport";
import style from "./IOPannel.module.css"

function IOPannel() {
  return (
    <div className={`container ${style.pannel}`}>
      <DBImport></DBImport>
      <DBExport></DBExport>
    </div>
  )
}

export default IOPannel
