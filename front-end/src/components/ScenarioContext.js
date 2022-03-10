import React from 'react'
import {  useState, createContext } from 'react'




export const ScenarioContext = createContext();

const ScenarioProvider = (props) => {

    const [scenario, setScenario] = useState({scenario_id:'default', name: ''});
    
    return (
      <ScenarioContext.Provider value={[scenario, setScenario]}>
      {props.children}
      </ScenarioContext.Provider>
    );
}

export default ScenarioProvider