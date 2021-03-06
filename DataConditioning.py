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


road_accidents= read_csv("accidents_day_council15_16.csv")
glasgow_road = road_accidents[["Unnamed: 0","Glasgow City"]]
def _init_(): 
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
    glasgow_road["Unnamed: 0"] = pandas.to_datetime(glasgow_road["Unnamed: 0"])
    glasgow_road["Unnamed: 0"] = glasgow_road["Unnamed: 0"].dt.date
    start_date = '2014-12-31'
    end_date = '2016-12-31'
    mask = (weather['dt'] > start_date)&(weather['dt'] <=end_date)
    weather = weather[mask]
    weather["dt"] = weather["dt"].dt.date
    
    
    time = (weather['dt_iso'].str.contains("13:00:00"))
    weather = weather[time]
    
    
        
    
    
    glasgow_and_clyde = atd["Treatment NHS Board Description - as at date of episode"].isin(["NHS GREATER GLASGOW & CLYDE"])
    
    attendances= atd[glasgow_and_clyde]
    attendances["Number Of Attendances"]= attendances["Number Of Attendances"].apply(pandas.to_numeric)
    attendances_mean = attendances.groupby("Treatment Location Name", as_index=False)["Number Of Attendances"].mean()
    attendances["Arrival Date"] = pandas.to_datetime(attendances["Arrival Date"])
    attendances["Arrival Date"] = attendances["Arrival Date"].dt.date
    attendances["Demmand"] = "NaN"
    demmand = attendances.Demmand.copy()
    
    
    for row in attendances.iterrows(): 
        hospital_loc = attendances_mean[attendances_mean["Treatment Location Name"] == row[1][2]]
        hospital_mean = np.int(hospital_loc["Number Of Attendances"])
        if (row[1][3])> hospital_mean:
            demmand[row[0]]= "High"       
        else: 
            demmand[row[0]] = "Low"
    
    attendances["Demmand"] = demmand
   
    
    final_df = pandas.merge(attendances, weather, left_on="Arrival Date", right_on="dt")
    final_df = pandas.merge(final_df, glasgow_road, left_on="dt", right_on="Unnamed: 0")
    print(final_df.columns) 
    
    final_df= final_df.drop(["icon", "id", "city_id", "rain.1h", "rain.3h","rain.24h", "rain.today", 
                           "Treatment NHS Board Description - as at date of episode", 
                           "city_id", "snow.3h", "Number Of Attendances", "Arrival Date", "dt_iso", "weather", "Unnamed: 0", "main"], axis=1)
    
    final_df.rename(columns={"Glasgow City": "Road_Accident"}, inplace=True)
    return final_df

value = _init_()