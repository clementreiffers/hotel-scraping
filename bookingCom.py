import time

import numpy as np
from selenium import webdriver
import commonFunctions as cf

driver = webdriver.Firefox()


def search_city(city):
    time.sleep(2)
    driver.find_element(by="id", value="ss").send_keys(city)

    time.sleep(2)
    driver.find_element(by="class name", value="sb-searchbox__button ").click()


def get_by_xpath(xpath):
    return driver.find_element(by="xpath",
                               value=xpath)


def accept_cookies():
    time.sleep(2)
    driver.find_element(by="id", value="onetrust-accept-btn-handler").click()


def set_good_month_year(month, year):
    # we can choose the correct month but we need the calendar open
    is_good_month_shows = False
    while not is_good_month_shows:
        time.sleep(2)
        xpath_calendar = "//div[contains(@aria-live, 'polite')]"
        current_date = get_by_xpath(xpath_calendar).text
        if len(current_date) == 0:
            current_date = driver.find_element(by="xpath", value="//*[contains(@class, 'bui-calendar__wrapper')]")
            current_date = current_date.text.split(" ")[0:2]
            current_date[1] = str(''.join(i for i in current_date[1] if i.isdigit()))

        if month in current_date and year in current_date:
            is_good_month_shows = True
        else:
            try:
                get_by_xpath("//button[contains(@class, 'd40f3b0d6d f5ea4b08ab')]").click()
            except:
                get_by_xpath(
                    "//*[local-name()='div' and contains(@class, 'bui-calendar__control bui-calendar__control--next')]").click()


def show_calendar():
    try:
        driver.find_element(by="xpath", value="//div[contains(@class, 'sb-date-field__display')]").click()
    except:
        driver.find_element(by="xpath", value="//button[contains(@data-testid, 'date-display-field-end')]").click()


def select_day(day):
    # permet de scroller quand on n'a pas le bon mois affiché
    xpathDay = "//span[contains(@aria-hidden, 'true') and contains(text(), '{}')]".format(day)
    get_by_xpath(xpathDay).click()


def set_date(start_date, end_date):
    """
    :param end_date:
    :param start_date:
    """
    start_day, start_month, start_year = cf.separateDate(start_date)
    end_day, end_month, end_year = cf.separateDate(end_date)

    set_good_month_year(start_month, start_year)

    select_day(start_day)

    show_calendar()

    set_good_month_year(end_month, end_year)

    select_day(end_day)


def getHotels():
    time.sleep(2)
    hostel_list = driver.find_elements(by="class name", value="fb01724e5b")
    names = list(map(lambda hotel: hotel.text.split("\n")[0], hostel_list))
    links = list(map(lambda hotel: hotel.get_attribute("href"), hostel_list))
    grades = list(map(lambda grade: grade.text + "/10",
                      driver.find_elements(by="xpath", value="//div[contains(@class, '_9c5f726ff bd528f9ea6')]")))
    prices = list(map(lambda price: price.text.split(" ")[1],
                      driver.find_elements(by="xpath", value="//span[contains(@class, 'fde444d7ef _e885fdc12')]")))
    localisations = list(map(lambda address: cf.getLocalisationFromAdd(address.text),
                             driver.find_elements(by="xpath", value="//span[contains(@data-testid, 'address')]")))

    cards = driver.find_elements(by="xpath", value="//div[contains(@data-testid, 'property-card')]")

    stars = []
    for i in cards:
        nbr_stars = i.find_elements(by="xpath", value='./*//div[contains(@data-testid, "rating-stars")]/span')
        stars.append(len(nbr_stars) if nbr_stars else np.nan)
    return [names, stars, grades, prices, localisations, links]


def applyFamilyAndDate():
    try:
        driver.find_element(by="xpath", value="//button[contains(@class, 'sb-searchbox__button')]").click()
    except:
        driver.find_element(by="xpath", value="//button[contains(@type, 'submit')]").click()


def changePage():
    time.sleep(2)
    driver.find_element(by="xpath", value="//button[contains(@aria-label, 'Page suivante')]").click()


def main(infos, filename):
    """
    :param filename: example.csv
    :param infos: [city, start_date, end_date]
    :return:
    """
    city, start_date, end_date = infos[0], infos[1], infos[2]

    driver.get(
        "https://www.booking.com/index.fr.html?label=gen173nr-1BCAEoggI46AdIM1gEaE2IAQGYAQ24ARfIAQzYAQHoAQGIAgGoAgO4Arf4yJEGwAIB0gIkNmMwYWYwNGUtNGY3Ni00ZTk3LThjOGUtZWQ0OTEwMDZkZGMw2AIF4AIB;sid=4870985d274b91999c83d2a5d6f77393;keep_landing=1&sb_price_type=total&")
    accept_cookies()

    search_city(city)
    set_date(start_date, end_date)
    applyFamilyAndDate()

    cf.createCsv(["name", "stars", "grade", "price", "localisation", "link"], 'bookingCom.csv')

    while True:
        cf.appendToCsv(getHotels(), filename)

        changePage()


if __name__ == '__main__':
    main(["paris", "20/05/2022", "23/05/2022"], "bookingCom.csv")
    driver.close()
