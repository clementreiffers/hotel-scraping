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
        const promise = new Promise((resolve, reject) => {
            const df = dfd.readCSV(filename)
                .then((d) => {
                    /*
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

                    data["!ref"] = "A1:" + code*/

                    let ws = {}
                    // initialisation des colonnes
                    /*
                    let char = 'A';
                    let code = char + 1;
                    for (let col of d["columns"]) {
                        ws[code] = {
                            "t": "s",
                            "v": col,
                            "r": "<t>" + col + "</t>",
                            "h": col,
                            "w": col
                        }
                        char = String.fromCharCode(char.charCodeAt(0) + 1);
                        code = char + 1;
                    }

                     */
                    // initialisation des values
                    let nbr = 2;
                    let char = "A";
                    let code = char + nbr;
                    for (let col of d["columns"]) {
                        nbr = 2;
                        code = char + nbr;
                        for (let value of d[col].values) {
                            ws[code] = {
                                "t": "n",
                                "v": value,
                                "w": "" + value
                            }
                            nbr++;
                            code = char + nbr;
                        }
                        char = String.fromCharCode(char.charCodeAt(0) + 1);
                    }
                    char = "A";
                    let data = []
                    // console.log(ws);
                    // on veut incrementer le numero
                    let n = 2;
                    while (n < nbr) {
                        code = char + n
                        // console.log(n);
                        // on veut incrementer la lettre
                        let temp = {}
                        for (let nbrChar in d["columns"]) {
                            temp[d["columns"][n]] = 1;
                            console.log(d["columns"][n])
                            char = String.fromCharCode("A".charCodeAt(0) + nbrChar);
                            code = char + nbr;
                        }
                        // console.log("temp");
                        data.push(temp);
                        console.log(data);
                        n++;
                    }
                    setItems(data);
                });

        })
        // items.map((d)=> console.log(d));
        // console.log(items);
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

/*
function App() {
   const [items, setItems] = useState([]);

   const readExcel = (file) => {
       const promise = new Promise((resolve, reject) => {
           const fileReader = new FileReader();
           fileReader.readAsArrayBuffer(file);

           fileReader.onload = (e) => {
               const bufferArray = e.target.result;

               const wb = XLSX.read(bufferArray, {type: "buffer"});

               const wsname = wb.SheetNames[0];

               const ws = {
                   "!ref": "A1:C4",
                   "A1": {
                       "t": "s",
                       "v": "Item",
                       "r": "<t>Item</t>",
                       "h": "Item",
                       "w": "Item"
                   },
                   "B1": {
                       "t": "s",
                       "v": "Description",
                       "r": "<t>Description</t>",
                       "h": "Description",
                       "w": "Description"
                   },
                   "C1": {
                       "t": "s",
                       "v": "Qtt",
                       "r": "<t>Qtt</t>",
                       "h": "Qtt",
                       "w": "Qtt"
                   },
                   "A2": {
                       "t": "n",
                       "v": 1,
                       "w": "1"
                   },
                   "B2": {
                       "t": "n",
                       "v": 2,
                       "w": "2"
                   },
                   "C2": {
                       "t": "n",
                       "v": 3,
                       "w": "3"
                   },
                   "A3": {
                       "t": "n",
                       "v": 1,
                       "w": "1"
                   },
                   "B3": {
                       "t": "n",
                       "v": 2,
                       "w": "2"
                   },
                   "C3": {
                       "t": "n",
                       "v": 3,
                       "w": "3"
                   },
                   "A4": {
                       "t": "n",
                       "v": 1,
                       "w": "1"
                   },
                   "B4": {
                       "t": "n",
                       "v": 2,
                       "w": "2"
                   },
                   "C4": {
                       "t": "n",
                       "v": 3,
                       "w": "3"
                   }
               }

               const data = XLSX.utils.sheet_to_json(ws);
               console.log(data);
               resolve(data);
           };

           fileReader.onerror = (error) => {
               reject(error);
           };
       });
       const test = [
           {
               "Item": 1,
               "Description": 2,
               "Qtt": 3
           },
           {
               "Item": 1,
               "Description": 2,
               "Qtt": 3
           },
           {
               "Item": 1,
               "Description": 2,
               "Qtt": 3
           }
       ]

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
                   <th scope="col">Item</th>
                   <th scope="col">Description</th>
                   <th scope="col">Qtt</th>
               </tr>
               </thead>
               <tbody>
               {items.map((d) => (
                   <tr key={d.Item}>
                       <th>{d.Item}</th>
                       <td>{d.Description}</td>
                       <td>{d.Qtt}</td>
                   </tr>
               ))}
               </tbody>
           </table>
       </div>
   );
}
*/

export default App;