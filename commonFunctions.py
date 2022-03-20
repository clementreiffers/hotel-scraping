import csv
from geopy.geocoders import Nominatim

monthCorrespondances = {
    "01": "janvier",
    "02": "fevrier",
    "03": "mars",
    "04": "avril",
    "05": "mai",
    "06": "juin",
    "07": "juillet",
    "08": "aout",
    "09": "septembre",
    "10": "octobre",
    "11": "novembre",
    "12": "decembre",
}


def addRows(infos, file, isHead=False):
    if isHead:
        csv.writer(file).writerow(infos)
    else:
        for j in range(len(infos[0]) - 1):
            rowCsv = []
            for i in range(len(infos)):
                rowCsv.append(infos[i][j])
                print(i, j)
            csv.writer(file).writerow(rowCsv)
    file.close()


def createCsv(infos, file):
    f = open(file, 'w')
    addRows(infos, f, True)


def appendToCsv(infos, file):
    f = open(file, "a")
    addRows(infos, f)


def getLocalisationFromAdd(add):
    geolocator = Nominatim(user_agent="main")
    location = geolocator.geocode(add)
    return [location.latitude, location.longitude]


def separateDate(date):
    """
    :param date: dd/MM/yyyy
    """
    day, month, year = date.split("/")
    month = monthCorrespondances[month]
    return day, month, year
