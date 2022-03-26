import * as R from "ramda";
import * as fs from "fs";

const splitData_ = R.pipe(
    R.split("\n"),
    R.map(R.split(";"))
);

const splitGps_ = R.pipe(
    R.join(''),
    R.split(","),
);

const getLongitude = R.pipe(
    R.slice(4, 5),
    splitGps_,
    R.last,
    R.replace("]", ""),
);

const getLatitude = R.pipe(
    R.slice(4, 5),
    splitGps_,
    R.head,
    R.replace("[", ""),
);

const getGrade_ = R.pipe(
    R.slice(1, 2),
    R.head
)

const getStars_ = R.pipe(
    R.slice(2, 3),
    R.head
)

const getAddresses_ = R.pipe(
    R.slice(3, 4),
    R.head
)

const transformDataToJsonLike_ = R.applySpec({
    name: R.head,
    grade: getGrade_,
    stars: getStars_,
    address: getAddresses_,
    latitude: getLatitude,
    longitude: getLongitude,
    link: R.last
});

const getJson = R.pipe(
    splitData_,
    R.drop(1),
    R.map(transformDataToJsonLike_),
);

const data = fs.readFileSync('./bookingCom.csv',
    {encoding: 'utf8', flag: 'r'});


console.log(getJson(data))


// console.log(getJson(data));
// console.log(R.length(data));
// console.log(getLongitude("[555,444]"))