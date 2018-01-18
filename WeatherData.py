# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 19:31:09 2018

@author: Ross
"""

import pyowm
import requests 
import pandas

from pyowm.utils import timeutils
from pandas.io.json import json_normalize
import json



class weather_data:
    def __init__(self):
        self.r = requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?q=Glasgow&APPID=fa9b893f6e8874a535a62844d8192d69&cnt=14")
        self.owm = pyowm.OWM('fa9b893f6e8874a535a62844d8192d69')
        
        
    def getWeatherData(self, location):
    #API way of getting weather data

        
        data = json_normalize(self.r.json(), "list")
        weather = pandas.DataFrame(columns=["description", "icon","id", "main"])
        for key, value in data.weather.iteritems():
            weather.append(json_normalize(value))
            
      
        


        for key, value in data.temp.iteritems():
            temp.append(json_normalize(value))
        
        weather = pandas.DataFrame.from_records(weather) 
        final = pandas.concat([data, weather, temp], axis=1, join="inner")
       
        return data, weather, temp, final
        

weather = weather_data()
data = weather.getWeatherData("Glasgow")




