# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 13:28:09 2018

@author: Ross
"""
import pandas
from pandas import read_csv
import matplotlib.pyplot as plt
from sklearn import svm 
import numpy as np
import scipy as sp
import DataPreprocessing as data_pre

from sklearn.externals import joblib


x,y, test_x, test_y = data_pre.get_data()

def create_model():
    
    
    print("Creating the model")
    classifier = svm.SVC(C=1, kernel="rbf")
    
    classifier.fit(x, y)
    print("Model is built")
    
    model_per = joblib.dump(classifier, "A&EModel")
    
    
    
    test_Model(classifier)
    
    

def test_Model(prediction_model):
    #For every test item assess the result and display a correct 
    # total and accuracy percentage
    predict_results = [int(a) for a in prediction_model.predict(test_x)]
    correct_total = sum(int(a==y) for a, y in zip(predict_results, test_y))
    
    
    print("Results of prediction are: ")
    print("%s of %s values correct." % (correct_total, len(Y_Test)))
    print("an Accuracy of %s" %((correct_total/len(Y_Test))*100))

create_model()
    
    
