# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 13:30:54 2018

@author: Ross
"""

from sklearn.externals import joblib
from sklearn import svm

class modelAccess : 
    
    def __init__(self): 
        self.clf = joblib.load("A&EModel")
    
    def get_model(self):
        return self.clf
    
    def prediction(self, inputData):
        
        result = self.clf.predict(inputData)
        
        if(result == 1):
            return "High Demmand"
        
        elif(result==0):
            return "Low Demmand"
        
        else: return "Error: 404"
        
        