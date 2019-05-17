import React from 'react';
import LineChart from './components/LineChart'
import StatsTable from './components/StatsTable'
import Navbar from './components/Navbar'
import {BrowserRouter} from "react-browser-router";
import './App.css';

function App() {
  return (
    <BrowserRouter>
    <div className="background">
      <div>
        <Navbar/>
      </div>
      <div>
        <LineChart/>
      </div>
      <div>
        <StatsTable/>
      </div>
    </div>
    </BrowserRouter>
  );
}

export default App;
