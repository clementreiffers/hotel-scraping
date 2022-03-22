# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 21:57:06 2022

@author: ACER
"""


### scrap hotel.com    https://fr.hotels.com/
## demander aux garçons de se mettre d'accord tous sur une date pour le prix 


##df_hotel : nom , adresse, nombre étoile , prix 1 nuit 2 personnes, prix 1 nuit 4 personnes 


import time 
import re
import folium
import webbrowser
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from geopy.geocoders import Nominatim 

# création du data frame

df = pd.DataFrame(columns=['hotel_name','stars','price','address','latitude','longitude'])

# ouverture de la page
driver = webdriver.Firefox()
driver.get("https://fr.hotels.com/")
time.sleep(10)

# acceptation des cookies
driver.find_element_by_xpath("//button[@class='osano-cm-accept-all osano-cm-buttons__button osano-cm-button osano-cm-button--type_accept']").click()
time.sleep(10)

# configuration de la recherche

driver.find_element_by_xpath("//div[@class='uitk-field has-floatedLabel-label has-no-placeholder']").click()

time.sleep(10)
search_dest = driver.find_element_by_id("location-field-destination")
search_dest.send_keys("Paris", Keys.ENTER)
time.sleep(5)

"""
driver.find_element_by_id("d1-btn").click()
time.sleep(2)

driver.find_element_by_class_name("uitk-button uitk-button-medium uitk-button-only-icon uitk-layout-flex-item uitk-button-paging").click().click()
time.sleep(2)


select_date = driver.find_elements_by_xpath("//button[@class='uitk-date-picker-day']")


for i in range (len(select_date)):
    if select_date[i].['aria-label'] == "8 juill. 2022":
        select_date[i].click()


driver.find_element_by_class_name("uitk-button uitk-button-medium uitk-button-has-text uitk-button-primary uitk-layout-flex-item uitk-layout-flex-item-flex-shrink-0 dialog-done").click()

"""

# rechercher
driver.find_element_by_xpath("//button[@class='uitk-button uitk-button-large uitk-button-fullWidth uitk-button-has-text uitk-button-primary']").click()
time.sleep(15)

# Scrap

# more1 = driver.find_element_by_xpath("//button[@data-stid='show-more-results']")
# driver.execute_script("arguments[0].click();", more1)
# more2 = driver.find_element_by_xpath("//button[@data-stid='show-more-results']")
# driver.execute_script("arguments[0].click();", more2)    
# more3 = driver.find_element_by_xpath("//button[@data-stid='show-more-results']")
# driver.execute_script("arguments[0].click();", more3)  
# more4 = driver.find_element_by_xpath("//button[@data-stid='show-more-results']")
# driver.execute_script("arguments[0].click();", more4)
# more5 = driver.find_element_by_xpath("//button[@data-stid='show-more-results']")
# driver.execute_script("arguments[0].click();", more5)
    
link_list = driver.find_elements_by_xpath("//a[@class = 'listing__link uitk-card-link']")


price = list(map(lambda price: price.text, driver.find_elements(by="xpath", value="//div[contains(@class, 'uitk-text uitk-type-600 uitk-type-bold uitk-text-emphasis-theme')]")))
print(price)   

for link, i  in link_list[0:1], range(len(link_list)): 
    driver.execute_script("arguments[0].click();", link)
    time.sleep(10)

# Changer de fenêtre
    
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(15)
    


# Scrap name, address, stars
    
    name = driver.find_element_by_class_name("uitk-heading-3").text 
    
    address = driver.find_element_by_xpath("//div[@class='uitk-text uitk-type-300 uitk-layout-flex-item uitk-layout-flex-item-flex-basis-full_width uitk-text-default-theme']").text
    
    locator = Nominatim(user_agent='myGeocoder')
    location = locator.geocode(address)
    
    
    span_list = driver.find_elements_by_xpath("//span[@class='is-visually-hidden']")
    star_text = span_list[10].get_attribute("innerHTML")
    if len(star_text) > 30:
        stars = '0'
    else:
        stars = re.search('([0-9]+)\.([0-9]+)', star_text).group(0)
    
    
# ajout au data frame
    if location == None:
        print(name)
    else:
        df = df.append({'hotel_name': name, 'stars': stars, 'address': address, 'latitude': location.latitude,'longitude': location.longitude }, ignore_index=True)
    
# on ferme l'onglet 
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0]) 
    
    
    


# création du CSV

df.to_csv("hotelsCom.csv")

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
