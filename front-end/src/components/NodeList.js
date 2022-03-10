import React, { useContext } from "react";
import EVDropdown from "./EVDropdown";
import useFetch from "./useFetch";

function NodeList(props) {
  const { data: nodes } = useFetch(
    "http://127.0.0.1:/api/nodes/",
    props.network
  );

  const renderEVDropdown = (node) => {
    if (props.confirmed) {
      if (node.node_id === props.substation) return;
      return <EVDropdown node={node.node_id} confirmed={props.confirmed} />;
    }
  };

  return (
    <div className="nodelist">
      <div className="nodeheader">{"Network"}</div>

      {nodes &&
        nodes.map((node) => {
          return (
            <div className="node" key={node.node_id}>
              <h1>{node.name}</h1>
              <h2>
                Connections:{" "}
                {node.connections.map((item) => {
                  let found = nodes.find((node) => node.node_id === item);
                  return found.name + " ";
                })}{" "}
              </h2>
              <div>


                <div>{renderEVDropdown(node)}</div>
              </div>
            </div>
          );
        })}
    </div>
  );
}

export default NodeList;