#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Mar  19 11:37:12 2022

@author: QuentinM
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import commonFunctions as cf
import numpy as np


def click_cookies_button():
    time.sleep(2)
    driver.find_element(by="id", value="onetrust-accept-btn-handler").click()


def select_hotel_tab():
    time.sleep(2)
    list_buttons = driver.find_elements(by="tag name", value="label")
    for button in list_buttons:
        if button.text == "Hôtel":
            button.click()


def write_city(city):
    time.sleep(2)
    driver.find_element(by="id", value="input-auto-complete").send_keys(city)
    time.sleep(2)
    driver.find_element(by="id", value="react-autowhatever-1--item-0").click()


def select_date(date_chosen):
    date_chosen = date_format_eu_to_us(date_chosen)
    time.sleep(2)
    try:
        driver.find_element(by="xpath", value="//time[@datetime='" + date_chosen + "']") \
            .find_element(by="xpath", value="..") \
            .click()
    except:
        date_chosen_arr = date_chosen.split('-')
        date_calendar = driver.find_element(by="xpath", value="//button[contains(@class, 'cursor-auto font-bold')]") \
            .text.split(' ')
        while date_calendar[1] != date_chosen_arr[1] and date_calendar[1] != date_chosen_arr[1]:
            time.sleep(2)
            driver.find_element(by="xpath", value="//button[@data-testid='calendar-button-next']").click()
            date_calendar = driver.find_element(by="xpath", value="//button[contains(@class, 'cursor-auto font-bold')]") \
                .text.split(' ')
            date_calendar = [date_calendar[1], cf.month_digits_dictionary[date_calendar[0]]]

        time.sleep(2)
        driver.find_element(by="xpath", value="//time[@datetime='" + date_chosen + "']") \
            .find_element(by="xpath", value="..") \
            .click()


def date_format_eu_to_us(date):
    date = list(reversed(date.split('-')))
    return date[0] + '-' + date[1] + '-' + date[2]


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
    driver.find_element(by="xpath", value="//label[@data-title='Hôtel']").click()  # Click hotel view filter
    time.sleep(2)
    driver.find_element(by="xpath",
                        value="//button[@data-testid='switch-view-button-desktop']").click()  # Click map cross
    time.sleep(2)
    cf.createCsv(["name", "grade", "stars", "price", "location", "gps", "link"], file_name)
    next_page_button_present = True
    while next_page_button_present:
        cf.appendToCsv(get_hotels(), file_name)
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
    locations_list = get_hotels_location()
    return [get_hotels_name(), get_hotels_grade(), get_hotels_stars(), locations_list, get_hotels_gps(locations_list),
            get_hotels_link()]


def click_all_localisation_buttons():
    addresses_buttons = driver.find_elements(by="xpath", value="//button[@data-testid='distance-label-section']")
    for addressButton in addresses_buttons:
        time.sleep(0.5)
        addressButton.click()
    show_hotels_policies_buttons = driver \
        .find_elements(by="xpath", value="//button[@data-testid='hotel-policies-show-more']")
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


def get_hotels_gps(locations_list):
    return list(
        map(lambda location: cf.getLocalisationFromAdd(location), locations_list))


def get_hotels_link():
    return list(
        map(lambda link: link.get_attribute("href"), driver.find_elements(by="xpath", value="//a[@itemprop='url']")))


def get_hotels_stars():
    accomodation_type_list = driver.find_elements(by="xpath", value="//button[@data-testid='accommodation-type']")
    stars_hotels_list = []
    for accomodation_type in accomodation_type_list:
        try:
            stars_hotels_list \
                .append(accomodation_type.find_element(by="xpath", value="./span/span/meta[@itemprop='ratingValue']") \
                        .get_attribute("content"))
        except:
            stars_hotels_list.append(np.nan)
    return stars_hotels_list


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://www.trivago.fr")
    click_cookies_button()
    select_hotel_tab()
    write_city("Paris")
    select_date('20-04-2022')
    select_date('21-04-2022')
    select_ghests(5, 4, 5)
    copy_hotels_to_csv_loop("trivagoScraping.csv")
    driver.close()
