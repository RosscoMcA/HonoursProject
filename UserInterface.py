
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 17:43:31 2018

@author: Ross
"""
from ModelAccess import modelAccess as ma
import pandas as pd
import numpy as np

    
    
from DataHandler import data_interface

import datetime as date

try:
    import tkinter as tk
    import tkinter.ttk as tkk
    
except: 
    import Tkinter as tk
    import ttk as tkk
    

class UserInterface: 
    
    def __init__(self):
        self.main_page()
        

    def main_page(self):
        root = tk.Tk()
        root.title("A&E Demand Forecasting")
        frame = tk.Frame(root)
        frame.grid()
        

        var = tk.StringVar()
        
        def refresh_section(hospital):
            var.set("")
            self.results = self.get_result_data(value=hospital)
            
            var.set("Displaying estimated demands for "+hospital)
            tk.Label(frame, textvariable=var).grid(row=0, column=0)
            Tv= tkk.Treeview(frame, columns= ("Date", "Demmand"))
             
            
            Tv.heading("Date", text="Date of Prediction")
            Tv.column("Date", width=150)
            Tv.heading("Demmand", text="Potential Demmand Level")
            Tv.column("Demmand", width=200)
            
            Tv.grid(row=3)
            
            
            i= len(self.results)
            for single in self.results:
                
                Tv.insert("",0, text= i, values=(single[0], single[1]))
                i=i-1
                
            
        refresh_section("ROYAL ALEXANDRA HOSPITAL")   
         
        self.select_case = tk.StringVar()
        self.hospital = tkk.Combobox(frame, textvariable=self.select_case, state="readonly")
 
        self.hospital["values"] = ("ROYAL ALEXANDRA HOSPITAL",
                         "INVERCLYDE ROYAL HOSPITAL", "GLASGOW ROYAL INFIRMARY", 
                         "NEW VICTORIA HOSPITAL", 
                         "QUEEN ELIZABETH UNIVERSITY HOSPITAL", 
                         "ROYAL HOSPITAL FOR CHILDREN", 
                         "STOBHILL HOSPITAL", 
                         "VALE OF LEVEN GENERAL HOSPITAL", 
                         "WEST GLASGOW")
        self.hospital.grid(row=1, column= 0)
        
        
        
        btnPredict = tk.Button(frame, text="Submit", command=lambda: refresh_section(hospital=str(self.select_case.get())))
        btnPredict.grid(row=2, column=0)
        root.mainloop()
        
        
            
            
            
    def get_result_data(self, value=None):
        
        if value == None:
            return None
        
        self.dataframe = self.culminate_data(value)
        
        
        results= []
        for index, item in self.dataframe.iterrows(): 
            dt = str(int(item["month"])) + "/"+ str(int(item["day"]))
            item = item.reshape(1, -1)
            value = self.prediction(item)
            results.append([dt,value])
        return results
    
    def culminate_data(self, department):    
        data_inter = data_interface(department)
        
        data = data_inter.get_data()
        
        
        
      
        
        print(data.dtypes)
        
        return data
    
    def prediction(self, test_case):
        model = ma()
        result = model.prediction(test_case)
         
        return result
        

item = UserInterface()
data = item.culminate_data("VALE OF LEVEN GENERAL HOSPITAL")
res = item.get_result_data()
