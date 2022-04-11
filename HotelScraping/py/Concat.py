import pandas as pd
import glob
from os import listdir
from os.path import isfile, join


def concat(path, name):
   all_files = glob.glob(path + "/*.csv")
   li = []

   for filename in all_files:
      df = pd.read_csv(filename, sep=";")
      li.append(df)

   frame = pd.concat(li, axis=0, ignore_index=True)
   frame.to_csv(name,index=False,sep=";")


#concat("C:/Users/ACER/PycharmProjects/HotelScraping/HotelScraping/csv/booking","C:/Users/ACER/PycharmProjects/HotelScraping/HotelScraping/csv/csv_par_site/booking_general.csv")
#concat("C:/Users/ACER/PycharmProjects/HotelScraping/HotelScraping/csv/hotelsCom","C:/Users/ACER/PycharmProjects/HotelScraping/HotelScraping/csv/csv_par_site/hotelsCom_general.csv")
#concat("C:/Users/ACER/PycharmProjects/HotelScraping/HotelScraping/csv/trivago","C:/Users/ACER/PycharmProjects/HotelScraping/HotelScraping/csv/csv_par_site/trivago_general.csv")


#concat("C:/Users/ACER/PycharmProjects/HotelScraping/HotelScraping/csv/csv_par_site","C:/Users/ACER/PycharmProjects/InterfaceHotel/test_carte.csv")

#df = pd.read_csv("C:/Users/ACER/PycharmProjects/HotelScraping/HotelScraping/csv/csv_par_site/trivago_general.csv", sep=";")
#df.drop(df.loc[df['name']=='name'].index, inplace=True)
#df.to_csv("C:/Users/ACER/PycharmProjects/HotelScraping/HotelScraping/csv/csv_par_site/trivago_general.csv",index=False, sep=";")


""" 
path = "C:/Users/ACER/PycharmProjects/InterfaceHotel"
df = pd.read_csv(path+"/test_carte.csv", sep=";")
df['stars'].fillna("0",inplace=True)
df.to_csv(path+"/test_carte.csv", index=False,sep=";")
"""
path = "C:/Users/ACER/PycharmProjects/InterfaceHotel"
df = pd.read_csv(path+"/test_carte.csv", sep=";")

new_list=[]
for i in range(len(df['prices'])):
   price_space=df['prices'].iloc[i].replace("\u202f","")
   prix_space = price_space.split(" ")
   prix_space = "".join(prix_space)
   prix=prix_space.replace(',', '.')
   new_list.append(float(prix))
df['prices'] = df['prices'].replace(df['prices'].values, new_list)
df.to_csv(path+"/test_carte.csv",index=False, sep=";")

