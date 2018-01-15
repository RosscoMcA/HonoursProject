# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 13:26:48 2018

@author: Ross
"""

from pandas import read_csv
import pandas
import matplotlib.pyplot as plt
from sklearn import svm 
import numpy as np
import DataConditioning as dc
from matplotlib import interactive
interactive(True)


def get_data():
    dataset = dc._init_()
   
    dataset.plot.hist(bins=20, stacked=True, figsize=(10,10))
    '''dataset = set_dummies([], dataset)'''
   
    return dataset

data = get_data()
get_data()  
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


#X_Train, X_Test, Y_Train, Y_Test = train_test_split(x, y, train_size=70, random_state=1)



def feature_selec():
    select = sklearn.feature_selection.SelectKBest(k=8)
    select_feature = select.fit(X_Train, Y_Train)
    indic_sel = select_feature.get_support(indices=True)
    colnames_select = [x.columns[i] for i in indic_sel]
    
    x_train_sel = X_Train[colnames_select]
    x_test_sel = X_Test[colnames_select]
    
    return x_train_sel, x_test_sel


#final_train_case_x, final_test_case_x = feature_selec()
  
    
def set_dummies(dummy_Items, dataset):
    
    dataset = pandas.get_dummies(columns= dummy_Items)



