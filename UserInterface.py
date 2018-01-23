# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 17:43:31 2018

@author: Ross
"""
from ModelAccess import modelAccess as ma
import pandas as pd
import numpy as np
import tkinter as tk
from DataHandler import data_interface


class UserInterface: 
    
    def __init__(self):
        self.main_page()
        

    def main_page(self):
        root = tk.Tk()
        frame = tk.Frame(root)
        frame.pack()
        

        self.dataframe = self.culminate_data("INVERCLYDE ROYAL HOSPITAL")
        
        self.dataframe = self.dataframe.values
        results= []
        for item in self.dataframe: 
            
            value = self.prediction(item)
            results.append(value)
            tk.Label(frame, text= value, font=('bold')).pack()
        self.results = results
        #root.mainloop()
       
    def get_result_data(self):
        return self.results
       
    def culminate_data(self, department):   
        data_inter = data_interface(department)
        
        data = data_inter.get_data()
        
        data["clouds.all"] = [float(x) for x in data["clouds.all"]]
        
      
        
        print(data.dtypes)
        
        return data
    
    def prediction(self, test_case):
        model = ma()
        result = model.prediction(test_case)
         
        return result
        

item = UserInterface()
data = item.culminate_data("QUEEN ELIZABETH UNIVERSITY HOSPITAL")
res = item.get_result_data()
