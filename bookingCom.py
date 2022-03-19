import time

from selenium import webdriver

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


def searchCity(city):
    time.sleep(2)
    driver.find_element(by="id", value="ss").send_keys(city)

    time.sleep(2)
    driver.find_element(by="class name", value="sb-searchbox__button ").click()


def separateDate(date):
    """
    :param date: dd/MM/yyyy
    """
    day, month, year = date.split("/")
    month = monthCorrespondances[month]
    return day, month, year


def getByXpath(xpath):
    return driver.find_element(by="xpath",
                               value=xpath)


def acceptCookies():
    time.sleep(2)
    driver.find_element(by="id", value="onetrust-accept-btn-handler").click()


def setDate(date):
    """
    :param date: dd/MM/yyyy
    """
    day, month, year = separateDate(date)
    requestedDate = " ".join((day, month, year))

    # valeur de la fleche pour choisir les dates mais pas utile pour le moment car
    # c'est affiche par default
    # driver.find_elements(by="xpath", value="//div[contains(@class, 'bk-icon -streamline-arrow_nav_down sb-date-field__icon-arrow-down')]")

    # permet de scroller quand on n'a pas le bon mois affiché
    isGoodMonthShows = False
    while not isGoodMonthShows:
        time.sleep(5)
        xpathCalendar = "//div[contains(@aria-live, 'polite')]"
        currentDate = getByXpath(xpathCalendar).text

        print("month '{}', year '{}', current date '{}'".format(month, year, currentDate))

        if month in currentDate and year in currentDate:
            isGoodMonthShows = True
        else:
            try:
                getByXpath("//button[contains(@class, 'd40f3b0d6d f5ea4b08ab')]").click()
            except:
                print("j'ai eu un pb je suis passe par la div")
                getByXpath(
                    "//*[local-name()='div' and contains(@class, 'bui-calendar__control bui-calendar__control--next')]").click()
                print(driver.find_element(by="css selector", value="bui-calendar__wrapper").text)
    xpathDay = "//span[contains(@aria-hidden, 'true') and contains(text(), '19')]"
    # xpathDay = "//p[contains(@id, 'onetrust-policy-text')]"
    getByXpath(xpathDay).click()


def getHotels():
    time.sleep(2)
    hostelList = driver.find_elements(by="class name", value="fb01724e5b")
    hostelsNames = list(map(lambda hotel: hotel.text.split("\n")[0], hostelList))
    hostelsLinks = list(map(lambda hotel: hotel.get_attribute("href"), hostelList))
    grades = list(map(lambda grade: grade.text, getByXpath("//div[contains(@class, '_9c5f726ff bd528f9ea6')]")))


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get(
        "https://www.booking.com/index.fr.html?label=gen173nr-1BCAEoggI46AdIM1gEaE2IAQGYAQ24ARfIAQzYAQHoAQGIAgGoAgO4Arf4yJEGwAIB0gIkNmMwYWYwNGUtNGY3Ni00ZTk3LThjOGUtZWQ0OTEwMDZkZGMw2AIF4AIB;sid=4870985d274b91999c83d2a5d6f77393;keep_landing=1&sb_price_type=total&")

    acceptCookies()
    searchCity("Paris")
    setDate("20/05/2022")
