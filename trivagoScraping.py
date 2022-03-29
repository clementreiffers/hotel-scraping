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
    driver.find_element(by="xpath", value="//label[@data-title='Hôtel']").click()


def write_city(city):
    time.sleep(2)
    driver.find_element(by="id", value="input-auto-complete").send_keys(city)
    time.sleep(2)
    driver.find_element(by="id", value="react-autowhatever-1--item-0").click()


def select_date(date_chosen):
    time.sleep(2)
    date_chosen = cf.date_format_eu_to_us(date_chosen)
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


def select_guests(adults_number, children_number, rooms_number):
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
    driver.find_element(by="xpath", value="//button[@data-testid='guest-selector-apply']").click()


def validate_research():
    driver.find_element(by="xpath", value="//button[@data-testid='search-button']").click()


def copy_hotels_to_csv_loop(file_name):
    time.sleep(2)
    driver.find_element(by="xpath", value="//label[@data-title='Hôtel']").click()  # Click hotel view filter
    time.sleep(2)
    driver.find_element(by="xpath",
                        value="//button[@data-testid='switch-view-button-desktop']").click()  # Click map cross
    time.sleep(2)
    next_page_button_present = True
    while next_page_button_present:

        get_hotels(file_name)
        scroll_page()
        print("Hotels data have been written")
        try:
            driver.find_element(by="xpath", value="//button[@data-testid='next-result-page']").click()
            print("No more hotels to scan, changing page.")
        except:
            next_page_button_present = False
            print("No more pages to get hotels' data from.")


def get_hotels(file_name):
    click_all_localisation_buttons()
    locations_list = get_hotels_location()
    cf.addRows(
        names=get_hotels_name(),
        stars=get_hotels_stars(),
        gps=get_hotels_gps(locations_list),
        prices=get_hotels_price(),
        addresses=locations_list,
        links=get_hotels_link(),
        grades=get_hotels_grade(),
        filename=file_name,
        is_head=int(get_current_page()) == 1)


def click_all_localisation_buttons():
    time.sleep(2)
    addresses_buttons = driver.find_elements(by="xpath", value="//button[@data-testid='distance-label-section']")
    for addressButton in addresses_buttons:
        time.sleep(1)
        addressButton.click()
    show_hotels_policies_buttons = driver \
        .find_elements(by="xpath", value="//button[@data-testid='hotel-policies-show-more']")
    for showHotelPoliciesButton in show_hotels_policies_buttons:
        time.sleep(1)
        showHotelPoliciesButton.click()


def scroll_page():
    driver.find_element(by="css selector", value="body").send_keys(Keys.CONTROL, Keys.END)
    time.sleep(2)


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
    accommodation_type_list = driver.find_elements(by="xpath", value="//button[@data-testid='accommodation-type']")
    stars_hotels_list = []
    for accommodation_type in accommodation_type_list:
        try:
            stars_hotels_list \
                .append(accommodation_type.find_element(by="xpath", value="./span/span/meta[@itemprop='ratingValue']") \
                        .get_attribute("content"))
        except:
            stars_hotels_list.append(np.nan)
    return stars_hotels_list


def get_current_page():
    try:
        return driver.find_element(by="xpath", value="//button[@aria-current='page']").text
    except:
        return "1"


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://www.trivago.fr")
    click_cookies_button()
    select_hotel_tab()
    write_city("Paris")
    select_date('20-04-2022')
    select_date('21-04-2022')
    select_guests(5, 4, 5)
    validate_research()
    copy_hotels_to_csv_loop("trivagoScraping.csv")
    driver.close()
