#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created         March 27 2020

Updated         June 18 2020

@author         celiacailloux/ceshuca

Sample          EXAMPLE

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

# plt.close('all')
" change to match experiment"
C1s_CC_BE = 284.62

import_XPS_data             = True
Survey                      = False 
Valence_SI                    = True
Valence_NI                  = False

Element_Scan_NI             = False
Element_Scan_SI             = False

save_plot                   = True 

element = 'Pd NI' 
element = 'ZnLMM NI'
element = 'Pd'
# element = 'Zn'
# element = 'ZnLMM'
element = 'Al'
element = 'Cu'

Single_Element              = False
Single_Element_Normalized   = False

" --------------------------------------------------------------- Create Paths"
if import_XPS_data:
    " don't change "
    # user_path       = osfunc.get_user_path()
    # XPS_data_dir    = r'OneDrive - Danmarks Tekniske Universitet/PhD/Data/XPS/'
    # XPS_data_path   = join_paths(user_path, XPS_data_dir)
    
    
    " change to match experiment"
    " #1 "    
    exp_ID1 = 'Cu foil fresh DP'
    # Is used as label when plotting!
    sample_description = exp_ID1     
    # std or XPS
    measurement_type1            = 'DP'    
    XPS_exps = get_XPS_exps(exp_ID1, composition = '', XRD_phase = '')


    if Survey:
        " change to match experiment"
        exp_Survey1  = r''
        XPS_exps[exp_ID1]['Paths']['Survey']['path']  = exp_Survey1
        XPS_exps[exp_ID1]['Paths']['Survey']['measurement type'] = 'std' 

    if Valence_SI: #V for valence
        " change to match experiment"
        exp_Valence1  = r'C:/Users/ceshuca/OneDrive - Danmarks Tekniske Universitet/PhD/Data/XPS/20200626 Cu, PdZn, Al2O3/20200626 Cu, PdZn, Al2O3/Cu foil fresh DP/Valence - NF - SI - Cu foil fresh - DP.xlsx'
        XPS_exps[exp_ID1]['Paths']['V']['path'] = exp_Valence1
        XPS_exps[exp_ID1]['Paths']['V']['measurement type'] = measurement_type1         
        
    if Valence_NI: #V for valence
        " change to match experiment"
        exp_Valence1  = r''
        XPS_exps[exp_ID1]['Paths']['V']['path'] = exp_Valence1
        XPS_exps[exp_ID1]['Paths']['V']['measurement type'] = measurement_type1         
        
    if Element_Scan_NI:
        " change to match experiment"
        exp_SingleElement_NI1  = r''
        
        " don't change "
        XPS_exps[exp_ID1]['Paths']['SE']['Pd NI'] = {}            
        XPS_exps[exp_ID1]['Paths']['SE']['Pd NI']['band'] = '3d'
        XPS_exps[exp_ID1]['Paths']['SE']['Pd NI']['sheet_name'] = 'Pd3d Scan'
        XPS_exps[exp_ID1]['Paths']['SE']['Pd NI']['path'] = exp_SingleElement_NI1
        XPS_exps[exp_ID1]['Paths']['SE']['Pd NI']['measurement type'] = measurement_type1 
        
        XPS_exps[exp_ID1]['Paths']['SE']['Zn NI'] = {}
        XPS_exps[exp_ID1]['Paths']['SE']['Zn NI']['band'] = '2p'
        XPS_exps[exp_ID1]['Paths']['SE']['Zn NI']['sheet_name'] = 'Zn2p Scan'
        XPS_exps[exp_ID1]['Paths']['SE']['Zn NI']['path'] = exp_SingleElement_NI1
        XPS_exps[exp_ID1]['Paths']['SE']['Zn NI']['measurement type'] = measurement_type1 
        
        XPS_exps[exp_ID1]['Paths']['SE']['ZnLMM NI'] = {}
        XPS_exps[exp_ID1]['Paths']['SE']['ZnLMM NI']['band'] = 'LMM'
        XPS_exps[exp_ID1]['Paths']['SE']['ZnLMM NI']['sheet_name'] = 'ZnLMM Scan'
        XPS_exps[exp_ID1]['Paths']['SE']['ZnLMM NI']['path'] = exp_SingleElement_NI1
        XPS_exps[exp_ID1]['Paths']['SE']['ZnLMM NI']['measurement type'] = measurement_type1 
        
        XPS_exps[exp_ID1]['Paths']['SE']['Al NI'] = {}  
        XPS_exps[exp_ID1]['Paths']['SE']['Al NI']['band'] = '2p'
        XPS_exps[exp_ID1]['Paths']['SE']['Al NI']['sheet_name'] = 'Al2p Scan'
        XPS_exps[exp_ID1]['Paths']['SE']['Al NI']['path'] = exp_SingleElement_NI1
        XPS_exps[exp_ID1]['Paths']['SE']['Al NI']['measurement type'] = measurement_type1        
        
    if Element_Scan_SI: #SE for single element
        " change to match experiment "
        exp_SingleElement_SI1  = \
            r'C:/Users/ceshuca/OneDrive - Danmarks Tekniske Universitet/PhD/Data/XPS/20200626 Cu, PdZn, Al2O3/20200626 Cu, PdZn, Al2O3/Cu foil fresh DP/Element Scan - NF - SI - Cu foil fresh - DP.xlsx'
        
        " don't change "
        XPS_exps[exp_ID1]['Paths']['SE']['Pd'] = {}  
        XPS_exps[exp_ID1]['Paths']['SE']['Pd']['band'] = '3d'
        XPS_exps[exp_ID1]['Paths']['SE']['Pd']['sheet_name'] = 'Pd3d Scan'
        XPS_exps[exp_ID1]['Paths']['SE']['Pd']['path'] = exp_SingleElement_SI1
        XPS_exps[exp_ID1]['Paths']['SE']['Pd']['measurement type'] = measurement_type1 
        
        XPS_exps[exp_ID1]['Paths']['SE']['Zn'] = {}  
        XPS_exps[exp_ID1]['Paths']['SE']['Zn']['band'] = '2p'
        XPS_exps[exp_ID1]['Paths']['SE']['Zn']['sheet_name'] = 'Zn2p Scan'
        XPS_exps[exp_ID1]['Paths']['SE']['Zn']['path'] = exp_SingleElement_SI1
        XPS_exps[exp_ID1]['Paths']['SE']['Zn']['measurement type'] = measurement_type1 
        
        XPS_exps[exp_ID1]['Paths']['SE']['ZnLMM'] = {}  
        XPS_exps[exp_ID1]['Paths']['SE']['ZnLMM']['band'] = 'LMM'
        XPS_exps[exp_ID1]['Paths']['SE']['ZnLMM']['sheet_name'] = 'ZnLMM Scan'
        XPS_exps[exp_ID1]['Paths']['SE']['ZnLMM']['path'] = exp_SingleElement_SI1
        XPS_exps[exp_ID1]['Paths']['SE']['ZnLMM']['measurement type'] = measurement_type1 
        
        XPS_exps[exp_ID1]['Paths']['SE']['Al'] = {}  
        XPS_exps[exp_ID1]['Paths']['SE']['Al']['band'] = '2p'
        XPS_exps[exp_ID1]['Paths']['SE']['Al']['sheet_name'] = 'Al2p Scan'
        XPS_exps[exp_ID1]['Paths']['SE']['Al']['path'] = exp_SingleElement_SI1
        XPS_exps[exp_ID1]['Paths']['SE']['Al']['measurement type'] = measurement_type1 

        # XPS_exps[exp_ID1]['Paths']['SE']['Zn'] = {}  
        # XPS_exps[exp_ID1]['Paths']['SE']['Zn']['band'] = '2p'
        # XPS_exps[exp_ID1]['Paths']['SE']['Zn']['sheet_name'] = 'Zn2p Scan'
        # XPS_exps[exp_ID1]['Paths']['SE']['Zn']['path'] = exp_SingleElement_SI1
        # XPS_exps[exp_ID1]['Paths']['SE']['Zn']['measurement type'] = measurement_type1 
        

        # XPS_exps[exp_ID1]['Paths']['SE']['Zn'] = {}  
        # XPS_exps[exp_ID1]['Paths']['SE']['Zn']['band'] = '2p'
        # XPS_exps[exp_ID1]['Paths']['SE']['Zn']['sheet_name'] = 'Zn2p Scan'
        # XPS_exps[exp_ID1]['Paths']['SE']['Zn']['path'] = exp_SingleElement_SI1
        # XPS_exps[exp_ID1]['Paths']['SE']['Zn']['measurement type'] = measurement_type1 
        ''' add Al, O KLM1 etc.... '''
    
    " Create new instances of the class XPSData."
    exp1 = XPSData(XPS_ID = exp_ID1,
                   XPS_exps = XPS_exps,
                   sample_description = sample_description, 
                   C1s_CC_BE = C1s_CC_BE) 
    
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

if Valence_NI:
    
    exp1.quick_plot_valence(save_plot = save_plot)
    
if Valence_SI:

    'fill out'
    exp1.quick_plot_valence(save_plot = save_plot)
    
if Element_Scan_NI:
    """ Doublet """
    exp1.quick_plot_single_element_normalized(element = element, 
                                              save_plot = save_plot, main_peak_only = False)
    """ Main peak """    
    exp1.quick_plot_single_element_normalized(element = element, 
                                              save_plot = save_plot, main_peak_only = True)    

if Element_Scan_SI:
    """ Doublet """
    exp1.quick_plot_single_element_normalized(element = element, 
                                              save_plot = save_plot, main_peak_only = False)
    """ Main peak """    
    exp1.quick_plot_single_element_normalized(element = element, 
                                              save_plot = save_plot, main_peak_only = True)
    
if Single_Element_Normalized:
    element = 'Pd N'
    """
    Doublet
    """

    exp1.quick_plot_single_element_normalized(element = element, 
                                              save_plot = save_plot, main_peak_only = False)
    """
    Main peak
    """    
    exp1.quick_plot_single_element_normalized(element = element, 
                                              save_plot = save_plot, main_peak_only = True)    

    
