# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:15:33 2022

@author: Meat is delicious
"""

from selenium import webdriver
import time

def accept_conditions():
    time.sleep(6)
    try:
        driver.find_element(by="xpath", value="//button[contains(@aria-label, 'Accepter')]").click()
    except:
        driver.find_element(by="xpath",value="//button[contains(@class, 'Iqt3 Iqt3-mod-stretch Iqt3-mod-bold Button-No-Standard-Style Iqt3-mod-variant-solid Iqt3-mod-theme-action Iqt3-mod-shape-rounded-small Iqt3-mod-shape-mod-default Iqt3-mod-spacing-default Iqt3-mod-size-small')]").click()       

def set_parameters(location, date_debut,date_fin, adultes, enfants, chambre):
    #pour mettre la date en format kayak
    reverse_date_debut = date_debut.split("-")
    date_debut1 = '-'.join(reverse_date_debut[::-1])
    
    reverse_date_fin = date_fin.split("-")
    date_fin1 = '-'.join(reverse_date_fin[::-1])
    
    parameter = "https://www.kayak.fr/hotels/"+location+"-c36014/"+str(date_debut1)+"/"+str(date_fin1)+"/"+str(adultes)+"adults/"+str(enfants)+"children"+int(enfants)*"-0"+"/"+str(chambre)+"rooms"
    return parameter

def get_more_hotel():
    for i in range(0,3,1):
        #boucle a ralentir si wifi de merde
        more = driver.find_element_by_class_name('moreButton')
        more.click()
        time.sleep(10)
    return

def get_nom():
    textsList= driver.find_elements(by="xpath", value="//div[contains(@class, 'FLpo-hotel-name')]")
    list_nom=[]                                           #on a besoin de créer une liste vide
    import unidecode
    for textHotel in textsList:                           #parcour les elements de la liste
        unaccented_string = unidecode.unidecode(textHotel.text)      # retire les accents du data collecté
        list_nom.append(unaccented_string)
    return list_nom

def get_grade():                                         # 
    import numpy as np 
    list_grade=[]
    liste1 = driver.find_elements(by="xpath", value="//div[contains(@class, 'FLpo-reviews')]")
    for element in liste1:
        if "Aucun" in element.text:
            list_grade.append(np.nan)
        else:
            grade = element.find_element_by_class_name("FLpo-score")
            list_grade.append(grade.text)
    return list_grade

def get_stars():                                        #compter le nombre de classes --> 
                                                        #Pointer la bonne classe, dans une sous classe                                                 
    nbr_stars_list = driver.find_elements(by="xpath", value="//div[contains(@class, 'FLpo-info-top')]")  
    stars_list=[]
    for i in nbr_stars_list:
        try :
            star = i.find_element(by="xpath", value="//div[contains(@class, 'O3Yc-star')]")
            if star is None:
                stars_list.append(0)
        except:
            stars_list.append(len(i.find_elements_by_class_name('O3Yc-star')))
    return stars_list

def get_price():                                       #triez les caractères car n'ai pas réussi à avoir juste le prix
                                                       #eliminer les valeurs en double de la liste                                              

    list_price = driver.find_elements(by="xpath", value="//div[contains(@class, 'zV27-price')]")
    list_price2=[]
    for price in list_price:
        import re
        numeric_price = re.sub("[^0-9]","",price.text)    #Trie les caractères speciaux et tt le bazard pour retourner que le prix
        list_price2.append(numeric_price+"€")          
        list_price2=list(dict.fromkeys(list_price2))      #enleve les valeurs en double dans la liste list_price2
    return list_price2
   
def get_adresse():                                    # Obliger d'ouvrir une nouvelle fenetre   
                                                      # recuperer adresse, en mettant retournant np.nan si null
                                                      # --> pb des annonces, que l'on arrivait pas cliquer dessus, tout en cliquant sur le reste des hotels
                                                      
    import numpy as np
    liste_adresse=[]
    driver_list = driver.find_elements_by_class_name('zV27')
    for hotel in driver_list:
        hotel.click()
        time.sleep(8)
        driver.switch_to.window(driver.window_handles[1])
        adresse = driver.find_element(by="xpath", value="//span[contains(@class, 'c9fNw-address')]") 
        
        if "Adresse" in  adresse.text:
                liste_adresse.append(np.nan)               #ajoute un retour d'erreur a la liste quand il trouve qu'il n'y a pas d'adresse dans la case
        else:
                liste_adresse.append(adresse.text)
                
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return liste_adresse

def getLocalisationFromAdd(add):
    import numpy as np
    from geopy.geocoders import Nominatim
    try:
        location = Nominatim(user_agent="main").geocode(add)
        return [location.latitude, location.longitude] if location is not None else np.nan
    except:
        return np.nan
    
def get_hotels_gps_from_get_loc(adresse_list):
        liste_adresse=adresse_list
        liste_gps = list(map(lambda location: getLocalisationFromAdd(location), liste_adresse))
        return  liste_gps

def get_link():
    liste_link=[]
    driver_list = driver.find_elements_by_class_name('zV27')
    for hotel in driver_list:  
        hotel.click()
        time.sleep(8)
        driver.switch_to.window(driver.window_handles[1])  
        
        link = driver.current_url
        liste_link.append(link)
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return liste_link  



if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.maximize_window()
    
    start_date = "15-05-2022"
    end_date = "20-05-2022"
    adults = "3"
    enfants= "0"
    chambres = "2"  
    
    driver.get(set_parameters("Paris,France", start_date,end_date,adults,enfants,chambres))
    accept_conditions()
    time.sleep(20)
    
    nom = get_nom()
    note = get_grade()
    etoiles = get_stars()
    prix = get_price()
    adresse = get_adresse()
    gps= get_hotels_gps_from_get_loc(get_adresse())
    lien =  get_link()
    
    print(len(nom))
    print(len(note))
    print(len(etoiles))
    print(len(prix))
    print(len(adresse))
    print(len(gps))
    print(len(lien))
    
    print(nom)
    print("##########################")
    print(note)
    print("##########################")
    print(etoiles)
    print("##########################")
    print(prix)
    print("##########################")
    print(adresse)
    print("##########################")
    print(gps)
    print("##########################")
    print(lien)

    import pandas as pd
    date_depart = [start_date for i in range(len(get_nom()))]
    date_arrive = [end_date for i in range(len(get_nom()))]
    adults = [ adults for i in range(len(get_nom()))]
    children = [ enfants for i in range(len(get_nom()))]
    rooms = [chambres for i in range(len(get_nom()))]
    
    #name;grade;stars#;prices;address#;gps#;start_date;end_date;nb_adulte;nb_enfant;nb_chambre;link#
    dict = {"name" : nom,"grade": note, "stars": etoiles,"price": prix, "adresse": adresse,"gps": gps , "start_date": date_depart,"end_date" : date_arrive,"nb_adulte":adults,"nb_enfant": children, "nb_chambre": rooms, "link": lien }
    df = pd.DataFrame(dict)
    df.to_csv('hotel_kayak_test.csv',index = False) 



    


    
    
    
    
    
    
    
    
    
    
    
    
    
    