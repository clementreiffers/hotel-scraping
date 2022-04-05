import "./SearchHotels.css"
import React from "react";
import Field from "./Fields";

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
                    <Field value={this.state.search} onChange={this.handleChange} name="search" type="text">search</Field>
                    <Field value={this.state.adults} onChange={this.handleChange} name="adults" type="number">adults</Field>
                    <Field value={this.state.children} onChange={this.handleChange} name="children" type="number">children</Field>
                    <Field value={this.state.rooms} onChange={this.handleChange} name="rooms" type="number">rooms</Field>
                    <Field value={this.state.startDate} onChange={this.handleChange} name="start_date" type="date">start date</Field>
                    <Field value={this.state.endDate} onChange={this.handleChange} name="end_date" type="date">end date</Field>
                    <input type="submit" className="submit" />
                </form>
                {JSON.stringify(this.state)}
            </div>
        );
    }
}

export default SearchHotels;