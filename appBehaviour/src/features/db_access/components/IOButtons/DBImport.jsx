import { importDbFromUserFile, getWorkingDb } from '../../../../shared/db/connection';
import Button from '../../../../shared/ui/Button/Button';

function DBImport() {
  const onImportClick = async () => {
    const path = await importDbFromUserFile();
    if (!path) return;

    const db = await getWorkingDb();
    const rows = await db.select('SELECT name FROM sqlite_master WHERE type = "table"');
    console.log('rows', rows);
  };

  return (
    <Button type="button" onClick={onImportClick}>
      Import DB
    </Button>
  );
}

export default DBImport
