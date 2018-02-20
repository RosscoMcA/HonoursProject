# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 19:17:20 2018

@author: Ross
"""

from DepartmentHandler import department 
from WeatherData import weather_data as wd
import pandas as pd
import sklearn.feature_selection as feature_sel
from ModelAccess import modelAccess as ma
from pandas import read_csv

class data_interface: 
    
    def __init__(self, dept): 
        
        self.department = department()
        
        dummy_department = self.department.get_department_dummies(dept,14)
        weather_source= wd()
        weather = weather_source.get_data()
        
        dataset = pd.merge( weather,dummy_department, right_index=True, left_index=True)
        
        dataset["dt"]= pd.to_datetime(dataset["dt"], unit="s").dt.date
        dataset["dt"] = pd.to_datetime(dataset["dt"])
        dataset["day"]= dataset["dt"].apply(lambda x: int(x.day))
        dataset["month"] = dataset["dt"].apply(lambda x: int(x.month))
        
        dummy = read_csv("dummy_model")
        dataset = dataset.reindex(columns=dummy.columns, fill_value=0)
        
        
       
        dataset = dataset.dropna()
        dataset["clouds.all"] = [float(x) for x in dataset["clouds.all"]]
        dataset = dataset.drop(["Unnamed: 0"], axis=1)
        
          
        self.final_dataset= dataset
    
    
    
      
        
    def get_data(self):
        
        return self.final_dataset
        

d = data_interface("INVERCLYDE ROYAL HOSPITAL")
da = d.get_data()
        