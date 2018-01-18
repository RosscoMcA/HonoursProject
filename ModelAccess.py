# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 13:30:54 2018

@author: Ross
"""

from sklearn.externals import joblib
from sklearn import svm

class modelAccess : 
    
    
    
   
    
    def prediction(inputData):
        
        clf = joblib.load("A&EModel")
        
        result = clf.predict(inputData)
        
        if(result == 1):
            return "High Demmand"
        
        elif(result==0):
            return "Low Demmand"
        
        else: return "Error: 404"
        
        