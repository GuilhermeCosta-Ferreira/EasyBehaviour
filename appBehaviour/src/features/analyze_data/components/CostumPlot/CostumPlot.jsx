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


  // The Plot Settings
  const option = {
    title: { text: "ECharts Getting Started Example" },
    tooltip: {},
    legend: { data: ["sales"] },
    xAxis: {
      type: "category",
      data: ["Shirts", "Cardigans", "Chiffons", "Pants", "Heels", "Socks"],
    },
    yAxis: { type: "value" },
    series: [
      {
        name: "sales",
        type: "bar",
        data: [5, 20, 36, 10, 10, 20],
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
