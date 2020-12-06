# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 16:12:24 2018

@author: surfcat
"""

import pickle

f = open('obj/' + 'calibrations_direct_CO_pressure_corrected_4' + '.pkl', 'rb')
mamawebo = pickle.load(f)
f.close()

print(mamawebo)