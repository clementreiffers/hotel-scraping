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


#concat("csv/booking","csv/csv_par_site/booking_general.csv")
#concat("csv/hotelsCom","csv/csv_par_site/hotelsCom_general.csv")
#concat("csv/trivago","csv/csv_par_site/trivago_general.csv"

#df = pd.read_csv("C:/Users/ACER/PycharmProjects/HotelScraping/HotelScraping/csv/csv_par_site/trivago_general.csv", sep=";")
#df.drop(df.loc[df['name']=='name'].index, inplace=True)
#df.to_csv("C:/Users/ACER/PycharmProjects/HotelScraping/HotelScraping/csv/csv_par_site/trivago_general.csv",index=False, sep=";")