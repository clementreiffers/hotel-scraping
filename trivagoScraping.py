#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Mar  19 11:37:12 2022

@author: QuentinM
"""

# Dictionnary
monthCorrespondances = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
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


def selectDate(dateChoosen):
    time.sleep(2)
    try:
        driver.find_element(by="xpath", value="//time[@datetime='" + dateChoosen + "']") \
            .find_element(by="xpath", value="..") \
            .click()
    except:
        dateChoosen = dateChoosen.split('-')
        dateChoosen = datetime.date(int(dateChoosen[0]), int(dateChoosen[1]), int(dateChoosen[2]))
        dateCalendar = driver.find_element(by="xpath", value="//button[contains(@class, 'cursor-auto font-bold')]") \
            .text.split(' ')
        # dateCalendar = datetime.date(int(dateCalendar[0]), int(dateCalendar[1]), 1)
        month = dateCalendar[0]
        year = dateCalendar[1]
        while month not in dateChoosen and year not in dateChoosen:
            # Go to next page

# pageDate = driver.find_element(by="xpath",value="//div[@data-testid='calendar-popover']/")
# if pageDate < currentYear:
#     exit('Selected date is behind the current date')
# else:
#     while pageDate < currentYear:
# Press next button

# time.sleep(2)
# driver.find_element(by="xpath", value="//time[@datetime='" + checkOutDate + "']") \
#     .find_element(by="xpath", value="..").click()


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
    selectDate('2022-03-19')
    selectDate('2022-03-20')
    # selectGhests(5, 4, 5)
    # copyHotelsDataFromResearch()
    # driver.close()
