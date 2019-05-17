import React, {Component} from "react";
import ReactDOM from "react-dom";
import Chart from "react-google-charts";
// Ref : https://developers.google.com/chart/interactive/docs/gallery/histogram

const data = [
  ["Year", "Sales", "Expenses"],
  ["2004", 1000, 400],
  ["2005", 1170, 460],
  ["2006", 660, 1120],
  ["2007", 1030, 540]
];
const options = {
  title: "Betting Outcomes",
  curveType: "function",
  legend: { position: "right" }
};
class LineChart extends Component {
  render() {
    return (
      <div className="chart">
        <Chart
          chartType="LineChart"
          width="100%"
          height="400px"
          data={data}
          options={options}
        />
      </div>
    );
  }
}

export default LineChart;
