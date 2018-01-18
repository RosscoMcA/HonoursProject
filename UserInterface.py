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
        data =[75	,53,	65,	1005,	281.15,	281.15,	281.15,	290,	4,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]

        
        value = self.prediction(data)
        tk.Label(frame, text= value, font=('bold')).pack()
        
        root.mainloop()
        '''
         tv = ttk.Treeview(frame)
        tv['columns']=('IName','IWeight', 'ICost')
        tv.heading('IName', text='Name')
        tv.column('IName', width=100)
        tv.heading('IWeight', text='Weight')
        tv.column('IWeight', width=100)
        tv.heading('ICost', text= 'Cost')
        tv.column('ICost', width=100)
        tv.grid(row=1, column=2, sticky=(tk.N, tk.S, tk.E, tk.W))

        xs = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tv.xview)
        tv["xscrollcommand"] = xs.set
        xs.grid(row=1, column=2, sticky=(tk.E, tk.W))
        '''
    
       
        
    
    def prediction(self,test_case):
        
        result = ma.prediction(test_case)
         
        return result
        

item = UserInterface()