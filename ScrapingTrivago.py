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


class ScrapingTrivago:

    def __init__(self, filename, city, start_date,
                 end_date, nbr_adults, children_age_array, nbr_room):
        self.__driver = None
        self.__filename = filename
        self.__city = city
        self.__start_date = start_date
        self.__end_date = end_date
        self.__nbr_adults = nbr_adults
        self.__children_age_array = children_age_array
        self.__nbr_children = len(children_age_array)
        self.__nbr_room = nbr_room

    def __click_cookies_button(self):
        time.sleep(2)
        self.__driver.find_element(by="id", value="onetrust-accept-btn-handler").click()

    def __select_hotel_tab(self):
        time.sleep(2)
        self.__driver.find_element(by="xpath", value="//label[@data-title='Hôtel']").click()

    def __write_city(self):
        time.sleep(2)
        self.__driver.find_element(by="id", value="input-auto-complete").send_keys(self.__city)
        time.sleep(2)
        self.__driver.find_element(by="id", value="react-autowhatever-1--item-0").click()

    def __select_date(self, date_chosen):
        time.sleep(2)
        date_chosen = cf.date_format_eu_to_us(date_chosen)
        try:
            self.__driver.find_element(by="xpath", value="//time[@datetime='" + date_chosen + "']") \
                .find_element(by="xpath", value="..") \
                .click()
        except:
            date_chosen_arr = date_chosen.split('-')
            date_calendar = self.__driver.find_element(by="xpath",
                                                       value="//button[contains(@class, 'cursor-auto font-bold')]") \
                .text.split(' ')
            while date_calendar[1] != date_chosen_arr[1] and date_calendar[1] != date_chosen_arr[1]:
                time.sleep(2)
                self.__driver.find_element(by="xpath", value="//button[@data-testid='calendar-button-next']").click()
                date_calendar = self.__driver.find_element(by="xpath",
                                                           value="//button[contains(@class, 'cursor-auto font-bold')]") \
                    .text.split(' ')
                date_calendar = [date_calendar[1], cf.month_digits_dictionary[date_calendar[0]]]

            time.sleep(2)
            self.__driver.find_element(by="xpath", value="//time[@datetime='" + date_chosen + "']") \
                .find_element(by="xpath", value="..") \
                .click()

    def __select_guests(self):
        time.sleep(2)
        self.__driver.find_element(by="id", value="number-input-12").click()
        self.__driver.find_element(by="id", value="number-input-12").send_keys(Keys.CONTROL + 'a')
        self.__driver.find_element(by="id", value="number-input-12").send_keys(self.__nbr_adults)
        time.sleep(2)
        self.__driver.find_element(by="id", value="number-input-13").click()
        self.__driver.find_element(by="id", value="number-input-13").send_keys(Keys.CONTROL + 'a')
        self.__driver.find_element(by="id", value="number-input-13").send_keys(self.__nbr_children)
        time.sleep(2)
        self.__driver.find_element(by="id", value="number-input-14").click()
        self.__driver.find_element(by="id", value="number-input-14").send_keys(Keys.CONTROL + 'a')
        self.__driver.find_element(by="id", value="number-input-14").send_keys(self.__nbr_room)
        time.sleep(2)
        self.__select_children_ages()
        self.__driver.find_element(by="xpath", value="//button[@data-testid='guest-selector-apply']").click()

    def __select_children_ages(self):
        time.sleep(2)
        children_ages_select = self.__driver.find_element(by="xpath", value="//fieldset[@id='childAgeSelector']")
        children_ages_select = children_ages_select.find_elements(by="xpath", value="./ul/li/select")
        for child, age in zip(children_ages_select, self.__children_age_array):
            time.sleep(1)
            child.click()
            time.sleep(1)
            child.find_element(by="xpath", value="./option[@value='" + age + "']").click()

    def __validate_research(self):
        self.__driver.find_element(by="xpath", value="//button[@data-testid='search-button']").click()

    def __copy_hotels_to_csv_loop(self):
        time.sleep(2)
        self.__driver.find_element(by="xpath", value="//label[@data-title='Hôtel']").click()  # Click hotel view filter
        time.sleep(2)
        self.__driver.find_element(by="xpath",
                                   value="//button[@data-testid='switch-view-button-desktop']").click()  # Click map cross
        time.sleep(2)
        next_page_button_present = True
        while next_page_button_present:

            self.__get_hotels()
            # self.__scroll_page()
            print("Hotels data have been written")
            try:
                self.__driver.find_element(by="xpath", value="//button[@data-testid='next-result-page']").click()
                print("No more hotels to scan, changing page.")
            except:
                next_page_button_present = False
                print("No more pages to get hotels' data from.")

    def __get_hotels(self):
        self.__click_all_localisation_buttons()
        locations_list = self.__get_hotels_location()
        cf.addRows(
            names=self.__get_hotels_name(),
            stars=self.__get_hotels_stars(),
            prices=self.__get_hotels_price(),
            grades=self.__get_hotels_grade(),
            gps=self.__get_hotels_gps(locations_list),
            addresses=locations_list,
            start_date=self.__start_date,
            end_date=self.__end_date,
            links=self.__get_hotels_link(),
            filename=self.__filename,
            is_head=int(self.__get_current_page()) == 1,
            nb_adults=[self.__nbr_adults for _ in range(25)],
            nb_children=[self.__nbr_children for _ in range(25)],
            nb_room=[self.__nbr_room for _ in range(25)],
        )

    def __click_all_localisation_buttons(self):
        time.sleep(2)
        addresses_buttons = self.__driver.find_elements(by="xpath",
                                                        value="//button[@data-testid='distance-label-section']")
        for addressButton in addresses_buttons:
            time.sleep(1)
            addressButton.click()
        show_hotels_policies_buttons = self.__driver \
            .find_elements(by="xpath", value="//button[@data-testid='hotel-policies-show-more']")
        for showHotelPoliciesButton in show_hotels_policies_buttons:
            time.sleep(1)
            showHotelPoliciesButton.click()

    def __scroll_page(self):
        self.__driver.find_element(by="css selector", value="body").send_keys(Keys.CONTROL, Keys.END)
        time.sleep(2)

    def __get_hotels_name(self):
        return list(
            map(lambda name: name.text,
                self.__driver.find_elements(by="xpath", value="//button[@data-testid='item-name']")))

    def __get_hotels_grade(self):
        return list(
            map(lambda grade: grade.text,
                self.__driver.find_elements(by="xpath", value="//span[@itemprop='ratingValue']")))

    def __get_hotels_price(self):
        return list(
            map(lambda price: price.text, self.__driver.find_elements(by="xpath", value="//p[@itemprop='price']")))

    def __get_hotels_location(self):
        return list(
            map(lambda location: location.text,
                self.__driver.find_elements(by="xpath", value="//address[@data-testid='info-slideout-map-address']")))

    def __get_hotels_gps(self, locations_list):
        return list(
            map(lambda location: cf.getLocalisationFromAdd(location), locations_list))

    def __get_hotels_link(self):
        return list(
            map(lambda link: link.get_attribute("href"),
                self.__driver.find_elements(by="xpath", value="//a[@itemprop='url']")))

    def __get_hotels_stars(self):
        accommodation_type_list = self.__driver.find_elements(by="xpath",
                                                              value="//button[@data-testid='accommodation-type']")
        stars_hotels_list = []
        for accommodation_type in accommodation_type_list:
            try:
                stars_hotels_list \
                    .append(
                    accommodation_type.find_element(by="xpath", value="./span/span/meta[@itemprop='ratingValue']") \
                        .get_attribute("content"))
            except:
                stars_hotels_list.append(np.nan)
        return stars_hotels_list

    def __get_current_page(self):
        try:
            return self.__driver.find_element(by="xpath", value="//button[@aria-current='page']").text
        except:
            return "1"

    def main(self):
        self.__driver = webdriver.Firefox()
        self.__driver.maximize_window()
        self.__driver.get("https://www.trivago.fr")
        self.__click_cookies_button()
        self.__select_hotel_tab()
        self.__write_city()
        self.__select_date(self.__start_date)
        self.__select_date(self.__end_date)
        self.__select_guests()
        self.__validate_research()
        self.__copy_hotels_to_csv_loop()
        self.__driver.close()
        self.__driver = None


if __name__ == '__main__':
    booking_trivago = ScrapingTrivago("trivagoScraping.csv", "Paris", '20-04-2022', '21-04-2022', \
                                      2, ["10", "17", "15"], 3)
    booking_trivago.main()
