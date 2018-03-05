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
import matplotlib.pyplot as plt
from pandas_ml import ConfusionMatrix
from sklearn.externals import joblib


class ModellingTest: 
    
    def __init__(self):
        self.x, self.eval_x, self.test_x,self.y, self.eval_y, self.test_y = data_pre.get_data_builder()
        
        create_model(self)

def create_model(self):
    
    
    print("Creating the model")
    classifier = svm.NuSVC(kernel="rbf", gamma=1e-4)
    
    
    classifier.fit(self.x, self.y)
    
    
    
    
    
    
    
    print("Model is built")
    
    joblib.dump(classifier, "A&EModel")
    
    
    
    assess_Model(self, classifier)
    

    

def assess_Model(self, prediction_model):
    #For every test item assess the result and display a correct 
    # total and accuracy percentage
    predict_results = [int(a) for a in prediction_model.predict(self.eval_x)]
    correct_total = sum(int(a==y) for a, y in zip(predict_results, self.eval_y))
    
    
    print("Results of evaluation are: ")
    print("%s of %s values correct." % (correct_total, len(self.eval_y)))
    print("an Accuracy of %s" %((int(correct_total)/len(self.eval_y))*100))
    
    test_model(self,prediction_model)

def test_model(self, prediction_model):
    predict_results = [int(a) for a in prediction_model.predict(self.test_x)]
    correct_total = sum(int(a==y) for a, y in zip(predict_results, self.test_y))
    
    
    print("Results of test are: ")
    print("%s of %s values correct." % (correct_total, len(self.test_y)))
    print("an Accuracy of %s" %((correct_total/len(self.test_y))*100))
    
    conf = ConfusionMatrix(predict_results, self.test_y)

    print(conf)
    
ModellingTest()    
