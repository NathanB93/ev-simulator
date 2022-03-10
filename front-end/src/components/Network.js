import React, { useContext } from "react";
import NodeList from "./NodeList";
import { useState, useEffect } from "react";
import useFetch from "./useFetch";
import Button from "react-bootstrap/Button";

import { ScenarioContext } from "./ScenarioContext";
import { StatusContext } from "./StatusContext";
import getCookie from "./getCookie";

function Network() {
  const [cableSpec, setCableSpec] = useState("");

  const [confirmed, setConfirmed] = useState(false);

  const [name, setName] = useState("");

  const [scenario, setScenario] = useContext(ScenarioContext);

  const [status] = useContext(StatusContext);

  const csrftoken = getCookie('csrftoken')
  console.log(csrftoken)

  const { data: networks } = useFetch(
    "http://127.0.0.1:/api/network-list/",
    ""
  );

  const [selected, setSelected] = useState({
    network_id: 1,
    name: "network1",
    substation: 1,
  });

  useEffect(() => {
    setConfirmed(confirmed);
  }, [confirmed]);

  const renderConfirmed = () => {
    if (confirmed) {
      return "Confirmed";
    }
  };

  const handleChange = (e) => {
    if (!confirmed) {
      const id = parseInt(e.target.value);
      const found = networks.find((item) => item.network_id === id);

      setSelected(found);
    } else {
      alert("Please press cancel button if you wish to change Network");
    }
  };

  const renderNodeList = () => {
    if (!selected) return;
    return (
      <NodeList
        network={selected.network_id}
        substation={selected.substation}
        confirmed={confirmed}
      />
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (confirmed) {
      alert("Your Scenario: " + scenario.name + " is already confirmed.");
    } else if (cableSpec && name) {
      fetch("http://127.0.0.1:/api/scenario/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
          name: name,
          cable_spec: cableSpec,
          network_id: selected.network_id,
        }),
      })
        .then((resp) => resp.json())
        .then((data) => {
          setConfirmed(true);
          setScenario(data);
          alert(
            "Network Configuration confirmed, you can now assign EVs and run your simulation."
          );
        })
        .catch((error) => console.log(error));
    } else if (cableSpec && !name) {
      alert("Name can not be empty, please try again.");
    } else if (!cableSpec && name) {
      alert("Max Current can not be empty, please try again.");
    } else {
      alert("All fields must be completed, please try again.");
    }
  };

  const handleClick = () => {
    if (confirmed && !status) {
      setConfirmed(false);
      setScenario({
        scenario_id: "default",
        name: "",
        cable_spec: 123,
        network_id: 3,
      });
      setName("");
      setCableSpec("");
    } else if (confirmed && status) {
      alert(
        "Configuration cannot be cancelled while a simulation is running, please cancel the simulation and try again"
      );
    } else {
      alert("You have not confirmed a configuration.");
    }
  };

  return (
    <div className="configpanel">
      <form className="network" onSubmit={handleSubmit}>
        <h1>Scenario</h1>

        <p>
          <label className="networklabel">Select a Network:</label>
          <select
            className="networkselect"
            value={selected.network_id}
            onChange={handleChange}
          >
            {networks.map((network) => (
              <option key={network.network_id} value={network.network_id}>
                {network.name}
              </option>
            ))}
          </select>
        </p>

        <p>
          <label className="namelabel">Name:</label>

          <input
            className="nameinput"
            type="text"
            placeholder="Enter scenario name"
            value={name}
            onChange={(e) => {
              setName(e.target.value);
            }}
          />
        </p>

        <p>
          <label className="currentlabel">Max Current(A): </label>

          <input
            className="currentinput"
            type="number"
            placeholder="Enter max current"
            min="0"
            value={cableSpec}
            onChange={(e) => {
              setCableSpec(e.target.value);
            }}
          />
        </p>

        <p>
          <Button
            variant="success"
            className="confirm"
            type="submit"
            value="Confirm"
          >
            Confirm
          </Button>

          <Button
            variant="danger"
            className="cancel"
            type="button"
            onClick={() => {
              handleClick();
            }}
          >
            Cancel
          </Button>
          <div className="confirmed">{renderConfirmed()}</div>
        </p>
      </form>

      {renderNodeList()}
    </div>
  );
}

export default Network;
