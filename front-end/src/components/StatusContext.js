import {useState, createContext} from 'react'
import React from 'react'



export const StatusContext = createContext();

const StatusProvider = (props) => {

    const [status, setStatus] = useState("")
    
    return (
      <StatusContext.Provider value={[status, setStatus]}>
      {props.children}
      </StatusContext.Provider>
    );
}

export default StatusProvider