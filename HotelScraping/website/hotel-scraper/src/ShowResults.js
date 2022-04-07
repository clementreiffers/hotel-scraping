import "./SearchHotels.css"
import React, {useState} from "react";
import * as R from "ramda";
import * as XLSX from "xlsx";

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
            city:R.nth(0),
            adults:R.nth(1),
            children: R.nth(2),
            rooms:R.nth(3),
            startDate:R.nth(4),
            endDate:R.nth(5)
        })
    )

function App() {
    const [items, setItems] = useState([]);

    const readExcel = (file) => {
        const promise = new Promise((resolve, reject) => {
            const fileReader = new FileReader();
            fileReader.readAsArrayBuffer(file);

            fileReader.onload = (e) => {
                const bufferArray = e.target.result;

                const wb = XLSX.read(bufferArray, { type: "buffer" });

                const wsname = wb.SheetNames[0];

                const ws = wb.Sheets[wsname];

                const data = XLSX.utils.sheet_to_json(ws);

                resolve(data);
            };

            fileReader.onerror = (error) => {
                reject(error);
            };
        });

        promise.then((d) => {
            setItems(d);
        });
    };

    return (
        <div>
            <input
                type="file"
                onChange={(e) => {
                    const file = e.target.files[0];
                    readExcel(file);
                }}
            />

            <table class="table container">
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