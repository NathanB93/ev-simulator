import './App.css';
import React from 'react'
import Network from './components/Network';
import ScenarioProvider from './components/ScenarioContext';
import Results from './components/Results';
import StatusProvider from './components/StatusContext';
import NavBar from './components/NavBar';




function App() {





  return (

        <StatusProvider>
        <ScenarioProvider>


        <div className="container">
          
        <div className = "header">
          <NavBar/>
        </div>
          
        <div className= "sidepanel">

        <Network/>

        </div>
        

        
        <div className= "resultspanel">

        <Results/>
        
        </div>

        </div>
      
    </ScenarioProvider>
    </StatusProvider>
   
      
      
      
      
    
    
  );
}

export default App;