import csv
import numpy as np
from geopy.geocoders import Nominatim

# maybe create an english for certain cases
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


def addRows(infos, file, is_head=False):
    """
    :param infos: all infos you want to put in
    :param file: File object you want to write in
    :param is_head: True if you just want to put 1 line
    :return: None
    """
    if is_head:
        csv.writer(file).writerow(infos)
    else:
        for j in range(len(infos[0])):
            csv.writer(file).writerow([infos[i][j] for i in range(len(infos))])
    file.close()


def createCsv(infos, file):
    """
    :param infos: send the head of the csv ex : ["name", "grade", "price", "localisation", "link"]
    :param file: the name of the file you want to create ex: "test.csv"
    :return: None
    """
    f = open(file, 'w')
    addRows(infos, f, True)


def appendToCsv(infos, file):
    """
    :param infos: [[allNames], [allGrades],[allPrices], [allLocalisations], [allLinks]]
    :param file: name of the csv ex : "file.csv"
    :return: None
    """
    f = open(file, "a")
    addRows(infos, f)


def getLocalisationFromAdd(add):
    """
    :param add: "address_hotel"
    :return: [latitude, longitude] else None
    """
    location = Nominatim(user_agent="main").geocode(add)
    return [location.latitude, location.longitude] if location is not None else np.nan


def separateDate(date):
    """
    :param date: dd/MM/yyyy
    :return: day, month, year
    """
    day, month, year = date.split("/")
    month = monthCorrespondances[month]
    return day, month, year
