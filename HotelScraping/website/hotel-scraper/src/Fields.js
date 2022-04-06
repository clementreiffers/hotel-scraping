import React from "react";
import {useNavigate} from "react-router-dom";

export const Field = ({name, value, onChange, type, children}) => {
    return <div className="form-group">
        <label htmlFor={name}>{children}</label>
        <input type={type} className={name} name={name} id={name} value={value}
               onChange={onChange}/>
    </div>
}

export const Submit = ({city, adults, children, rooms, startDate, endDate}) => {
    const navigate = useNavigate();
    return (
        <button onClick={() => navigate(
            "/ShowResults?city="+city+"&adults="+adults+"&children="+children+"&rooms="+rooms+"&startDate="+startDate+"&endDate="+endDate
        )}>valider</button>
    )
};
