# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 21:43:01 2017

@author: Ross
"""
import pandas 
from pandas import read_csv
import json 
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import numpy as np 
import scipy as sp
 
atd = read_csv("A&E Daily Attendances.csv")


atd = atd.drop(atd.index[[0,1,2,3]])
atd.columns = atd.iloc[0]
atd = atd.drop(atd.index[[0]])
with open('bulkweather.json') as datafile: 
    
    data = json.load(datafile)

weather_main = json_normalize(data)
weather_items = json_normalize(data, "weather")


atd.dropna()
weather = pandas.concat([weather_main], ignore_index=False)
weather = weather.join(weather_items,rsuffix="_y" )
weather["dt"]= pandas.to_datetime(weather["dt"], unit="s")

start_date = '2014-12-31'
end_date = '2016-12-31'
mask = (weather['dt'] > start_date)&(weather['dt'] <=end_date)
weather = weather[mask]
weather["dt"] = weather["dt"].dt.date


time = (weather['dt_iso'].str.contains("13:00:00"))
weather = weather[time]


    


glasgow_and_clyde = atd["Treatment NHS Board Description - as at date of episode"].isin(["NHS GREATER GLASGOW & CLYDE"])

attendances= atd[glasgow_and_clyde]

attendances_mean = np.mean(pandas.to_numeric(attendances["Number Of Attendances"]))
attendances["Arrival Date"] = pandas.to_datetime(attendances["Arrival Date"])
attendances["Arrival Date"] = attendances["Arrival Date"].dt.date
attendances["Demmand"] = "Low"

for row in attendances.iterrows(): 
    
    if int(row[1][3])> attendances_mean:
        row[1][4] = "High"
        
    else: 
        row[1][4] = "Low"
print(attendances.describe()) 

final_df = pandas.merge(attendances, weather, left_on="Arrival Date", right_on="dt")
