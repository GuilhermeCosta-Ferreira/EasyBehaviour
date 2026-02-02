import { useCallback, useEffect, useState } from "react";
import { getWorkingDb } from "../db/connection"; // adjust path

export function useBehaviorDictionary() {
  const [dict, setDict] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [nonce, setNonce] = useState(0);
  const reload = useCallback(() => setNonce((n) => n + 1), []);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      try {
        setLoading(true);
        setError(null);

        const db = await getWorkingDb();
        const rows = await db.select(
          `SELECT behavior_id AS id, name FROM behaviors`
        );

        if (cancelled) return;

        const nextDict = Object.fromEntries(rows.map((r) => [r.id, r.name]));
        setDict(nextDict);
      } catch (e) {
        if (!cancelled) setError(String(e));
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [nonce]);

  return { dict, loading, error, reload };
}
