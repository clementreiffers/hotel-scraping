import "./SearchHotels.css"
import React from "react";
import {Field, Submit} from "./Fields";

class SearchHotels extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            city:null,
            startDate:null,
            endDate:null,
            rooms:null,
            children:null,
            adults:null
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

    }

    render() {
        return (
            <div className="divForm">
                <form onSubmit={this.handleSubmit}>
                    <Field value={this.state.city} onChange={this.handleChange} name="city" type="text">city</Field>
                    <Field value={this.state.adults} onChange={this.handleChange} name="adults" type="number">adults</Field>
                    <Field value={this.state.children} onChange={this.handleChange} name="children" type="number">children</Field>
                    <Field value={this.state.rooms} onChange={this.handleChange} name="rooms" type="number">rooms</Field>
                    <Field value={this.state.startDate} onChange={this.handleChange} name="startDate" type="date">start date</Field>
                    <Field value={this.state.endDate} onChange={this.handleChange} name="endDate" type="date">end date</Field>
                    <Submit city={this.state.city}
                            adults={this.state.adults}
                            children={this.state.children}
                            rooms={this.state.rooms}
                            startDate={this.state.startDate}
                            endDate={this.state.endDate} />
                </form>
                {JSON.stringify(this.state)}
            </div>
        );
    }
}

export default SearchHotels;