# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 19:19:58 2018

@author: Ross
"""
import pandas 
from pandas import read_csv
import numpy as np 
class department:
    
    def get_department_dummies(self, option, repition):
        values = {"Treatment Location Name": [option]}
        
        data = pandas.DataFrame(values)
        
        dummy = read_csv("dummy_model")
        
        data = pandas.get_dummies(data)
        
        data = data.reindex(columns=dummy.columns, fill_value=0)
        
        data =data.append([data]*(repition-1), ignore_index=True)
        data = data.loc[:,["Treatment Location Name_GLASGOW ROYAL INFIRMARY", 
                    "Treatment Location Name_INVERCLYDE ROYAL HOSPITAL", 
                    "Treatment Location Name_NEW VICTORIA HOSPITAL", 
                    "Treatment Location Name_QUEEN ELIZABETH UNIVERSITY HOSPITAL", 
                    "Treatment Location Name_ROYAL ALEXANDRIA HOSPITAL", 
                    "Treatment Location Name_ROYAL HOSPITAL FOR CHILDREN", 
                    "Treatment Location Name_STOBHILL HOSPITAL", 
                    "Treatment Location Name_VALE OF LEVEN GENERAL HOSPITAL", 
                    "Treatment Location Name_WEST GLASGOW"]]
        
        data=  data.replace(np.NaN, 0)
        return data
        
    
      
        