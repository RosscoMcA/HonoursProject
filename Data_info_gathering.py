# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 12:57:03 2018

@author: Ross
"""
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import pandas 
import numpy as np
from pandas import read_csv
import json 

road_accidents= read_csv("accidents_day_council15_16.csv")
atd = read_csv("A&E Daily Attendances.csv")
with open('bulkweather.json') as datafile: 
        
        data = json.load(datafile)
        
weather = json_normalize(data)
weather["dt"]= pandas.to_datetime(weather["dt"], unit="s")
start_date = '2014-12-31'
end_date = '2016-12-31'
mask = (weather['dt'] > start_date)&(weather['dt'] <=end_date)
weather = weather[mask]
weather_items = json_normalize(data, "weather")
weather = pandas.concat([weather], ignore_index=False)
weather = weather.join(weather_items,rsuffix="_y" )
atd= atd.dropna()
print(atd.count())


