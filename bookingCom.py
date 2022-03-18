from selenium import webdriver
import time


def searchCity(city):
    time.sleep(2)
    driver.find_element(by="id", value="ss").send_keys(city)

    time.sleep(2)
    driver.find_element(by="class name", value="sb-searchbox__button ").click()

def setDate(date):
    ...

def getHotels():
    time.sleep(2)
    hostelList = driver.find_elements(by="class name", value="fb01724e5b")
    hostelsNames = list(map(lambda hotel: hotel.text.split("\n")[0], hostelList))
    hostelsLinks = list(map(lambda hotel: hotel.get_attribute("href"), hostelList))
    grades = list(map(lambda grade: grade.text,
                      driver.find_elements(by="xpath", value="//div[contains(@class, '_9c5f726ff bd528f9ea6')]")))


if __name__ == '__main__':
    driver = webdriver.Firefox()

    driver.get(
        "https://www.booking.com/index.fr.html?label=gen173nr-1BCAEoggI46AdIM1gEaE2IAQGYAQ24ARfIAQzYAQHoAQGIAgGoAgO4Arf4yJEGwAIB0gIkNmMwYWYwNGUtNGY3Ni00ZTk3LThjOGUtZWQ0OTEwMDZkZGMw2AIF4AIB;sid=4870985d274b91999c83d2a5d6f77393;keep_landing=1&sb_price_type=total&")

    searchCity("Paris")
    getHotels()
