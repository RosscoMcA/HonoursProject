# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 19:17:20 2018

@author: Ross
"""

from DepartmentHandler import department as dept
from WeatherData import weather_data as wd
import pandas as pd
import sklearn.feature_selection as feature_sel
from ModelAccess import modelAccess as ma
from pandas import read_csv

class data_interface: 
    
    def __init__(self, department): 
        
        dummy_department = dept.get_department_dummies(department,14)
        weather_source= wd()
        weather = weather_source.get_data()
        
        dataset = pd.merge( weather,dummy_department, right_index=True, left_index=True)
        
        
        dummy = read_csv("dummy_model")
        dataset = dataset.reindex(columns=dummy.columns, fill_value=0)
        
        dataset["dt"]= pd.to_datetime(dataset["dt"], unit="s").dt.date
        dataset["dt"] = pd.to_datetime(dataset["dt"])
        dataset["dt"]= dataset["dt"].apply(lambda x: x.toordinal())
       
        dataset = dataset.dropna()
        dataset = dataset.drop(["Unnamed: 0", "Road_Accident", 
                                "description_drizzle","description_snow", 
                                "description_thunderstorm", "description_rain and drizzle"
                                , "description_overcast clouds",
                                "description_light intensity drizzle", 
                                "description_light intensity shower rain"], axis=1)
        
          
        self.final_dataset= dataset
    
    
    
      
        
    def get_data(self):
        
        return self.final_dataset
        

d = data_interface("INVERCLYDE ROYAL HOSPITAL")
da = d.get_data()
        