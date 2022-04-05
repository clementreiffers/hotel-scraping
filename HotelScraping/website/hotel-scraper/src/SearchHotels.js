import "./SearchHotels.css"
import React from "react";

class SearchHotels extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            search:'',
            startDate:'',
            endDate:'',
            rooms:0,
            children:0,
            adults:0
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;

        this.setState({
            [name]: value
        });
    }

    handleSubmit(event) {
        /*
        ici il faudra renvoyer this.state qui definie precisement la recherche
         */

        alert("recherche : " + this.state);
        console.table(this.state);
        event.preventDefault();
    }

    render() {
        return (
            <div className="divForm">
                <form onSubmit={this.handleSubmit}>

                    <input type="search" className="search" name="value" value={this.state.value} onChange={this.handleChange}/>
                    <input type="number" className="nbr" name="adults" value={this.state.adults} onChange={this.handleChange}/>
                    <input type="number" className="nbr" name="children" value={this.state.children} onChange={this.handleChange}/>
                    <input type="number" className="nbr" name="rooms" value={this.state.rooms} onChange={this.handleChange}/>
                    <div className="dates">
                        <input type="date" className="date" name="startDate" value={this.state.startDate} onChange={this.handleChange}/>
                        <input type="date" className="date" name="endDate" value={this.state.endDate} onChange={this.handleChange}/>
                    </div>
                    <input type="submit" className="submit" />
                </form>
            </div>
        )
            ;
    }
}

export default SearchHotels;