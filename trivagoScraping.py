#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Mar  19 11:37:12 2022

@author: QuentinM
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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


def selectDate(checkInDate, checkOutDate):
    time.sleep(2)
    driver.find_element(by="xpath", value="//time[@datetime='" + checkInDate + "']").find_element(by="xpath",
                                                                                                  value="..").click()
    time.sleep(2)
    driver.find_element(by="xpath", value="//time[@datetime='" + checkOutDate + "']").find_element(by="xpath",
                                                                                                   value="..").click()


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


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://www.trivago.com")
    selectHoteltab()
    writeCity("Paris")
    selectDate('2022-04-13', '2022-04-14')
    selectGhests(5, 4, 5)
    driver.close()

    # datesListPage = driver.find_elements(by="tag name", value="time")
    # for dateCheckIn in datesListPage:
    #     if dateCheckIn.get_attribute("dateTime") == checkInDate:
    #         print("Date found")
    #         dateCheckIn.click()
    # print(dateCheckIn.get_attribute("dateTime"))

    # driver.find_element("css selector", value="time[datetime='2022-04-11']").click()
    # checkInDate=datetime.strptime(checkInDate,"%d/%m/%y")
    # print(checkInDate)
    # driver.find_element(by='id',value='cal-heading-month').
    # print(driver.find_element(by="Xpath",value="//*[@id=\"cal-heading-month\"]/span").is_selected())
    # monthDate = driver.find_element(by="id",value="cal-heading-month")
    # if monthDate.text==checkInDate:
    #     driver.find_element(by="")
