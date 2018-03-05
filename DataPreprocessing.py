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
from sklearn import preprocessing
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


def select_from_model(train_x, test_x, classifier):
    select = sklearn.feature_selection.SelectFromModel(classifier, prefit=True)
    X_Train_Results = select.transform(train_x)
    X_Test_Results = select.transform(test_x)
    
    
    
    return X_Train_Results, X_Test_Results
   



def feature_selec(X_Train, Y_Train, X_Test, x, number=None):
    
        
    select = sklearn.feature_selection.SelectPercentile(percentile=80)
    select_feature = select.fit(X_Train, Y_Train)
    indic_sel = select_feature.get_support(indices=True)
    colnames_select = [x.columns[i] for i in indic_sel]
    
    x_train_sel = X_Train[colnames_select]
    if(X_Test is None):
    
        return x_train_sel
    
    x_test_sel = X_Test[colnames_select]
    
    return x_train_sel, x_test_sel


def dimensionality_reduction(data):

    pca = PCA(n_components=12)
    X_PCA = pandas.DataFrame(pca.fit_transform(data))

    return X_PCA

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
    
    
    '''
    label_encoder = preprocessing.LabelEncoder()
    
    label_encoder.fit(dataset["description"])
    
    dataset["description"] = label_encoder.transform(dataset["description"])
    '''
    dataset = set_dummies(dataset, ["description"])
     
     
     
     
    dataset =dataset.groupby([dataset["Location Name"], dataset["dt"] ]).median().reset_index()
    dataset = set_dummies(dataset, ["Location Name"])
    dataset = dataset.rename(columns={"Location Name": "Treatment Location Name"})
    
    dataset = dataset.join(classify, rsuffix="_y")
    dataset = dataset.reset_index()
    dataset=  dataset.drop_duplicates()
    dataset = dataset.drop(["Location Name", "dt_y", "index"], 1)
    
   
   
    y = dataset["Demmand"]
    
    dataset = dataset.drop("Demmand", 1)
    
    
  
    
    x= dataset
    
    x["dt"] = pandas.to_datetime(x["dt"])
    x["day"]= x["dt"].apply(lambda x: int(x.day))
    x["month"] = x["dt"].apply(lambda x: int(x.month))
    
    '''
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("GLASGOW ROYAL INFIRMARY", 1)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("INVERCLYDE ROYAL HOSPITAL", 2)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("NEW VICTORIA HOSPITAL", 3)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("QUEEN ELIZABETH UNIVERSITY HOSPITAL", 4)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("ROYAL ALEXANDRA HOSPITAL", 5)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("ROYAL HOSPITAL FOR CHILDREN", 6)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("STOBHILL HOSPITAL", 7)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("VALE OF LEVEN GENERAL HOSPITAL", 8)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("WEST GLASGOW", 9)
    '''
    x= x.drop(["dt"], 1)
    
    
    
    

   
    
    dummy = read_csv("dummy_model")
  
    final_test_case_x = x.reindex(columns=dummy.columns, fill_value=0)

    final_test_case_x = final_test_case_x.drop(["Unnamed: 0"], 1)
    return  final_test_case_x, y
  
    


def get_data_builder():
    
    dataset = dc._init_()
    
    classify = pandas.DataFrame()
    classify["Demmand"] = dataset["Demmand"]
    classify["Treatment Location Name"] = dataset["Treatment Location Name"]
    classify["dt"] = dataset["dt"]
    classify = classify.replace("High", 1)
    classify = classify.replace("Low", 0)
    classify = classify.groupby([dataset["Treatment Location Name"], dataset["dt"] ]).median().reset_index(drop=True)
    
    test_set, test_y = get_data_tester()
    

    y_entries = [test_y, dataset["Demmand"]]
    y = pandas.concat(y_entries, ignore_index=True).reset_index(drop=True)
    
    
    dataset = dataset.drop("Demmand", 1)
    
    '''
    label_encoder = preprocessing.LabelEncoder()
    
    label_encoder.fit(dataset["description"])
    
    dataset["description"] = label_encoder.transform(dataset["description"])
    '''
    
     
    x = pandas.concat([test_set, dataset], ignore_index=True).reset_index(drop=True)
    
    dataset = set_dummies(dataset, ["description"])
     
     
     
     
    dataset =dataset.groupby([dataset["Treatment Location Name"], dataset["dt"] ]).median().reset_index()
    dataset = set_dummies(dataset, ["Treatment Location Name"])
    
    
    
    
    
    
    dataset = dataset.join(classify, rsuffix="_y")
    
    dataset=  dataset.drop_duplicates()

    
    
   
  
    
    #dataset.plot.hist(bins=20, stacked=True, figsize=(10,10))
    #dataset.plot.hist(by=dataset.Demmand, figsize=(25,10), stacked= True )
    
    y = dataset["Demmand"]
    
    
    dataset = dataset.drop("Demmand", 1)
    
    
    x = dataset
    
    x.index.name = None
    x= x.reset_index(drop= True)
    
    
    x["dt"] = pandas.to_datetime(x["dt"])
    x["day"]= x["dt"].apply(lambda x: int(x.day))
    x["month"] = x["dt"].apply(lambda x: int(x.month))
    
    
    
    
    
    '''
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("GLASGOW ROYAL INFIRMARY", 1)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("INVERCLYDE ROYAL HOSPITAL", 2)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("NEW VICTORIA HOSPITAL", 3)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("QUEEN ELIZABETH UNIVERSITY HOSPITAL", 4)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("ROYAL ALEXANDRA HOSPITAL", 5)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("ROYAL HOSPITAL FOR CHILDREN", 6)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("STOBHILL HOSPITAL", 7)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("VALE OF LEVEN GENERAL HOSPITAL", 8)
    x["Treatment Location Name"] = x["Treatment Location Name"].replace("WEST GLASGOW", 9)
    
    '''
    
    x= x.drop(["dt"], 1)
    
    x = x.astype(int)
    
    y= y.astype(int)
    
    x= x.drop_duplicates()
    
    
    
    
    
    

    
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
    
   
    
    X_Train, X_Test, Y_Train, Y_Test = train_test_split(x, y, train_size=0.9, random_state=2)
    
    
    
    final_train_case_x, final_test_case_x = feature_selec(X_Train, Y_Train, X_Test, x)
    
    set_reference_model(final_train_case_x)
    
    eval_x, cv_x, eval_y, cv_y= train_test_split(final_train_case_x, Y_Train, test_size=0.1, random_state=2)
    
   
    return  final_train_case_x, eval_x, final_test_case_x ,Y_Train, eval_y, Y_Test
    

data = get_data_builder()
    

