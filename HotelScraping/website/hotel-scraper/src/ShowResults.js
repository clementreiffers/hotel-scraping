import "./SearchHotels.css"
import React from "react";
import * as R from "ramda";

class ShowResults extends React.Component {

    constructor(props) {
        super(props);

        this.state = {};
    }

    removeTypeFromUrl = R.pipe(
        R.split("="),
        R.nth(1)
    )

    getAllValuesFromUrl = R.pipe(
        R.split("?"),
        R.nth(1),
        R.split("&"),
        R.map(this.removeTypeFromUrl),
        R.applySpec({
            city:R.nth(0),
            adults:R.nth(1),
            children: R.nth(2),
            rooms:R.nth(3),
            startDate:R.nth(4),
            endDate:R.nth(5)
        })
    )

    render() {
        // eslint-disable-next-line react/no-direct-mutation-state
        this.state = this.getAllValuesFromUrl(window.location.href);
        return (
            <p>{JSON.stringify(this.state)}</p>
        );
    }
}


export default ShowResults;