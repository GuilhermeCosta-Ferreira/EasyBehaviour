import DBImport from "../IOButtons/DBImport";
import DBExport from "../IOButtons/DBExport";
import style from "./IOPannel.module.css"
import Button from "../../../../shared/ui/Button/Button";
import { deselectWorkingDb } from "../../../../shared/db/connection";

function IOPannel() {
  const handleCloseDb = async () => {
      try {
        await deselectWorkingDb({deleteWorkingFile: true}); // or { deleteWorkingFile: true }
        // Optional: show a toast / update UI state here
      } catch (err) {
        console.error("Failed to deselect DB:", err);
        // Optional: show error toast
      }
    };

  return (
    <div className={`container ${style.pannel}`}>
      <DBImport></DBImport>
      <DBExport></DBExport>
      <Button onClick={handleCloseDb}>X</Button>
    </div>
  )
}

export default IOPannel
