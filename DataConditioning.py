# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 21:43:01 2017

@author: Ross
"""
import pandas 
from pandas import read_csv
from pandas import read_json
import matplotlib.pyplot as plt
import numpy as np 
import scipy as sp
 
attendaces = read_csv("A&E Daily Attendances.csv")
weather = read_json("bulkweather.json")

print(attendaces.describe())
print(weather.describe)