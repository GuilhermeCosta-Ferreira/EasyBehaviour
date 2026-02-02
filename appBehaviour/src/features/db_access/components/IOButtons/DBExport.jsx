import { exportWorkingDb } from '../../../../shared/db/connection';
import Button from '../../../../shared/ui/Button/Button';

function DBExport() {
  const onExportClick = async () => {
    const exportedTo = await exportWorkingDb();
    console.log('Exported to:', exportedTo);
  };

  return (
    <Button onClick={onExportClick}>
      Export DB
    </Button>
  )
}

export default DBExport
