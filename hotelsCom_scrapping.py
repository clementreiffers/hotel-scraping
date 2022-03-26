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
import folium
import webbrowser
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from geopy.geocoders import Nominatim
from selenium.webdriver.support.wait import WebDriverWait

import commonFunctions

# éléments de recherche

city = "Paris"
date = "11/07/2022"
current_date = datetime.date.today()
nb_adulte = "2"
nb_enfant = "0"

date_day, date_month, date_year = commonFunctions.separateDate(date)
date_month_year = str(date_month) +" "+ str(date_year)

current_date_month_year =commonFunctions.monthCorrespondances.get("0"+str(current_date.month))+" "+ str(current_date.year)


# ouverture de la page
driver = webdriver.Firefox()
driver.get("https://fr.hotels.com/")
time.sleep(5)

# acceptation des cookies
driver.find_element(by = "xpath" , value = "//button[@class='osano-cm-accept-all osano-cm-buttons__button osano-cm-button osano-cm-button--type_accept']").click()
time.sleep(5)

# configuration de la recherche

driver.find_element(by = "xpath", value = "//div[@class='uitk-field has-floatedLabel-label has-no-placeholder']").click()

time.sleep(5)
search_dest = driver.find_element(by = "id", value="location-field-destination")
dest = search_dest.send_keys(city, Keys.ENTER)
time.sleep(5)


driver.find_element(by = "id", value = "d1-btn").click()
time.sleep(2)

date_text = driver.find_element(by = "xpath", value = "//h2[@class='uitk-date-picker-month-name uitk-type-medium']").text
button_list = driver.find_elements(by="xpath", value="//button[@class='uitk-button uitk-button-medium uitk-button-only-icon uitk-layout-flex-item uitk-button-paging']")


while date_text != current_date_month_year:
    button_list[0].click()
    date_text = driver.find_element(by="xpath", value = "//h2[@class='uitk-date-picker-month-name uitk-type-medium']").text
    print(date_text)

while date_text != date_month_year:
    button_list[1].click()
    date_text = driver.find_element(by="xpath", value = "//h2[@class='uitk-date-picker-month-name uitk-type-medium']").text
    print(date_text)

select_date = driver.find_element(by = "xpath", value="//button[@data-day='11']").click()

driver.find_element(by = "xpath", value = "//button[@class='uitk-button uitk-button-medium uitk-button-has-text uitk-button-primary uitk-layout-flex-item uitk-layout-flex-item-flex-shrink-0 dialog-done']").click()

driver.find_element(by = "xpath", value = "//button[@aria-label='1 chambre, 2 pers.']").click()

adulte = driver.find_element(by = "xpath", value = "//input[@id='adult-input-0']").get_attribute("value")
enfant = driver.find_element(by = "xpath", value = "//input[@id='child-input-0']").get_attribute("value")

btn = driver.find_elements(by = "xpath", value = "//button[@class='uitk-layout-flex-item uitk-step-input-touch-target']")

while adulte != "1":
    btn[0].click()
    adulte = driver.find_element(by="xpath", value="//input[@id='adult-input-0']").get_attribute("value")

while adulte < nb_adulte:
    btn[1].click()
    adulte = driver.find_element(by="xpath", value="//input[@id='adult-input-0']").get_attribute("value")

while enfant != "0":
    btn[3].click()
    enfant = driver.find_element(by="xpath", value="//input[@id='child-input-0']").get_attribute("value")

while enfant < nb_enfant:
    btn[4].click()
    enfant = driver.find_element(by="xpath", value="//input[@id='child-input-0']").get_attribute("value")

select = driver.find_element(by = "xpath", value = "//button[@class='uitk-button uitk-button-large uitk-button-fullWidth uitk-button-has-text uitk-button-primary uitk-button-floating-full-width']").click()

# rechercher
driver.find_element(by = "xpath", value="//button[@class='uitk-button uitk-button-large uitk-button-fullWidth uitk-button-has-text uitk-button-primary']").click()
time.sleep(15)

# Scrap

i = 0

while i < 10:
    more = driver.find_element(by="xpath", value="//button[@data-stid='show-more-results']")
    driver.execute_script("arguments[0].click();", more)
    time.sleep(3)
    i += 1


for i in range(20):
    driver.find_element(by = "css selector", value = "body").send_keys(Keys.PAGE_DOWN)

    

link_list = driver.find_elements(by="xpath", value="//a[@class = 'listing__link uitk-card-link']")


prices = list(map(lambda price: price.text, driver.find_elements(by="xpath", value="//div[contains(@class, 'uitk-text uitk-type-600 uitk-type-bold uitk-text-emphasis-theme')]")))
print(len(prices))

#grade = list(map(lambda note: note.text, driver.find_elements(by="xpath", value="//span[contains(@class, 'uitk-type-300 uitk-type-bold all-r-padding-one')]")))
#print(grade)
#print(len(grade))

name = list(map(lambda hotel: hotel.text, driver.find_elements(by="xpath", value="//h3[contains(@class, 'uitk-heading-5 truncate-lines-2 all-b-padding-half pwa-theme--grey-900 uitk-type-heading-500')]")))
print(len(name))

links = list(map(lambda hotel_link: hotel_link.get_attribute("href"), driver.find_elements(by="xpath", value="//a[contains(@class, 'listing__link uitk-card-link')]")))
print(len(links))

address = []
stars = []
localisation = []
grade = []

for link in link_list:
    print(link_list.index(link))

    driver.execute_script("arguments[0].click();", link)

    driver.implicitly_wait(15)

# Changer de fenêtre
    
    driver.switch_to.window(driver.window_handles[1])

# Scrap name, address, stars

    address_hotel = driver.find_element(by = "xpath",value = "//div[@class='uitk-text uitk-type-300 uitk-layout-flex-item uitk-layout-flex-item-flex-basis-full_width uitk-text-default-theme']").text


    grade_text = driver.find_element(by = "xpath", value = "//h3[@class='uitk-heading-5 uitk-spacing uitk-spacing-padding-blockend-three']").text
    grades_extraction = re.search('([0-9]+),([0-9]+)', grade_text)
    if grades_extraction == None:
        grades = None
    else:
        grades= grades_extraction.group(0)

    span_list = driver.find_elements(by = "xpath", value = "//span[@class='is-visually-hidden']")
    star_text = span_list[10].get_attribute("innerHTML")
    if len(star_text) > 30:
        stars_hotel = '0'
    else:
        stars_hotel = re.search('([0-9]+)\.([0-9]+)', star_text).group(0)

# ajout aux listes

    grade.append(grades)
    address.append(address_hotel)
    stars.append(stars_hotel)

# on ferme l'onglet 
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

localisation = list(map(lambda add: commonFunctions.getLocalisationFromAdd(add) if address is not None else np.nan, address))

print(len(grade))
print(len(stars))
print(len(address))
print(len(localisation))

df = pd.DataFrame(list(zip(name,grade,stars, prices,address,localisation, links)),columns=['hotel_name','note', 'stars', 'price', 'address', 'localisation','link'])

# création du CSV

df.to_csv("hotelsCom1.csv")

""""
# création de la carte

df_carte = pd.read_csv("hotelsCom.csv")


carte = folium.Map([48.850928, 2.346260], zoom_start=100)


z = df_carte['hotel_name']
x = df_carte['latitude']
y = df_carte['longitude']

for i in range(len(x)):
    folium.Marker([x[i],y[i]],popup=z[i]).add_to(carte)
    
carte.save('Carte_hotel.html')
webbrowser.open("Carte_hotel.html")

"""