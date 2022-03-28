import webbrowser

import pandas as pd
import numpy as np
import folium

""" 
df1 = pd.read_csv("bookingCom.csv")
df2 = pd.read_csv("trivagoScraping.csv")
df3 = pd.read_csv("hotelsCom1.csv")

df4 = pd.concat([df1,df2])
df = pd.concat([df4,df3])

df.to_csv("hotel_scrap.csv")
"""

df = pd.read_csv("hotelsCom1.csv")
carte = folium.Map([48.850928, 2.346260], zoom_start=20)

x = df['localisation']
y = df['hotel_name']
z = df['address']
p = df['price']

for i in range(len(df)):
    if x[i] is np.nan:
        None
    else:
        html = y[i] + "<br>" + z[i] + "<br>"  + p[i]
        iframe = folium.IFrame(html, width=200, height=100)
        popup = folium.Popup(iframe, max_width=200)
        loc = x[i].split(",")
        characters = "[]"
        latitude = ''.join( x for x in loc[0] if x not in characters)
        longitude = ''.join(x for x in loc[1] if x not in characters)
        folium.Marker([latitude, longitude], popup = popup).add_to(carte)

carte.save('Carte_hotel.html')
webbrowser.open("Carte_hotel.html")
