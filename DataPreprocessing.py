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
import test_conditioning 
from matplotlib import interactive
from sklearn.cross_validation import train_test_split
from sklearn.decomposition import PCA
import sklearn.feature_selection
from datetime import datetime

interactive(True)


def set_dummies(dataset, case=None):
    if(case!= None):
        
        dataset = pandas.get_dummies(dataset, columns=case)
    
    else :
        dataset = pandas.get_dummies(dataset)
    
    return dataset
    

def set_reference_model(dataset):
    dataset.to_csv("Dummy_model")


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






def feature_selec(X_Train, Y_Train, X_Test, x, number=None):
    
        
    select = sklearn.feature_selection.SelectPercentage()
    select_feature = select.fit(X_Train, Y_Train)
    indic_sel = select_feature.get_support(indices=True)
    colnames_select = [x.columns[i] for i in indic_sel]
    
    x_train_sel = X_Train[colnames_select]
    if(X_Test is None):
    
        return x_train_sel
    
    x_test_sel = X_Test[colnames_select]
    
    return x_train_sel, x_test_sel

#

def get_data_tester():
    
    dataset = test_conditioning.data
    
    classify = pandas.DataFrame()
    classify["Demmand"] = dataset["Demmand"]
    classify["Location Name"] = dataset["Location Name"]
    classify["dt"] = dataset["dt"]
    classify = classify.replace("High", 1)
    classify = classify.replace("Low", 0)
    classify = classify.groupby([dataset["Location Name"], dataset["dt"] ]).median().reset_index()
    

    dataset = dataset.drop("Demmand", 1)
    dataset = set_dummies(dataset, ["description"])
    
    
    
    
    dataset =dataset.groupby([dataset["Location Name"], dataset["dt"] ]).median().reset_index()
    dataset = dataset.rename(columns={"Location Name": "Treatment Location Name"})
    dataset = set_dummies(dataset, ["Treatment Location Name"])
    dataset = dataset.join(classify, rsuffix="_y")
    dataset = dataset.reset_index()
    dataset=  dataset.drop_duplicates()
    dataset = dataset.drop(["Location Name", "dt_y", "index"], 1)
    
    
   
    y = dataset["Demmand"]
    
    dataset = dataset.drop("Demmand", 1)
    
    
    x = dataset
    
    

   
    
    final_test_case_x = x
    
    return final_test_case_x, y
  
    


def get_data_builder():
    
    dataset = dc._init_()
    
    classify = pandas.DataFrame()
    classify["Demmand"] = dataset["Demmand"]
    classify["Treatment Location Name"] = dataset["Treatment Location Name"]
    classify["dt"] = dataset["dt"]
    classify = classify.replace("High", 1)
    classify = classify.replace("Low", 0)
    classify = classify.groupby([dataset["Treatment Location Name"], dataset["dt"] ]).median().reset_index()
    
    

    dataset = dataset.drop("Demmand", 1)
    dataset = set_dummies(dataset, ["description"])
    
    
    
    
    dataset =dataset.groupby([dataset["Treatment Location Name"], dataset["dt"] ]).median().reset_index()
    dataset = set_dummies(dataset, ["Treatment Location Name"])
    dataset = dataset.join(classify, rsuffix="_y")
    dataset = dataset.reset_index()
    dataset=  dataset.drop_duplicates()
    dataset = dataset.drop(["Treatment Location Name", "dt_y", "index"], 1)
    
    test_set, test_y = get_data_tester()
    
    #dataset.plot.hist(bins=20, stacked=True, figsize=(10,10))
    #dataset.plot.hist(by=dataset.Demmand, figsize=(25,10), stacked= True )
    
    y_entries = [test_y, dataset["Demmand"]]
    y = pandas.concat(y_entries, ignore_index=True)
    
    dataset = dataset.drop("Demmand", 1)
    
    
    x = pandas.concat([test_set, dataset], ignore_index=True)
    x["dt"] = pandas.to_datetime(x["dt"])
    x["day"]= x["dt"].apply(lambda x: int(x.day))
    x["month"] = x["dt"].apply(lambda x: int(x.month))
    
    x=  x.drop("dt", 1)
   
    
    
    
    
    
    '''
    x["clouds.all"] = processOutliers(x["clouds.all"], x)
    x["main.humidity"] = processOutliers(x["main.humidity"], x)
    x["main.pressure"] = processOutliers(x["main.pressure"], x)
    x["main.temp"] = processOutliers(x["main.temp"], x)
    x["main.temp_max"] = processOutliers(x["main.temp_max"], x)
    x["main.temp_min"] = processOutliers(x["main.temp_min"], x)
    x["wind.deg"] = processOutliers(x["wind.deg"], x)
    x["wind.speed"] = processOutliers(x["wind.speed"], x)
    '''

    x= x.replace(np.NaN, 0)
    X_Train, X_Test, Y_Train, Y_Test = train_test_split(x, y, train_size=0.8, random_state=2)
    final_train_case_x, final_test_case_x = feature_selec(X_Train, Y_Train, X_Test, x)
    
    set_reference_model(final_train_case_x)
    return  final_train_case_x, final_test_case_x ,Y_Train, Y_Test
    

data = get_data_builder()
    



