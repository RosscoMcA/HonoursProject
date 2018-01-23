# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 19:31:09 2018

@author: Ross
"""

import pyowm
import requests 
import pandas
import numpy as np
from pandas import read_csv
from pyowm.utils import timeutils
from pandas.io.json import json_normalize
import json



class weather_data:
    def __init__(self):
        self.r = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?q=Glasgow&APPID=fa9b893f6e8874a535a62844d8192d69&cnt=14")
        self.owm = pyowm.OWM('fa9b893f6e8874a535a62844d8192d69')
    
    def get_data(self, location="Glasgow"):
        
        return self.pre_process_data(location)
        
    def pre_process_data(self, location):
        
        weather = self.pull_weather_data(location)
        
        weather = weather.drop(["temp", "weather", "rain", "icon", 
                                "id","main", "eve", "morn", "night"], axis=1)
        
        weather["humidity"] = weather["humidity"].replace(np.NaN, 0)
        weather = pandas.get_dummies(weather)
          
        weather = weather.rename(columns={"clouds": "clouds.all","humidity": "main.humidity",
                                          "pressure": "main.pressure", "speed": "wind.speed",
                                          "deg": "wind.deg", "day": "main.temp", "max":"main.temp_max",
                                          "min":"main.temp_min"})
        
        return weather
        
        
    def pull_weather_data(self, location):
    #API way of getting weather data

        
        data = json_normalize(self.r.json(), "list")
        weather = pandas.DataFrame()
        for key, value in data.weather.iteritems(): 
           weather = weather.append(json_normalize(value), ignore_index=True)
        
        temp = pandas.DataFrame()
        for key, value in data.temp.iteritems(): 
           temp = temp.append(json_normalize(value), ignore_index=True)    
            
        final = pandas.merge(data, weather, left_index=True, right_index=True)
        final = pandas.merge(final, temp, left_index=True, right_index=True)
        
        return final
       

wd = weather_data()
da = wd.get_data()




