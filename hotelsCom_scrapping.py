# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 21:57:06 2022

@author: ACER
"""


### scrap hotel.com    https://fr.hotels.com/


##df_hotel : nom ,note, nombre étoile, prix, address, localisation, link


import time
import datetime
import re
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import commonFunctions
monthCorrespondances = {
    "01": "janvier",
    "02": "février",
    "03": "mars",
    "04": "avril",
    "05": "mai",
    "06": "juin",
    "07": "juillet",
    "08": "août",
    "09": "septembre",
    "10": "octobre",
    "11": "novembre",
    "12": "décembre",
}

def separateDate(date):
    """
    :param date: dd/MM/yyyy
    :return: day, month, year
    """
    day, month, year = date.split("/")
    month = monthCorrespondances[month]
    return day, month, year

# éléments de recherche

city = "Paris"
date_set = "11/05/2023"
current_date = datetime.date.today()
nb_adulte = "2"
nb_enfant = "2"

date_day, date_month, date_year = separateDate(date_set)
date_month_year = str(date_month) + " " + str(date_year)

current_date_month_year = monthCorrespondances.get("0" + str(current_date.month)) + " " + str(
    current_date.year)

# ouverture de la page
driver = webdriver.Firefox()
driver.get("https://fr.hotels.com/")
time.sleep(5)

# acceptation des cookies
driver.find_element(by="xpath",
                    value="//button[@class='osano-cm-accept-all osano-cm-buttons__button osano-cm-button osano-cm-button--type_accept']").click()
time.sleep(5)

# configuration de la recherche

driver.find_element(by="xpath", value="//div[@class='uitk-field has-floatedLabel-label has-no-placeholder']").click()

time.sleep(5)
search_dest = driver.find_element(by="id", value="location-field-destination")
dest = search_dest.send_keys(city, Keys.ENTER)
time.sleep(5)

driver.find_element(by="id", value="d1-btn").click()
time.sleep(2)

date_text = driver.find_element(by="xpath", value="//h2[@class='uitk-date-picker-month-name uitk-type-medium']").text
button_list = driver.find_elements(by="xpath",
                                   value="//button[@class='uitk-button uitk-button-medium uitk-button-only-icon uitk-layout-flex-item uitk-button-paging']")

while date_text != current_date_month_year:
    button_list[0].click()
    date_text = driver.find_element(by="xpath",
                                    value="//h2[@class='uitk-date-picker-month-name uitk-type-medium']").text



while date_text != date_month_year:
    button_list[1].click()
    date_text = driver.find_element(by="xpath",
                                    value="//h2[@class='uitk-date-picker-month-name uitk-type-medium']").text


select_date = driver.find_element(by="xpath", value="//button[@data-day='11']").click()

driver.find_element(by="xpath",
                    value="//button[@class='uitk-button uitk-button-medium uitk-button-has-text uitk-button-primary uitk-layout-flex-item uitk-layout-flex-item-flex-shrink-0 dialog-done']").click()

driver.find_element(by="xpath", value="//button[@aria-label='1 chambre, 2 pers.']").click()

adulte = driver.find_element(by="xpath", value="//input[@id='adult-input-0']").get_attribute("value")
enfant = driver.find_element(by="xpath", value="//input[@id='child-input-0']").get_attribute("value")

btn = driver.find_elements(by="xpath", value="//button[@class='uitk-layout-flex-item uitk-step-input-touch-target']")

while adulte != "1":
    btn[0].click()
    adulte = driver.find_element(by="xpath", value="//input[@id='adult-input-0']").get_attribute("value")

while adulte < nb_adulte:
    btn[1].click()
    adulte = driver.find_element(by="xpath", value="//input[@id='adult-input-0']").get_attribute("value")

while enfant != "0":
    btn[2].click()
    enfant = driver.find_element(by="xpath", value="//input[@id='child-input-0']").get_attribute("value")

while enfant < nb_enfant:
    btn[3].click()
    enfant = driver.find_element(by="xpath", value="//input[@id='child-input-0']").get_attribute("value")

if nb_enfant == "2":
    select_element = driver.find_element(by="id", value='child-age-input-0-0')
    select_object = Select(select_element)
    select_object.select_by_index(10)
    select_element = driver.find_element(by="id", value='child-age-input-0-1')
    select_object = Select(select_element)
    select_object.select_by_index(5)

driver.find_element(by="xpath",
                             value="//button[@class='uitk-button uitk-button-large uitk-button-fullWidth uitk-button-has-text uitk-button-primary uitk-button-floating-full-width']").click()

# rechercher
driver.find_element(by="xpath",
                    value="//button[@class='uitk-button uitk-button-large uitk-button-fullWidth uitk-button-has-text uitk-button-primary']").click()
time.sleep(15)


# Scrap

i = 0

while i < 10:
    more = driver.find_element(by="xpath", value="//button[@data-stid='show-more-results']")
    driver.execute_script("arguments[0].click();", more)
    time.sleep(3)
    i += 1

for i in range(20):
    driver.find_element(by="css selector", value="body").send_keys(Keys.PAGE_DOWN)

link_list = driver.find_elements(by="xpath", value="//a[@class = 'listing__link uitk-card-link']")

prices = list(map(lambda price: price.text, driver.find_elements(by="xpath",
                                                                 value="//div[contains(@class, 'uitk-text uitk-type-600 uitk-type-bold uitk-text-emphasis-theme')]")))


# grade = list(map(lambda note: note.text, driver.find_elements(by="xpath", value="//span[contains(@class, 'uitk-type-300 uitk-type-bold all-r-padding-one')]")))
# print(grade)
# print(len(grade))

name = list(map(lambda hotel: hotel.text, driver.find_elements(by="xpath",
                                                               value="//h3[contains(@class, 'uitk-heading-5 truncate-lines-2 all-b-padding-half pwa-theme--grey-900 uitk-type-heading-500')]")))


links = list(map(lambda hotel_link: hotel_link.get_attribute("href"),
                 driver.find_elements(by="xpath", value="//a[contains(@class, 'listing__link uitk-card-link')]")))


address = []
stars = []
localisation = []
grade = []
date = []
nb_personne = []

print(len(name))

for link in link_list:
    print(link_list.index(link))

    driver.execute_script("arguments[0].click();", link)

    driver.implicitly_wait(20)

    # Changer de fenêtre

    driver.switch_to.window(driver.window_handles[1])

    # Scrap name, address, stars

    address_hotel = driver.find_element(by="xpath",
                                        value="//div[@class='uitk-text uitk-type-300 uitk-layout-flex-item uitk-layout-flex-item-flex-basis-full_width uitk-text-default-theme']").text

    grade_text = driver.find_element(by="xpath",
                                     value="//h3[@class='uitk-heading-5 uitk-spacing uitk-spacing-padding-blockend-three']").text
    grades_extraction = re.search('([0-9]+),([0-9]+)', grade_text)
    if grades_extraction == None:
        grades = None
    else:
        grades = grades_extraction.group(0)

    span_list = driver.find_elements(by="xpath", value="//span[@class='is-visually-hidden']")
    star_text = span_list[10].get_attribute("innerHTML")
    star = re.search('([0-9]+)\.([0-9]+)', star_text)
    if star == None:
        stars_hotel = '0'
    else:
        stars_hotel = star.group(0)

    # ajout aux listes

    grade.append(grades)
    address.append(address_hotel)
    stars.append(stars_hotel)
    date.append(date_set)
    nb_personne.append(int(nb_adulte)+int(nb_enfant))

    # on ferme l'onglet

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

localisation = list(
    map(lambda add: commonFunctions.getLocalisationFromAdd(add) if address is not None else np.nan, address))


df = pd.DataFrame(list(zip(name, grade, stars, prices, address, localisation, date, nb_personne, links)),
                  columns=['name', 'grade','stars', 'prices','address', 'gps', 'date', 'nb_personne', 'link' ])

# création du CSV

df.to_csv("csv/hotelsCom/hotelsCom_Mai2023_4.csv",index = False, sep=";")
