import * as R from "ramda";
import * as fs from "fs";

// to read 'input.txt' file
const data = fs.readFileSync('./bookingCom.csv',
    {encoding:'utf8', flag:'r'});

console.log(data);