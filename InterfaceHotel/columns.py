import numpy as np
import pandas as pd

def columns():
    df = pd.read_csv("test_carte.csv", sep=";")

    lenght = len(df.columns)

    stars_choice = df['stars'].unique()
    stars_choice = np.insert(stars_choice,0,10)
    date_choice = df['start_date'].unique()
    date_choice = np.insert(date_choice,0,'all')
    adulte_choice = df['nb_adulte'].unique()
    adulte_choice = np.insert(adulte_choice,0,10)
    enfant_choice = df['nb_enfant'].unique()
    enfant_choice = np.insert(enfant_choice,0,10)
    room_choice = df['nb_chambre'].unique()
    room_choice = np.insert(room_choice,0,10)
    return stars_choice,date_choice,adulte_choice,enfant_choice,room_choice, lenght