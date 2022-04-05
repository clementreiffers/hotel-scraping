import React from "react";

const Field = ({name, value, onChange, type, children}) => {
    return <div className="form-group">
            <label htmlFor={name}>{children}</label>
            <input type={type} className={name} name={name} id={name} value={value}
                   onChange={onChange}/>
        </div>
}

export default Field;
