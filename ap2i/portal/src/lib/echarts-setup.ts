// Only the chart types / components the portal uses: named imports let the bundler drop the rest of ECharts.
import * as echarts from "echarts/core";
import { BarChart, LineChart, PieChart, SankeyChart, ScatterChart, TreemapChart } from "echarts/charts";
import { AriaComponent, GridComponent, LegendComponent, MarkAreaComponent, TitleComponent, TooltipComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";

echarts.use([BarChart, LineChart, PieChart, SankeyChart, ScatterChart, TreemapChart, AriaComponent, GridComponent, LegendComponent,
  MarkAreaComponent, TitleComponent, TooltipComponent, CanvasRenderer]);

export default echarts;
