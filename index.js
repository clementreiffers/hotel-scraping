import * as R from "ramda";
import * as fs from "fs";

const splitData = R.pipe(
    R.split("\n"),
    R.map(R.split(","))
);

const transformDataToJsonLike = R.pipe(
    
)

const data = fs.readFileSync('./bookingCom.csv',
    {encoding:'utf8', flag:'r'});

console.log(splitData(data));