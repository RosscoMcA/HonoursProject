# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 14:04:08 2018

@author: Ross
"""
import pandas 
from pandas import read_csv
import json 
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import numpy as np 
import scipy as sp

class test_conditioning:
    
    def load(self):
        accidents= read_csv("A&E Daily Attendances - 2017.csv")
        
        
        with open('bulkweather.json') as datafile: 
            
            data = json.load(datafile)
        
        weather_main = json_normalize(data)
        weather_items = json_normalize(data, "weather")
        
        
        accidents.dropna()
        weather = pandas.concat([weather_main], ignore_index=False)
        weather = weather.join(weather_items,rsuffix="_y" )
        weather["dt"]= pandas.to_datetime(weather["dt"], unit="s")
       
        start_date = '2017-1-1'
        end_date = '2017-11-17'
        mask = (weather['dt'] > start_date)&(weather['dt'] <=end_date)
        weather = weather[mask]
        weather["dt"] = weather["dt"].dt.date
        
        
        #time = (weather['dt_iso'].str.contains("13:00:00"))
        #weather = weather[time]
        
        
            
        
        
        glasgow_and_clyde = accidents["Treatment NHS Board Description - as at date of episode"].isin(["NHS GREATER GLASGOW & CLYDE"])
        
        attendances= accidents[glasgow_and_clyde]
        attendances["Number Of Attendances"]= attendances["Number Of Attendances"].apply(pandas.to_numeric)
        attendances_mean = attendances.groupby("Location Name", as_index=False)["Number Of Attendances"].mean()
        attendances["Arrival Date"] = pandas.to_datetime(attendances["Arrival Date"])
        attendances["Arrival Date"] = attendances["Arrival Date"].dt.date
        attendances["Demmand"] = "NaN"
        demmand = attendances.Demmand.copy()
        
        
        for row in attendances.iterrows(): 
            hospital_loc = attendances_mean[attendances_mean["Location Name"] == row[1][2]]
            hospital_mean = np.int(hospital_loc["Number Of Attendances"])
            if (row[1][3])> hospital_mean:
                demmand[row[0]]= "High"       
            else: 
                demmand[row[0]] = "Low"
        
        attendances["Demmand"] = demmand
       
        
        final_df = pandas.merge(attendances, weather, left_on="Arrival Date", right_on="dt")
        
        print(final_df.columns) 
        
        final_df= final_df.drop(["icon", "id", "city_id", "rain.1h", "rain.3h","rain.24h", "rain.today", 
                               "Treatment NHS Board Description - as at date of episode", 
                               "city_id", "snow.3h", "Number Of Attendances", "Arrival Date", "dt_iso", "weather", "main"], axis=1)
        
        final_df.rename(columns={"Glasgow City": "Road_Accident"}, inplace=True)
        
        return final_df

test = test_conditioning()
data = test.load()