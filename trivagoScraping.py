#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Mar  19 11:37:12 2022

@author: QuentinM
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time
import commonFunctions as cf

monthDictionnary = {
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


def selectHoteltab():
    time.sleep(2)
    listButtons = driver.find_elements(by="tag name", value="label")
    for button in listButtons:
        if button.text == "Hotel":
            button.click()


def writeCity(city):
    time.sleep(2)
    driver.find_element(by="id", value="input-auto-complete").send_keys(city)
    time.sleep(2)
    driver.find_element(by="id", value="react-autowhatever-1--item-0").click()


def selectDate(dateChosen):
    time.sleep(2)
    try:
        driver.find_element(by="xpath", value="//time[@datetime='" + dateChosen + "']") \
            .find_element(by="xpath", value="..") \
            .click()
    except:
        dateChosenArr = dateChosen.split('-')
        dateCalendar = driver.find_element(by="xpath", value="//button[contains(@class, 'cursor-auto font-bold')]") \
            .text.split(' ')
        while dateCalendar[1] != dateChosenArr[1] and dateCalendar[1] != dateChosenArr[1]:
            time.sleep(2)
            driver.find_element(by="xpath", value="//button[@data-testid='calendar-button-next']").click()
            dateCalendar = driver.find_element(by="xpath", value="//button[contains(@class, 'cursor-auto font-bold')]") \
                .text.split(' ')
            dateCalendar = [dateCalendar[1], monthDictionnary[dateCalendar[0]]]

        time.sleep(2)
        driver.find_element(by="xpath", value="//time[@datetime='" + dateChosen + "']") \
            .find_element(by="xpath", value="..") \
            .click()


def selectGhests(adultsNumber, childrenNumber, roomsNumber):
    time.sleep(2)
    driver.find_element(by="id", value="number-input-12").click()
    driver.find_element(by="id", value="number-input-12").send_keys(Keys.CONTROL + 'a')
    driver.find_element(by="id", value="number-input-12").send_keys(adultsNumber)
    time.sleep(2)
    driver.find_element(by="id", value="number-input-13").click()
    driver.find_element(by="id", value="number-input-13").send_keys(Keys.CONTROL + 'a')
    driver.find_element(by="id", value="number-input-13").send_keys(childrenNumber)
    time.sleep(2)
    driver.find_element(by="id", value="number-input-14").click()
    driver.find_element(by="id", value="number-input-14").send_keys(Keys.CONTROL + 'a')
    driver.find_element(by="id", value="number-input-14").send_keys(roomsNumber)
    time.sleep(2)
    driver.find_element(by="xpath", value="//button[@data-testid='search-button']").click()


def copyHotelsToCsvLoop(fileName):
    time.sleep(2)
    driver.find_element(by="xpath", value="//label[@data-title='Hotel']").click() #Click hotel view filter
    time.sleep(2)
    driver.find_element(by="xpath", value="//button[@data-testid='switch-view-button-desktop']").click() # Click map cross
    time.sleep(2)
    cf.createCsv(["name", "grade", "price", "localisation", "link"], fileName)
    nextPageButtonPresent = True
    while nextPageButtonPresent:
        # cf.appendToCsv(getHotels(), fileName)
        getHotels()
        print("Hotels data have been written")
        try:
            driver.find_element(by="xpath", value="//button[@data-testid='next-result-page']").click()
            print("No more hotels to scan, changing page.")
        except:
            print("No more pages to get hotels' data from.")
            nextPageButtonPresent = False


def getHotels():
    time.sleep(4)
    clickAllLocalisationButtons()
    names = getHotelsName()
    grades = getHotelsGrade()
    prices = getHotelsPrice()
    locations = getHotelsLocation()
    links = getHotelsLink()
    return [names, grades, prices, locations, links]


def clickAllLocalisationButtons():
    addressesButtons = driver.find_elements(by="xpath", value="//button[@data-testid='distance-label-section']")
    for addressButton in addressesButtons:
        time.sleep(0.5)
        addressButton.click()
    # showHotelsPoliciesButtons = driver.find_elements(by="xpath",
    #                                                  value="//button[@data-testid='hotel-policies-show-more']")
    # for showHotelPoliciesButton in showHotelsPoliciesButtons:
    #     time.sleep(0.5)
    #     showHotelPoliciesButton.click()


def getHotelsName():
    return list(
        map(lambda name: name.text, driver.find_elements(by="xpath", value="//button[@data-testid='item-name']")))


def getHotelsGrade():
    return list(
        map(lambda grade: grade.text, driver.find_elements(by="xpath", value="//span[@itemprop='ratingValue']")))


def getHotelsPrice():
    return list(
        map(lambda price: price.text, driver.find_elements(by="xpath", value="//p[@itemprop='price']")))


def getHotelsLocation():
    return list(
        map(lambda location: location.text,
            driver.find_elements(by="xpath", value="//address[@data-testid='info-slideout-map-address']")))
    # return list(
    #     map(lambda localisation: localisation.text,
    #         driver.find_elements(by="xpath", value="//span[@itemprop='streetAddress']")))


def getHotelsLink():
    return list(
        map(lambda link: link.get_attribute("href"), driver.find_elements(by="xpath", value="//a[@itemprop='url']")))


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://www.trivago.com")
    selectHoteltab()
    writeCity("Paris")
    selectDate('2022-04-20')
    selectDate('2022-04-21')
    selectGhests(5, 4, 5)
    copyHotelsToCsvLoop("trivagoScraping.csv")
    driver.close()
