import pandas as pd
import numpy as np
import datetime
import plotly.express as px


def figure():
    df_total = pd.read_csv("stat.csv", sep=";")
    fig = px.line(df_total, x="date", y="mean", markers=True, color_discrete_sequence = [ "#82DAD0"])
    return fig


def moyenne_mois(df):
    moyenne=[]
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
        price = df_mois["prices"].mean()
        mois.append(price)
        moyenne.append(mois)
    df_moyenne = pd.DataFrame(data=moyenne, columns=['date', 'mean'])
    df_moyenne.to_csv("stat.csv",index=False,sep=";")


df= pd.read_csv("test_carte.csv", sep=";")
#moyenne_mois(df)

#df.loc[df['start_date']=='11-04-2022','start_date'] = "04-11-2022"
#df.loc[df['start_date']=='11-05-2022','start_date'] = "05-11-2022"
#df.to_csv(path+"/test_carte.csv", index = False,sep=";")

