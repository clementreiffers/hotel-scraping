import pandas as pd
import numpy as np
import datetime
import plotly.express as px


def figure_et():
    df_total = pd.read_csv("statEtendu.csv", sep=";")
    fig = px.line(df_total, x="date", y=["etendu",'max','min'], markers=True, color_discrete_sequence = [ "#82DAD0","#FFC300",'#DAF7A6'])
    return fig


def etendu_mois(df):
    et=[]
    indexNames = df[df['prices'] <= 20].index
    df.drop(indexNames, inplace=True)
    list_mois = df['start_date'].unique()
    print(list_mois)
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
        max = df_mois["prices"].max()
        min = df_mois["prices"].min()
        etendue = max-min
        mois.append(etendue)
        mois.append(max)
        mois.append(min)
        et.append(mois)
    df_moyenne = pd.DataFrame(data=et, columns=['date', 'etendu','max','min'])
    df_moyenne.to_csv("statEtendu.csv",index=False,sep=";")


df= pd.read_csv("test_carte.csv", sep=";")
#etendu_mois(df)