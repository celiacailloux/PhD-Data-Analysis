#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 11:49:16 2019

@author: celiacailloux
"""
#import csv
#
#reffiles = ['test_ref1.csv']
#
#path = reffiles[0]
#
#with open(path) as file:
#    reader = csv.reader(file, delimiter = ',')
#    for column in reader:
#        angles = column[0]
#        spectrum = column[1]
#        
#print(angles)
    
import pandas as pd
import numpy as np

reffiles = ['test_ref1.csv']

path = reffiles[0]
file = pd.read_csv(path, delimiter = ',',names = ['angles', 'spectrum'], header = None)

angles = file['angles']
spectrum = file['spectrum']


