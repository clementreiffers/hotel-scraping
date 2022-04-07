import "./SearchHotels.css"
import React, {useState} from "react";
import * as R from "ramda";
import * as XLSX from "xlsx";
import * as dfd from "danfojs";

const removeTypeFromUrl = R.pipe(
    R.split("="),
    R.nth(1)
)

const getAllValuesFromUrl = R.pipe(
    R.split("?"),
    R.nth(1),
    R.split("&"),
    R.map(removeTypeFromUrl),
    R.applySpec({
        city: R.nth(0),
        adults: R.nth(1),
        children: R.nth(2),
        rooms: R.nth(3),
        startDate: R.nth(4),
        endDate: R.nth(5)
    })
)

function App() {
    const [items, setItems] = useState([]);

    const readExcel = (filename) => {
        const df = dfd.readCSV(filename)
            .then((d) => {
                    const promise = new Promise((resolve, reject) => {

                        const data = {};
                        let char = "A";
                        let number = 1;
                        let code = char + number;
                        for (let col of d["columns"]) {
                            data[code] = {t: "s", v: col, w: col};
                            number++;
                            code = char + number;
                            for (let values of d[col].values) {
                                data[code] = {t: "s", w: values, v: values}
                                number++;
                                code = char + number;
                            }
                            number = 1;
                            char = String.fromCharCode(char.charCodeAt(0) + 1)

                        }
                        resolve(data);
                    });
                    promise.then((d) => {
                            setItems(d);
                        }
                    )
                },
            )
        // items.map((d)=> console.log(d));
        console.log(items);
    }
    return (
        <div>
            {readExcel("test.csv")}
            <table className="table container">
                <thead>
                <tr>
                    <th scope="col">name</th>
                    <th scope="col">grade</th>
                </tr>
                </thead>
                <tbody>
                {items.map((d) => (
                    <tr key={d.name}>
                        <th>{d.name}</th>
                        <td>{d.grade}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );

}


export default App;