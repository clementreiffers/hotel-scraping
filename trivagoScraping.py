#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Mar  19 11:37:12 2022

@author: QuentinM
"""

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

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time


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


def copyHotelsDataFromResearch():
    print("")


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://www.trivago.com")
    selectHoteltab()
    writeCity("Paris")
    selectDate('2022-07-19')
    selectDate('2022-07-20')
    selectGhests(5, 4, 5)
    copyHotelsDataFromResearch()
    # driver.close()
