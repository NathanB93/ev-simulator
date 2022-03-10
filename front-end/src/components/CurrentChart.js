import React, { useContext } from "react";
import { Line } from "react-chartjs-2";

import { useState, useEffect } from "react";
import { ScenarioContext } from "./ScenarioContext";
import { StatusContext } from "./StatusContext";


const CurrentChart = () => {
  const [chartData, setChartData] = useState({});
  const [scenario] = useContext(ScenarioContext);
  const [status] = useContext(StatusContext);

  const chart = () => {
    if (scenario.scenario_id !== "default") {
      fetch("http://127.0.0.1:/api/results/" + scenario.scenario_id, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
          .then((resp) => resp.json())
          .catch((error) => console.log(error))
          .then((resp) => {

            let xVals = resp.map((item) => parseInt(item.total_charge_x));
            let yVals = resp.map((item) => parseInt(item.total_charge_y));
            console.log(resp);

            let threshold = new Array(xVals.length).fill(scenario.cable_spec);

            setChartData({
              labels: xVals,
              datasets: [
                {
                  label: "Current vs Time",
                  pointStyle: "circle",
                  data: yVals,
                  backgroundColor: "rgba(0, 255, 0,  0.4)",
                  borderColor: "rgba(0, 0, 0,  1)",
                  pointBackgroundColor: "rgba(0, 255, 0,  1)",
                  pointBorderWidth: 0.1,
                  fill: "origin",
                  borderWidth: 1,
                  lineTension: 0.8,
                  showLine: true,
                  spanGaps: true,
                },
                {
                  label: "Current threshold",
                  pointStyle: "circle",
                  data: threshold,
                  borderColor: "rgba(255, 0, 0, 1)",
                  pointRadius: 0,
                  pointBackgroundColor: "rgba(255,0, 0, 1)",
                  borderWidth: 3,
                  lineTension: 0.8,
                  showLine: true,
                  spanGaps: true,
                },
              ],
            });
          });
    } else {
      setChartData({
        labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        datasets: [
            {
              label: "Current vs Time",
              pointStyle: "star",
              data: [],
              backgroundColor: ["rgba(75, 192, 0.6)"],
              borderWidth: 4,
              lineTension: 0.8,
            },
        ],
      });
    }
  };
  useEffect(() => {
    chart();
  }, [status, scenario]);
  return (
    <div className="chart">
      <Line
        data={chartData}
        options={{
          plugins: {
            title: {
              display: true,
              text: scenario.name,
              font: {
                size: 30,
              },
              color: "#000000",
            },

            legend: {
              display: true,
              labels: {
                font: {
                  size: 15,
                },
                color: "#000000",
                boxWidth: 10,

                padding: 5,
              },
            },
          },

          scales: {
            x: {
              display: true,
              title: {
                display: true,
                text: "Time(min)",
                font: {
                  size: 20,
                },
                color: "#000000",
              },
            },

            y: {
              display: true,
              title: {
                display: true,
                text: "Current(A)",
                font: {
                  size: 20,
                },
                color: "#000000",
              },
            },
          },
        }}
      />
    </div>
  );
};

export default CurrentChart;
