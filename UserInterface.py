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
import tkinter.ttk as tkk
import datetime as date



class UserInterface: 
    
    def __init__(self):
        self.main_page()
        

    def main_page(self):
        root = tk.Tk()
        frame = tk.Frame(root)
        frame.grid()
        

        
        
        def refresh_section(hospital):
            
            self.results = self.get_result_data(value=hospital)
            var = tk.StringVar()
            var.set("Displaying estimated demands for "+hospital)
            tk.Label(frame, textvariable=var).grid(row=0)
            Tv= tkk.Treeview(frame)
            Tv["columns"]= ("Date", "Demmand")
            Tv.heading("Date", text="Date of Prediction")
            Tv.column("Date", width=150)
            Tv.heading("Demmand", text="Potential Demmand Level")
            Tv.column("Demmand", width=200)
            
            Tv.grid(row=2, sticky=(tk.N, tk.S, tk.E, tk.W))
            
            for single in self.results:
                Tv.insert("", "end", text="", values=(single[0], single[1]))
                
            
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
        btnPredict.grid(row=1, column=1)
        root.mainloop()
        
        
            
            
            
    def get_result_data(self, value=None):
        
        if value == None:
            return None
        
        self.dataframe = self.culminate_data(value)
        
        self.dataframe = self.dataframe.values
        results= []
        for item in self.dataframe: 
            dt = date.date.fromordinal(int(item[1]))
            value = self.prediction(item)
            results.append([dt,value])
        return results
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
data = item.culminate_data("VALE OF LEVEN GENERAL HOSPITAL")
res = item.get_result_data()
