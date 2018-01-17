# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 13:26:48 2018

@author: Ross
"""

from pandas import read_csv
import pandas
import matplotlib.pyplot as plt
import numpy as np
import DataConditioning as dc
from matplotlib import interactive
from sklearn.cross_validation import train_test_split
from sklearn.decomposition import PCA
import sklearn.feature_selection
from datetime import datetime

interactive(True)


def set_dummies(dataset):
    
    dataset = pandas.get_dummies(dataset)
    
    return dataset
    




def outlier_ident(x):
    q1 = np.percentile(x, 25)
    q3 = np.percentile(x, 75)
    inter_quart_r = q3-q1
    flr = q1-1.5*inter_quart_r
    cel = q3 + 1.5*inter_quart_r
    outlier_indices = list(x.index[(x<flr) | (x>cel)])
    return outlier_indices
    
def processOutliers(data, dataset):
    indices= outlier_ident(data)
        
    for item in indices:
       dataset.drop(item)

       
        
 

    return dataset






def feature_selec(X_Train, Y_Train, X_Test, x):
    select = sklearn.feature_selection.SelectPercentile(percentile=80)
    select_feature = select.fit(X_Train, Y_Train)
    indic_sel = select_feature.get_support(indices=True)
    colnames_select = [x.columns[i] for i in indic_sel]
    
    x_train_sel = X_Train[colnames_select]
    x_test_sel = X_Test[colnames_select]
    
    return x_train_sel, x_test_sel


#
  
def get_data():
    dataset = dc._init_()
   
    #dataset.plot.hist(bins=20, stacked=True, figsize=(10,10))
    #dataset.plot.hist(by=dataset.Demmand, figsize=(25,10), stacked= True )
    y = dataset["Demmand"]
    x = dataset.drop("Demmand", 1)
    x["dt"] = pandas.to_datetime(x["dt"]).dt.dayofyear
    x = set_dummies(x)
    y = y.replace("High", 1)
    y = y.replace("Low", 0)
    
    
    
 
    x["clouds.all"] = processOutliers(x["clouds.all"], x)
    x["main.humidity"] = processOutliers(x["main.humidity"], x)
    x["main.pressure"] = processOutliers(x["main.pressure"], x)
    x["main.temp"] = processOutliers(x["main.temp"], x)
    x["main.temp_max"] = processOutliers(x["main.temp_max"], x)
    x["main.temp_min"] = processOutliers(x["main.temp_min"], x)
    x["wind.deg"] = processOutliers(x["wind.deg"], x)
    x["wind.speed"] = processOutliers(x["wind.speed"], x)

   
    X_Train, X_Test, Y_Train, Y_Test = train_test_split(x, y, train_size=0.75, random_state=2)
    final_train_case_x, final_test_case_x = feature_selec(X_Train, Y_Train, X_Test, x)
    return  final_train_case_x, final_test_case_x ,Y_Train, Y_Test

data = get_data()
    



