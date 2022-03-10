import React, { useContext, useEffect } from "react";
import { useState } from "react";
import useFetch from "./useFetch";
import { ScenarioContext } from "./ScenarioContext";
import { StatusContext } from "./StatusContext";
import Button from "react-bootstrap/Button";
import getCookie from "./getCookie";

function EVDropdown(props) {
  const [scenario] = useContext(ScenarioContext);

  const [status] = useContext(StatusContext);

  const { data: evs } = useFetch("http://127.0.0.1/api/ev-list/", "");

  const { data: house } = useFetch("http://127.0.0.1:/api/house/", props.node);

  const csrftoken = getCookie('csrftoken')
  console.log(csrftoken)

  const [selected, setSelected] = useState({
    ev_id: 1,
    make: "tesla",
    model: "x",
    year: 2010,
  });
  const [chosenEVs, setChosenEVs] = useState([]);
  const [houseEVs, setHouseEVs] = useState([]);

  useEffect(() => {
    if (props.confirmed === false) {
      let arr = [];
      setChosenEVs(arr);
      setHouseEVs(arr);
    }
  }, [props.confirmed]);

  const handleChange = (e) => {
    const id = parseInt(e.target.value);
    const found = evs.find((item) => item.ev_id === id);
    setSelected(found);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (status) {
      alert("EVs cannot be added whilst a Simulation is running");
    } else {
      fetch("http://127.0.0.1:/api/houseevs/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
          house: house.house_id,
          ev: selected.ev_id,
          scenario: scenario.scenario_id,
        }),
      })
        .then((resp) => resp.json())
        .then((resp) => {
          setChosenEVs(() => [...chosenEVs, selected]);
          setHouseEVs(() => [...houseEVs, resp]);
        })
        .catch((error) => console.log(error))

    }
  };

  const handleDelete = (e) => {
    e.preventDefault();

    houseEVs.forEach((item) => {
      console.log(item.house_ev_id);
      fetch("http://127.0.0.1:/api/houseevs/" + item.house_ev_id, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((resp) => resp.json())
        .catch((error) => console.log(error));
    });
    let arr = [];
    setChosenEVs(arr);
    setHouseEVs(arr);
  };

  return (
    <div className="evmenu">
      <form onSubmit={handleSubmit}>
        <label>
          Add Electric Vehicles:
          <select value={selected.ev_id} onChange={handleChange}>
            {evs.map((item) => (
              <option key={item.ev_id} value={item.ev_id}>
                {item.make}
              </option>
            ))}
          </select>
          <Button variant="success" size="sm" type="submit" value="+">
            {" "}
            +
          </Button>
        </label>

        <div className="chosenevs">
          EVs:
          {chosenEVs.map((item) => " " + item.make + ",")}
          <Button variant="danger" size="sm" onClick={handleDelete}>
            X
          </Button>
        </div>
      </form>
    </div>
  );
}

export default EVDropdown;