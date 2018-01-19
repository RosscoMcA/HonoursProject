# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 17:43:31 2018

@author: Ross
"""
from ModelAccess import modelAccess as ma
import pandas as pd
import tkinter as tk


class UserInterface: 
    
    def __init__(self):
        self.main_page()

    def main_page(self):
        root = tk.Tk()
        frame = tk.Frame(root)
        frame.pack()
        

        
        value = self.prediction(data)
        tk.Label(frame, text= value, font=('bold')).pack()
        
        root.mainloop()
       
    
       
        
    
    def prediction(self,test_case):
        
        result = ma.prediction(test_case)
         
        return result
        

item = UserInterface()