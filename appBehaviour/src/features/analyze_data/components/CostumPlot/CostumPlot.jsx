import { useMemo } from "react";

import ReactECharts from "echarts-for-react";
import * as echarts from "echarts";

import { useDBTableData } from "../../../../shared/hooks/useDBTableData";

import nr_theme from "../../../../assets/themes/nr_style.json";
import style from "../TestPlot/TestPlot.module.css"
const THEME_NAME = "nr_style";

// Guard to avoid re-registering during dev hot reload
if (!window.__NR_THEME_REGISTERED__) {
  echarts.registerTheme(THEME_NAME, nr_theme);
  window.__NR_THEME_REGISTERED__ = true;
}

export default function CostumPlot({
  filters
}) {
  // 1. Get the raw data
  const { columns, rows, loading, error, clear } = useDBTableData("observations")

  // 2. Filter it by the filters
  const filteredRows = useMemo(() => {
      if (!rows?.length) return [];

      const active = Object.entries(filters).filter(
        ([, allowed]) => Array.isArray(allowed) && allowed.length > 0
      );

      if (active.length === 0) return rows;

      // (Optional) speedup for big lists: convert allowed arrays to Sets
      const activeSets = active.map(([key, allowed]) => [key, new Set(allowed)]);

      return rows.filter((row) =>
        activeSets.every(([key, allowedSet]) => allowedSet.has(row[key]))
      );
    }, [rows, filters]);

    if (loading) return <div>Loading…</div>;
  if (error) return <div>Error</div>;

  // Get x axis and y axis data
  const xdata = (filteredRows ?? []).map(row => row?.["metric_id"]);
  const ydata = (filteredRows ?? []).map(row => row?.["value"]);

  console.log(rows)
  console.log(filteredRows)


  // The Plot Settings
  const option = {
    title: { text: "ECharts Getting Started Example" },
    tooltip: {},
    legend: { data: ["metric_id"] },
    xAxis: {
      type: "category",
      data: xdata,
    },
    yAxis: { type: "value" },
    series: [
      {
        name: "metric_id",
        type: "bar",
        data: ydata,
      },
    ]
  };

  return (
    <div className={style.wrap}>
      <ReactECharts
      className={style.chart}
      echarts={echarts}
      theme={THEME_NAME}
        option={option}
        style={{ width: "80%", height: "80%" }}
      />
    </div>
  );
}
