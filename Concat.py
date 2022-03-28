import pandas as pd

df1 = pd.read_csv("bookingCom.csv", sep = ";")
df2 = pd.read_csv("trivagoScraping.csv", sep = ";")
df3 = pd.read_csv("hotelsCom.csv", sep = ";")

df4 = pd.concat([df1,df2])
df = pd.concat([df4,df3])

df.to_csv("hotel_scrap.csv", index = False, sep = ";")