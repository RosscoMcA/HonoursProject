# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 19:19:58 2018

@author: Ross
"""
import pandas 
from pandas import read_csv
class department:
    
    def get_department_dummies(option, repition):
        values = {"Treatment Location Name": [option]}
        
        data = pandas.DataFrame(values)
        
        dummy = read_csv("dummy_model")
        
        data = pandas.get_dummies(data)
        
        data = data.reindex(columns=dummy.columns, fill_value=0)
        
        data =data.append([data]*(repition-1), ignore_index=True)
        return data
        
    
data = department.get_department_dummies("INVERCLYDE ROYAL HOSPITAL", 14)        
        