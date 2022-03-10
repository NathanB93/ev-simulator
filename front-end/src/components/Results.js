import React, { useContext, useState } from "react";
import useInterval from "./useInterval";
import CurrentChart from "./CurrentChart";
import { ScenarioContext } from "./ScenarioContext";
import { StatusContext } from "./StatusContext";
import Button from "react-bootstrap/Button";
import getCookie from "./getCookie";

function Results() {
  const [job, setJob] = useState("");
  const [polling, setPolling] = useState(false);
  const [scenario] = useContext(ScenarioContext);
  const [status, setStatus] = useContext(StatusContext);
  const csrftoken = getCookie('csrftoken')
  console.log(csrftoken)

  useInterval(
    () => {
      fetch("http://127.0.0.1:/api/job/" + job, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((resp) => resp.json())
        .then((resp) => {
          if (typeof resp !== "string") {
            setPolling(false);
            setStatus("");
          } else {
            setStatus(resp);

            if (resp === "complete") {
              setPolling(false);
            }
          }
        })

        .catch((error) => console.log(error));
    },
    polling ? 1000 : null
  );

  const handleClickStop = (e) => {
    e.preventDefault();

    if (status) {
      setPolling(false);
      setStatus();
      alert("Simulation of Scenario: " + scenario.name + " has been stopped.");
    } else {
      alert("There is no simulation running.");
    }
  };

  const handleClickRun = (e) => {
    e.preventDefault();

    if (scenario.scenario_id === "default") {
      alert("Please confirm a configuration and try again");
    } else if (status) {
      alert("A simulation is already running.");
    } else {
      fetch("http://127.0.0.1:/api/job/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
          scenario: scenario.scenario_id,
          status: "waiting",
        }),
      })
        .then((resp) => resp.json())
        .then((data) => {
          setJob(data.job_id);
          setStatus(data.status);
          setPolling(true);
        })
        .then((resp) => console.log(resp))
        .catch((error) => console.log(error));
    }
  };

  return (
    <div className="results">
      <CurrentChart />

      <br></br>
      <br></br>
      <br></br>

      <div className="controlpanel">
        <Button
          className="runbutton"
          variant="success"
          onClick={handleClickRun}
        >
          {" "}
          Run
        </Button>{" "}
        <Button
          className="stopbutton"
          size="sm"
          variant="danger"
          onClick={handleClickStop}
        >
          {" "}
          Stop
        </Button>{" "}
        <div className="statuslabel">Status: {status}</div>
      </div>
    </div>
  );
}

export default Results;