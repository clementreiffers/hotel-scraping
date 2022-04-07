import * as R from "ramda";
import * as fs from "fs";
import {find} from "ramda";

const splitData_ = R.pipe(
    R.split("\r\n"),
    R.map(R.split(";"))
);

const transformDataToJsonLike_ = R.applySpec({
    name: R.head,
    grade: R.nth(1),
    stars: R.nth(2),
    prices: R.nth(3),
    address: R.nth(4),
    gps: R.nth(5),
    start_date: R.nth(6),
    end_date: R.nth(7),
    adults: R.nth(8),
    children: R.nth(9),
    rooms: R.nth(10),
    link: R.last
});


const getJson = R.pipe(
    splitData_,
    R.map(transformDataToJsonLike_)
);

const data = fs.readFileSync('../../../csv/csv_par_site/booking_general.csv',
    {encoding: 'utf8', flag: 'r'});

//console.log(getJson(data));


const findElements = (columnName, value, list) => {
    return R.filter(R.propEq(columnName, value), list);
};

//console.log(findElements("name","Moris Grands Boulevards",getJson(data)));

function getHotelsFromDic(dictionary) {
    let filtered = getJson(data);
    for (let key in dictionary) {
        filtered = findElements(key, dictionary[key], filtered);
    }
    return filtered;
}

fetch("booking_general.csv").then(data =>console.log(data.text()))