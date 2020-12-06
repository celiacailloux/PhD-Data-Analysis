#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created         March 27 2020

Updated         July 02 2020

@author         celiacailloux/ceshuca

Script type     EXAMPLE SURVEY

NF = non fitted
NI = normalizd intensity
SI = stacked intensity
SC = single scan
DP = depth profiling
NS = non charge-shiftet
"""


from XPSData import get_XPS_exps, XPSData
import OSfunctions as osfunc
from OSfunctions import create_file_path,  get_user_path, join_paths
from PickleFunctions import save_as_pickle, get_saved_pickle

#import PlottingFunctions as pltF
import matplotlib.pyplot as plt
import pandas as pd


import_XPS_data             = True

Survey                      = True

save_plot                   = True 

" -------------------------------------------------------------- CREATE PATHS "
if import_XPS_data:
    " change to match experiment"
    " #1 "    
    exp_ID1 = 'Cu foil fresh'
    # Is used as label when plotting!
    sample_description = exp_ID1     
    # std or XPS
    measurement_type1            = 'std'    
    XPS_exps = get_XPS_exps(exp_ID1, composition = '', XRD_phase = '')


    if Survey:
        " change to match experiment"
        exp_Survey1  = r'C:/Users/ceshuca/OneDrive - Danmarks Tekniske Universitet/PhD/Data/XPS/20200626 Cu, PdZn, Al2O3/20200626 Cu, PdZn, Al2O3/Cu foil fresh/Survey - STD.xlsx'
        XPS_exps[exp_ID1]['Paths']['Survey']['path']  = exp_Survey1
        XPS_exps[exp_ID1]['Paths']['Survey']['measurement type'] = measurement_type1 
    
    " Create new instances of the class XPSData."
    exp1 = XPSData(XPS_ID = exp_ID1,
                   XPS_exps = XPS_exps,
                   sample_description = sample_description) 
    
    save_as_pickle(pkl_data = XPS_exps, pkl_name = 'XPS_exps')
    
else:
    XPS_exps = get_saved_pickle(pkl_name = 'XPS_exps')
    
# print(exp1.data_valence['data'].head())
if Survey:
    " Survey plotting "
   
    exp1.data_survey['data']
    exp1.data_survey['survey peaks']
      
    exp1.quick_plot_survey(identification_quantification = True, 
                                        save_plot = save_plot)    
    # print(exp1.data_survey['survey peaks'].head(5))
