import * as R from "ramda";
import * as fs from "fs";

const splitData_ = R.pipe(
    R.split("\n"),
    R.map(R.split(";"))
);

const cleanArrayGps_ = R.pipe(
    R.nth(4),
    R.split(","),
    R.map(R.match(/[0-9].[0-9]{7}/))
);

const getLongitude = R.pipe(
    cleanArrayGps_,
    R.last,
    R.head
);

const getLatitude = R.pipe(
    cleanArrayGps_,
    R.head,
    R.head
);

const transformDataToJsonLike_ = R.applySpec({
    name: R.head,
    grade: R.nth(1),
    stars: R.nth(2),
    address: R.nth(3),
    latitude: getLatitude,
    longitude: getLongitude,
    link: R.last
});


const getJson = R.pipe(
    splitData_,
    R.drop(1),
    R.map(transformDataToJsonLike_),
);


const getData = (filename) => {
    return fs.readFileSync(filename,
        {encoding: 'utf8', flag: 'r'});
};

console.log(getJson(getData("bookingCom.csv")))

export {getData, getJson}



