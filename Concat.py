import pandas as pd
from os import listdir
from os.path import isfile, join

liste = [f for f in listdir("csv") if isfile(join("csv", f))]

dataFrame = pd.concat(
   map(pd.read_csv, liste), ignore_index=True)

dataFrame.to_csv("hotel_scrap.csv",sep=";")