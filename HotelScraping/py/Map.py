import webbrowser

import pandas as pd
import numpy as np
import folium

# export du csv général
df = pd.read_csv("C:/Users/ACER/PycharmProjects/InterfaceHotel/test_carte.csv", sep = ";")


# création de la carte
carte = folium.Map([48.850928, 2.346260], zoom_start=20)

# suppression des lignes jumelles pout le même hotel
df_carte = df[['gps','name','address','prices']]
df_carte = df_carte.sort_values(by=["name"], key=lambda col: col.str.upper())
info_carte = df_carte.drop_duplicates(subset=['name'], ignore_index = True)
coordo_carte = info_carte.dropna(how = 'any')


# récupération des données
x = coordo_carte['gps'].values
y = coordo_carte['name'].values
z = coordo_carte['address'].values
p = coordo_carte['prices'].values


# ajout des points sur la carte
for i in range(len(coordo_carte)):
    html = str(y[i]) + "<br>" + str(z[i]) + "<br>"  + str(p[i]+"€")
    iframe = folium.IFrame(html, width=200, height=100)
    popup = folium.Popup(iframe, max_width=200)
    loc = x[i].split(",")
    characters = "[]"
    latitude = ''.join( x for x in loc[0] if x not in characters)
    longitude = ''.join(x for x in loc[1] if x not in characters)
    folium.Marker([latitude, longitude], popup = popup).add_to(carte)

carte.save('C:/Users/ACER/PycharmProjects/InterfaceHotel/Carte_hotel.html')
webbrowser.open("C:/Users/ACER/PycharmProjects/InterfaceHotel/Carte_hotel.html")
