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


def select_hotel_tab():
    time.sleep(2)
    list_buttons = driver.find_elements(by="tag name", value="label")
    for button in list_buttons:
        if button.text == "Hotel":
            button.click()


def write_city(city):
    time.sleep(2)
    driver.find_element(by="id", value="input-auto-complete").send_keys(city)
    time.sleep(2)
    driver.find_element(by="id", value="react-autowhatever-1--item-0").click()


def select_date(date_choosen):
    time.sleep(2)
    try:
        driver.find_element(by="xpath", value="//time[@datetime='" + date_choosen + "']") \
            .find_element(by="xpath", value="..") \
            .click()
    except:
        date_chosen_arr = date_choosen.split('-')
        date_calendar = driver.find_element(by="xpath", value="//button[contains(@class, 'cursor-auto font-bold')]") \
            .text.split(' ')
        while date_calendar[1] != date_chosen_arr[1] and date_calendar[1] != date_chosen_arr[1]:
            time.sleep(2)
            driver.find_element(by="xpath", value="//button[@data-testid='calendar-button-next']").click()
            date_calendar = driver.find_element(by="xpath", value="//button[contains(@class, 'cursor-auto font-bold')]") \
                .text.split(' ')
            date_calendar = [date_calendar[1], monthDictionnary[date_calendar[0]]]

        time.sleep(2)
        driver.find_element(by="xpath", value="//time[@datetime='" + date_choosen + "']") \
            .find_element(by="xpath", value="..") \
            .click()


def select_ghests(adults_number, children_number, rooms_number):
    time.sleep(2)
    driver.find_element(by="id", value="number-input-12").click()
    driver.find_element(by="id", value="number-input-12").send_keys(Keys.CONTROL + 'a')
    driver.find_element(by="id", value="number-input-12").send_keys(adults_number)
    time.sleep(2)
    driver.find_element(by="id", value="number-input-13").click()
    driver.find_element(by="id", value="number-input-13").send_keys(Keys.CONTROL + 'a')
    driver.find_element(by="id", value="number-input-13").send_keys(children_number)
    time.sleep(2)
    driver.find_element(by="id", value="number-input-14").click()
    driver.find_element(by="id", value="number-input-14").send_keys(Keys.CONTROL + 'a')
    driver.find_element(by="id", value="number-input-14").send_keys(rooms_number)
    time.sleep(2)
    driver.find_element(by="xpath", value="//button[@data-testid='search-button']").click()


def copy_hotels_to_csv_loop(file_name):
    time.sleep(2)
    driver.find_element(by="xpath", value="//label[@data-title='Hotel']").click()  # Click hotel view filter
    time.sleep(2)
    driver.find_element(by="xpath",
                        value="//button[@data-testid='switch-view-button-desktop']").click()  # Click map cross
    time.sleep(2)
    # cf.createCsv(["name", "grade", "price", "localisation", "link", "stars"], fileName)
    cf.createCsv(["name", "grade", "price", "localisation", "link"], file_name)
    next_page_button_present = True
    while next_page_button_present:
        cf.appendToCsv(get_hotels(), file_name)
        # getHotels()
        print("Hotels data have been written")
        try:
            driver.find_element(by="xpath", value="//button[@data-testid='next-result-page']").click()
            print("No more hotels to scan, changing page.")
        except:
            print("No more pages to get hotels' data from.")
            next_page_button_present = False


def get_hotels():
    time.sleep(4)
    click_all_localisation_buttons()
    names_list = get_hotels_name()
    grades_list = get_hotels_grade()
    prices_list = get_hotels_price()
    locations_list = get_hotels_location()
    links_list = get_hotels_link()
    stars_list = get_hotels_stars()
    # offerLinksList =
    # for stars in starsList:
    #     print(stars)
    # chamberLink = getHotelsChamberLin()
    # return [namesList, gradesList, pricesList, locationsList, linksList, stars_list]
    return [names_list, grades_list, prices_list, locations_list, links_list]


def click_all_localisation_buttons():
    addresses_buttons = driver.find_elements(by="xpath", value="//button[@data-testid='distance-label-section']")
    for addressButton in addresses_buttons:
        time.sleep(0.5)
        addressButton.click()
    show_hotels_policies_buttons = driver.find_elements(by="xpath",
                                                     value="//button[@data-testid='hotel-policies-show-more']")
    for showHotelPoliciesButton in show_hotels_policies_buttons:
        time.sleep(0.5)
        showHotelPoliciesButton.click()


def get_hotels_name():
    return list(
        map(lambda name: name.text, driver.find_elements(by="xpath", value="//button[@data-testid='item-name']")))


def get_hotels_grade():
    return list(
        map(lambda grade: grade.text, driver.find_elements(by="xpath", value="//span[@itemprop='ratingValue']")))


def get_hotels_price():
    return list(
        map(lambda price: price.text, driver.find_elements(by="xpath", value="//p[@itemprop='price']")))


def get_hotels_location():
    return list(
        map(lambda location: location.text,
            driver.find_elements(by="xpath", value="//address[@data-testid='info-slideout-map-address']")))
    # return list(
    #     map(lambda localisation: localisation.text,
    #         driver.find_elements(by="xpath", value="//span[@itemprop='streetAddress']")))


def get_hotels_link():
    return list(
        map(lambda link: link.get_attribute("href"), driver.find_elements(by="xpath", value="//a[@itemprop='url']")))


def get_hotels_stars():
    return list(
        map(lambda star_grade: star_grade.get_attribute('content'),
            driver.find_elements(by="xpath", value="//meta[@itemprop='ratingValue']")))


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://www.trivago.com")
    select_hotel_tab()
    write_city("Paris")
    select_date('2022-04-20')
    select_date('2022-04-21')
    select_ghests(5, 4, 5)
    copy_hotels_to_csv_loop("trivagoScraping.csv")
    driver.close()
