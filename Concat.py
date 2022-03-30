import pandas as pd
import glob
from os import listdir
from os.path import isfile, join


def concat(path, name):
   all_files = glob.glob(path + "/*.csv")
   li = []

   for filename in all_files:
      df = pd.read_csv(filename)
      li.append(df)

   frame = pd.concat(li, axis=0, ignore_index=True)
   frame.to_csv(name,sep=";")

#concat("csv/booking","test.csv")

