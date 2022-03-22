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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from geopy.geocoders import Nominatim
import commonFunctions

# éléments de recherche

city = "Paris"
date_day = "11"
date_month = "juillet 2022"
current_date = datetime.date.today()

current_date_day = current_date.day

current_date_month = current_date.month
month = "0"+str(current_date_month)
month_year = commonFunctions.monthCorrespondances.get(month) + " " + str(current_date.year)

# création du data frame

df = pd.DataFrame(columns=['hotel_name','note', 'stars', 'price', 'address', 'localisation','link'])

# ouverture de la page
driver = webdriver.Firefox()
driver.get("https://fr.hotels.com/")
time.sleep(15)

# acceptation des cookies
driver.find_element(by = "xpath" , value = "//button[@class='osano-cm-accept-all osano-cm-buttons__button osano-cm-button osano-cm-button--type_accept']").click()
time.sleep(10)

# configuration de la recherche

driver.find_element(by = "xpath", value = "//div[@class='uitk-field has-floatedLabel-label has-no-placeholder']").click()

time.sleep(10)
search_dest = driver.find_element(by = "id", value="location-field-destination")
dest = search_dest.send_keys(city, Keys.ENTER)
time.sleep(5)


driver.find_element(by = "id", value = "d1-btn").click()
time.sleep(2)

date_text = driver.find_element(by = "xpath", value = "//h2[@class='uitk-date-picker-month-name uitk-type-medium']").text
button_list = driver.find_elements(by="xpath", value="//button[@class='uitk-button uitk-button-medium uitk-button-only-icon uitk-layout-flex-item uitk-button-paging']")


while date_text != month_year:
    button_list[0].click()
    date_text = driver.find_element(by="xpath", value = "//h2[@class='uitk-date-picker-month-name uitk-type-medium']").text

while date_text != date_month:
    button_list[1].click()
    date_text = driver.find_element(by="xpath", value = "//h2[@class='uitk-date-picker-month-name uitk-type-medium']").text


select_date = driver.find_element(by = "xpath", value="//button[@data-day='11']").click()



driver.find_element(by = "xpath", value = "//button[@class='uitk-button uitk-button-medium uitk-button-has-text uitk-button-primary uitk-layout-flex-item uitk-layout-flex-item-flex-shrink-0 dialog-done']").click()



# rechercher
driver.find_element(by = "xpath", value="//button[@class='uitk-button uitk-button-large uitk-button-fullWidth uitk-button-has-text uitk-button-primary']").click()
time.sleep(15)

# Scrap


more1 = driver.find_element(by = "xpath", value = "//button[@data-stid='show-more-results']")
driver.execute_script("arguments[0].click();", more1)
more2 = driver.find_element(by = "xpath", value = "//button[@data-stid='show-more-results']")
driver.execute_script("arguments[0].click();", more2)
more3 = driver.find_element(by = "xpath", value = "//button[@data-stid='show-more-results']")
driver.execute_script("arguments[0].click();", more3)
more4 = driver.find_element(by = "xpath", value = "//button[@data-stid='show-more-results']")
driver.execute_script("arguments[0].click();", more4)
more5 = driver.find_element(by = "xpath", value = "//button[@data-stid='show-more-results']")
driver.execute_script("arguments[0].click();", more5)
for i in range(10):
    driver.find_element(by = "css selector", value = "body").send_keys(Keys.PAGE_DOWN)

    
link_list = driver.find_elements(by = "xpath", value="//a[@class = 'listing__link uitk-card-link']")


prices = list(map(lambda price: price.text, driver.find_elements(by="xpath", value="//div[contains(@class, 'uitk-text uitk-type-600 uitk-type-bold uitk-text-emphasis-theme')]")))
print(prices)
print(len(prices))

grade = list(map(lambda note: note.text, driver.find_elements(by="xpath", value="//span[contains(@class, 'uitk-type-300 uitk-type-bold all-r-padding-one')]")))
print(grade)
print(len(grade))

name = list(map(lambda hotel: hotel.text, driver.find_elements(by="xpath", value="//h3[contains(@class, 'uitk-heading-5 truncate-lines-2 all-b-padding-half pwa-theme--grey-900 uitk-type-heading-500')]")))
print(name)
print(len(name))

links = list(map(lambda hotel_link: hotel_link.get_attribute("href"), driver.find_elements(by="xpath", value="//a[contains(@class, 'listing__link uitk-card-link')]")))
print(links)
print(len(links))

address = []
stars = []
localisation = []

for link in link_list:
    driver.execute_script("arguments[0].click();", link)
    time.sleep(10)

# Changer de fenêtre
    
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(15)

# Scrap name, address, stars

    address_hotel = driver.find_element(by = "xpath",value = "//div[@class='uitk-text uitk-type-300 uitk-layout-flex-item uitk-layout-flex-item-flex-basis-full_width uitk-text-default-theme']").text
    
    locator = Nominatim(user_agent='myGeocoder')
    location = locator.geocode(address_hotel)

    span_list = driver.find_elements(by = "xpath", value = "//span[@class='is-visually-hidden']")
    star_text = span_list[10].get_attribute("innerHTML")
    if len(star_text) > 30:
        stars_hotel = '0'
    else:
        stars_hotel = re.search('([0-9]+)\.([0-9]+)', star_text).group(0)

# ajout aux listes

    address.append(address_hotel)
    stars.append(stars_hotel)
    if location == None :
        localisation.append(("None","None"))
    else :
        localisation.append([location.latitude, location.longitude])

# on ferme l'onglet 
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

for i in range(len(name)):
    df_ligne= pd.DataFrame({'hotel_name': name[i],'note' : grade[i], 'stars': stars[i], 'price': prices[i], 'address' : address[i], 'localisation': localisation[i],'link':links[i]})
    df = pd.concat([df, df_ligne], ignore_index=True)

# création du CSV

df.to_csv("hotelsCom.csv")

"""""
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