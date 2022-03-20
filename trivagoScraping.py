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


# def getHotels(names, grades, prices, links, index):
#     name = names[index].text
#     grade = grades[index].get_attribute("content")
#     price = prices[index].text
#     localisations = driver.find_elements(by="xpath", value="//p[@itemprop='price']")
#     localisation = localisations[index].text
#     # link =
#     print(name + ", " + grade + ", " + price + ", " + localisation)
#     return [name, grade, price, localisation, "Links"]


# def clickAddressButton(addressesButtons, index):
#     addressesButtons[index].click()
#     hotelPolicyButtons = driver.find_elements(by="xpath", value="button[@data-testid='hotel-policies-show-more']")
#     hotelPolicyButtons[index].click()

def copyHotelsToCsvLoop(fileName):
    time.sleep(2)
    # driver.find_element(by="xpath", value="//label[@data-title='Hotel']").click()
    cf.createCsv(["name", "grade", "price", "localisation", "link"], fileName)
    nextPageButtonPresent = True
    while nextPageButtonPresent:
        getHotels()
        # cf.appendToCsv(getHotels(), "bookingCom.csv")
        try:
            driver.find_element(by="xpath", value="//button[@data-testid='next-result-page']").click()
            print("Next page")
        except:
            print("No more page to get hotels from")
            nextPageButtonPresent = False


def getHotels():
    time.sleep(4)
    clickAllLocalisationButtons()
    names = getHotelsName()
    grades = getHotelsGrade()
    prices = getHotelsPrice()
    locations = getHotelsLocation()
    # links = getHotelsLink()
    # for link in links:
    #     print(link)


def clickAllLocalisationButtons():
    addressesButtons = driver.find_elements(by="xpath", value="//button[@data-testid='distance-label-section']")
    for addressButton in addressesButtons:
        time.sleep(1)
        addressButton.click()
    showHotelsPoliciesButtons = driver.find_elements(by="xpath",
                                                     value="//button[@data-testid='hotel-policies-show-more']")
    for showHotelPoliciesButton in showHotelsPoliciesButtons:
        time.sleep(1)
        showHotelPoliciesButton.click()


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
        map(lambda localisation: localisation.text,
            driver.find_elements(by="xpath", value="//span[@itemprop='streetAddress']")))


# def getHotelsLink():
    # return list(
    #     map(lambda link: link, driver.find_elements_by_link_text("Official Homepage")))
    # return list(
    #     map(lambda link: link.get, driver.find_elements(by="xpath", value="//[@aitemprop='url']")))
    # return list(
    #     map(lambda link: link.get_attribute("href"), driver.find_elements(by="xpath", value="//[@aitemprop='url']")))

    # def copyHotelsToCsvLoop(fileName):
    # time.sleep(2)
    # driver.find_element(by="xpath", value="//label[@data-title='Hotel']").click()
    # cf.createCsv(["name", "grade", "price", "localisation", "link"], fileName)
    # nextPageButtonPresent = True
    # while nextPageButtonPresent:
    #     time.sleep(8)
    #     hotelsList = driver.find_elements(by="xpath", value="//li[@data-testid='accommodation-list-element']")
    #
    #     hostelList = driver.find_elements(by="class name", value="fb01724e5b")
    #     names = list(map(lambda hotel: hotel.text.split("\n")[0], hostelList))
    #     links = list(map(lambda hotel: hotel.get_attribute("href"), hostelList))
    #     grades = list(map(lambda grade: grade.text + "/10",
    #                       driver.find_elements(by="xpath", value="//div[contains(@class, '_9c5f726ff bd528f9ea6')]")))
    #     prices = list(map(lambda price: price.text.split(" ")[1],
    #                       driver.find_elements(by="xpath", value="//span[contains(@class, 'fde444d7ef _e885fdc12')]")))
    #     localisations = list(map(lambda address: cf.getLocalisationFromAdd(address.text),
    #                              driver.find_elements(by="xpath", value="//span[contains(@data-testid, 'address')]")))
    #
    #     return [names, grades, prices, localisations, links]

    # names = driver.find_elements(by="xpath", value="//button[@data-testid='item-name']")
    # grades = driver.find_elements(by="xpath", value="//meta[@itemprop='ratingValue']")
    # prices = driver.find_elements(by="xpath", value="//p[@itemprop='price']")
    # # addressesLocationButton = driver.find_elements(by="xpath",
    # #                                                value="//button[@data-testid='distance-label-section']")
    # index = 0
    # for hotel in hotelsList:
    #     time.sleep(2)
    #     # clickAddressButton(addressesLocationButton, index)
    #     getHotels(names, grades, prices, "f", index)
    #     # cf.appendToCsv(copyHotelsDataFromResearch(names, "f", "f", "f", "f", index), fileName)
    #     index += 1
    # try:
    #     driver.find_element(by="xpath", value="//button[@data-testid='next-result-page']").click()
    # except:
    #     print("No more page to get hotels from")
    #     nextPageButtonPresent = False


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    # driver.get("https://www.trivago.com")
    # selectHoteltab()
    # writeCity("Paris")
    # selectDate('2022-04-19')
    # selectDate('2022-04-20')
    # selectGhests(5, 4, 5)

    driver.get("https://www.trivago.com/en-US/lm/hotels-paris-france?search=101-2;200-22235;dr-20220331-20220401")
    copyHotelsToCsvLoop('trivagoScraping.csv')
    # driver.close()
