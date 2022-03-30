import * as R from "ramda";
import * as fs from "fs";

const splitData_ = R.pipe(
    R.split("\n"),
    R.map(R.split(";"))
);

const transformDataToJsonLike_ = R.applySpec({
    name: R.head,
    grade: R.slice(1, 2),
    stars: R.slice(2, 3),
    address: R.slice(3, 4),
    gps: R.slice(4, 5),
    link: R.last
})

const getJson = R.pipe(
    splitData_,
    R.map(transformDataToJsonLike_)
)

const data = fs.readFileSync('./bookingCom.csv',
    {encoding: 'utf8', flag: 'r'});


console.log(getJson(data))