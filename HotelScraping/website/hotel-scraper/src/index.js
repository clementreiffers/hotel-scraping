import React from 'react';
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import {createRoot} from "react-dom/client";
import reportWebVitals from './reportWebVitals';

import './index.css';

import SearchHotels from "./SearchHotels";
import ShowResults from "./ShowResults";

const container = document.getElementById("root")
const root = createRoot(container);
root.render(
    <Router>
        <Routes>
            <Route path="/" element={<SearchHotels />}/>
            <Route path="/ShowResults" element={<ShowResults />}/>
        </Routes>
    </Router>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
