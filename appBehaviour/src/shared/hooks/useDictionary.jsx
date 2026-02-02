import { useCallback, useEffect, useState } from "react";
import { translateDict } from "../db/translate";

export function useDictionary() {
  const [behaviourDict, setBehaviourDict] = useState({});
  const [metricDict, setMetricDict] = useState({});
  const [timepointDict, setTimepointDict] = useState({});
  const [miceDict, setMiceDict] = useState({});

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

        const { behaviour_dict, metric_dict, timepoint_dict, mice_dict } = await translateDict();
        if (cancelled) return;

        setBehaviourDict(behaviour_dict);
        setMetricDict(metric_dict);
        setTimepointDict(timepoint_dict);
        setMiceDict(mice_dict);

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

  return { behaviourDict, metricDict, timepointDict, miceDict, loading, error, reload };
}
