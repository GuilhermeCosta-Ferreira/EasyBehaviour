import ReactECharts from "echarts-for-react";
import * as echarts from "echarts";
import nr_theme from "../../../../assets/themes/nr_style.json";
import style from './TestPlot.module.css'
const THEME_NAME = "nr_style";

// Guard to avoid re-registering during dev hot reload
if (!window.__NR_THEME_REGISTERED__) {
  echarts.registerTheme(THEME_NAME, nr_theme);
  window.__NR_THEME_REGISTERED__ = true;
}

export default function TestPlot() {
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
        markLine: {
          symbol: "none",
          lineStyle: {
            color: "#fff", // line colour
            width: 2,
            type: "solid", // "dashed" | "dotted"
          },
          label: {
            formatter: "p = 0.01",
            color: "#fff",
            position: "middle",
          },
          data: [
            [
              { xAxis: "Shirts", yAxis: 40 },
              { xAxis: "Cardigans", yAxis: 40 },
            ],
          ],
        },
      },
    ],
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
