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


def nextResearchHotelPage():
    driver.find_element(by="xpath", value="//button[@data-testid='next-result-page']").click()


def copyHotelsDataFromResearch(names, grades, prices, localisations, links, index):
    name = names[index].text
    print(name)
    # grade =
    # price =
    # localisation =
    # link =
    # return [name, grade, price, localisation, link]
    return [name, "Grade", "Price", "Localisations", "Links"]


def copyHotelsToCsvLoop(fileName):
    time.sleep(2)
    cf.createCsv(["name", "grade", "price", "localisation", "link"], fileName)
    nexPageButtonPresent = True
    while nexPageButtonPresent:
        hotelsList = driver.find_elements(by="xpath", value="//li[@data-testid='accommodation-list-element']")
        time.sleep(10)
        for hotel in hotelsList:
            time.sleep(2)
            copyHotelsDataFromResearch(hotel)
            # cf.appendToCsv(copyHotelsDataFromResearch(hotel), fileName)
        try:
            nextResearchHotelPage()
        except:
            print("No more page to get hotels from")
            nexPageButtonPresent = False


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    # driver.get("https://www.trivago.com")

    driver.get("https://www.trivago.com/en-US/lm/hotels-paris-france?search=200-22235;dr-20220419-20220420")
    time.sleep(10)
    hotelsList = driver.find_elements(by="xpath", value="//li[@data-testid='accommodation-list-element']")
    names = driver.find_elements(by="xpath", value="//button[@data-testid='item-name']")
    index = 0
    for hotel in hotelsList:
        time.sleep(2)
        copyHotelsDataFromResearch(names, "f", "f", "f", "f", index)
        index += 1
        # cf.appendToCsv(copyHotelsDataFromResearch(hotel), fileName)

    # selectHoteltab()
    # writeCity("Paris")
    # selectDate('2022-04-19')
    # selectDate('2022-04-20')
    # selectGhests(5, 4, 5)
    # copyHotelsToCsvLoop('trivagoScraping.csv')
    driver.close()
