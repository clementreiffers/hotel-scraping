import time
import csv
from selenium import webdriver
import commonFunctions as cf


def searchCity(city):
    time.sleep(2)
    driver.find_element(by="id", value="ss").send_keys(city)

    time.sleep(2)
    driver.find_element(by="class name", value="sb-searchbox__button ").click()


def getByXpath(xpath):
    return driver.find_element(by="xpath",
                               value=xpath)


def acceptCookies():
    time.sleep(2)
    driver.find_element(by="id", value="onetrust-accept-btn-handler").click()


def setGoodMonthYear(month, year):
    # we can choose the correct month but we need the calendar open
    isGoodMonthShows = False
    while not isGoodMonthShows:
        time.sleep(2)
        xpathCalendar = "//div[contains(@aria-live, 'polite')]"
        currentDate = getByXpath(xpathCalendar).text
        if len(currentDate) == 0:
            currentDate = driver.find_element(by="xpath", value="//*[contains(@class, 'bui-calendar__wrapper')]")
            currentDate = currentDate.text.split(" ")[0:2]
            currentDate[1] = str(''.join(i for i in currentDate[1] if i.isdigit()))

        if month in currentDate and year in currentDate:
            isGoodMonthShows = True
        else:
            try:
                getByXpath("//button[contains(@class, 'd40f3b0d6d f5ea4b08ab')]").click()
            except:
                getByXpath(
                    "//*[local-name()='div' and contains(@class, 'bui-calendar__control bui-calendar__control--next')]").click()


def showCalendar():
    try:
        driver.find_element(by="xpath", value="//div[contains(@class, 'sb-date-field__display')]").click()
    except:
        print("je suis passe par ici")
        driver.find_element(by="xpath", value="//button[contains(@data-testid, 'date-display-field-end')]").click()


def selectDay(day):
    # permet de scroller quand on n'a pas le bon mois affiché
    xpathDay = "//span[contains(@aria-hidden, 'true') and contains(text(), '{}')]".format(day)
    getByXpath(xpathDay).click()


def setDate(startDate, endDate):
    """
    :param arrivalDate: dd/MM/yyyy
    """
    startDay, startMonth, startYear = cf.separateDate(startDate)
    endDay, endMonth, endYear = cf.separateDate(endDate)

    setGoodMonthYear(startMonth, startYear)

    selectDay(startDay)

    showCalendar()

    setGoodMonthYear(endMonth, endYear)

    selectDay(endDay)


def getHotels():
    time.sleep(2)
    hostelList = driver.find_elements(by="class name", value="fb01724e5b")
    names = list(map(lambda hotel: hotel.text.split("\n")[0], hostelList))
    links = list(map(lambda hotel: hotel.get_attribute("href"), hostelList))
    grades = list(map(lambda grade: grade.text + "/10",
                      driver.find_elements(by="xpath", value="//div[contains(@class, '_9c5f726ff bd528f9ea6')]")))
    prices = list(map(lambda price: price.text.split(" ")[1],
                      driver.find_elements(by="xpath", value="//span[contains(@class, 'fde444d7ef _e885fdc12')]")))
    localisations = list(map(lambda address: cf.getLocalisationFromAdd(address.text),
                             driver.find_elements(by="xpath", value="//span[contains(@data-testid, 'address')]")))

    return [names, grades, prices, localisations, links]


def applyFamilyAndDate():
    try:
        driver.find_element(by="xpath", value="//button[contains(@class, 'sb-searchbox__button')]").click()
    except:
        driver.find_element(by="xpath", value="//button[contains(@type, 'submit')]").click()


def changePage():
    time.sleep(2)
    driver.find_element(by="xpath", value="//button[contains(@aria-label, 'Page suivante')]").click()


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get(
        "https://www.booking.com/index.fr.html?label=gen173nr-1BCAEoggI46AdIM1gEaE2IAQGYAQ24ARfIAQzYAQHoAQGIAgGoAgO4Arf4yJEGwAIB0gIkNmMwYWYwNGUtNGY3Ni00ZTk3LThjOGUtZWQ0OTEwMDZkZGMw2AIF4AIB;sid=4870985d274b91999c83d2a5d6f77393;keep_landing=1&sb_price_type=total&")

    acceptCookies()
    searchCity("Paris")
    setDate("20/05/2022", "23/05/2022")
    applyFamilyAndDate()

    cf.createCsv(["name", "grade", "price", "localisation", "link"], 'bookingCom.csv')

    while True:
        cf.appendToCsv(getHotels(), "bookingCom.csv")

        changePage()
    # cf.createCsv(["name", "grade", "price", "localisation", "link"], 'bookingCom.csv')
    # cf.appendToCsv([["test", "test2"], ["test", "test2"], ["test", "test2"], ["test", "test2"], ["test", "test2"]], "bookingCom.csv")
