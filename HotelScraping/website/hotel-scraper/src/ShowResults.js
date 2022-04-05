import "./SearchHotels.css"
import React from "react";
import {useLocation} from "react-router-dom";

const GetAllUrl = (type) => {
    const {search} = useLocation();
    for(type of ["city", "adults", "children", "rooms", "startDate", "endDate"])
        const match = search.match("/"+type+"=(.*)/")?.[1];
}

export default ShowResults;