import pandas as pd
import numpy as np
import datetime
import plotly.express as px


def figure_med():
    df_total = pd.read_csv("statMed.csv", sep=";")
    fig = px.line(df_total, x="date", y="median", markers=True, color_discrete_sequence = [ "#82DAD0"])
    return fig


def mediane_mois(df):
    mediane=[]
    indexNames = df[df['prices'] <= 20].index
    df.drop(indexNames, inplace=True)
    list_mois = df['start_date'].unique()
    for i in range(len(list_mois)):
        list_mois[i] = datetime.datetime.strptime(list_mois[i], "%m-%d-%Y")
    list_mois = sorted(list_mois)
    for i in range(len(list_mois)):
        list_mois[i] = datetime.datetime.strftime(list_mois[i], "%m-%d-%Y")
    for i in list_mois:
        mois=[]
        df = df[['start_date','prices']]
        df_mois = df[(df['start_date']== i)]
        mois.append(i)
        price = df_mois["prices"].median()
        mois.append(price)
        mediane.append(mois)
    df_med = pd.DataFrame(data=mediane, columns=['date', 'median'])
    df_med.to_csv("statMed.csv",index=False,sep=";")


df = pd.read_csv("test_carte.csv", sep=";")
#mediane_mois(df)