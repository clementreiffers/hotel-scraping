import * as R from "ramda";
import * as fs from "fs";

const splitData_ = R.pipe(
    R.split("\n"),
    R.map(R.split(";"))
);

const splitGps_ = R.pipe(
    R.without("]"),
    R.without("["),
    R.join(''),
    R.split(",")
);

const getLongitude = R.pipe(
    R.slice(4, 5),
    splitGps_,
    R.last
);

const getLatitude = R.pipe(
    R.slice(1,10),
    // splitGps_,
    // R.head
);
const transformDataToJsonLike_ = R.applySpec({
    name: R.head,
    stars: R.slice(1, 2),
    grade: R.slice(2, 3),
    price: R.slice(3, 4),
    longitude: R.pipe(getLongitude),
    latitude: R.pipe(getLatitude),
    link: R.last
});

const getJson = R.pipe(
    splitData_,
    R.map(transformDataToJsonLike_)
);

const data = fs.readFileSync('./bookingCom.csv',
    {encoding: 'utf8', flag: 'r'});


console.log(getJson(data));

// console.log(getLongitude("[555,444]"))