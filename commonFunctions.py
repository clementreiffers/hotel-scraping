import csv
import numpy as np
from geopy.geocoders import Nominatim
import pandas as pd

# maybe create an english for certain cases
monthCorrespondances = {
    "01": "janvier",
    "02": "fevrier",
    "03": "mars",
    "04": "avril",
    "05": "mai",
    "06": "juin",
    "07": "juillet",
    "08": "août",
    "09": "septembre",
    "10": "octobre",
    "11": "novembre",
    "12": "decembre",
}

month_digits_dictionary = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12",
}


def addRows(names, stars, prices, grades, gps, addresses, start_date, end_date, links, filename, is_head):
    """
    :param end_date: the date you choose for the research
    :param start_date: the date you choose for the research
    :param prices: all prices you get from the website
    :param is_head: put True if you want to erase the existing file, False to append
    :param filename: the name of the file
    :param links: all links you get from the website
    :param addresses: all addresses you get from the website
    :param gps: all gps you get from the website
    :param grades: all grades you get from the website
    :param stars: all stars you get from the website
    :param names: all names you get from the website

    :return: None
    """
    df = pd.DataFrame(
        {
            "name": names,
            "grade": grades,
            "stars": stars,
            "prices": prices,
            "address": addresses,
            "gps": gps,
            "start_date": start_date,
            "end_date": end_date,
            "link": links,
        }
    )

    df.to_csv(filename, index=False, mode="w" if is_head else "a", sep=";")


def getLocalisationFromAdd(add):
    """
    :param add: "address_hotel"
    :return: [latitude, longitude] else None
    """
    try:
        location = Nominatim(user_agent="main").geocode(add)
        return [location.latitude, location.longitude] if location is not None else np.nan
    except:
        return np.nan


def separateDate(date):
    """
    :param date: dd/MM/yyyy
    :return: day, month, year
    """
    return date.split("/")


def separateAmericanDate(date):
    """
    :param date: MM-dd-yyyy
    :return: day, month, year
    """
    month, day, year = date.split("-")
    return day, month, year


def date_format_eu_to_us(date):
    date = list(reversed(date.split('-')))
    return date[0] + '-' + date[1] + '-' + date[2]
