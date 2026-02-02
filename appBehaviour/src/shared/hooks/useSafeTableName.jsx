import { useMemo } from "react";

export function useSafeTableName(selectedTable, names) {
  return useMemo(() => {
    if (!selectedTable) return null;
    return names.includes(selectedTable) ? selectedTable : null;
  }, [selectedTable, names]);
}
