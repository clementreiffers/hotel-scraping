import pandas as pd
from os import listdir
from os.path import isfile, join

def concat(dossier, name):
   liste = [f for f in listdir(dossier) if isfile(join(dossier, f))]

   dataFrame = pd.concat(
      map(pd.read_csv, liste), ignore_index=True)

   dataFrame.to_csv(name,sep=";")
