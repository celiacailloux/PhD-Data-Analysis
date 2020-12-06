#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created         March 27 2020

Updated         July 02 2020

@author         celiacailloux/ceshuca

Sample          SINGLE ELEMENT

NF = non fitted
NI = normalizd intensity
SI = stacked intensity
SC = single scan
DP = depth profiling
NS = non charge-shiftet
NC C1s = not C1s corrected
C C1s = C1s corrected
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
C1s_CC_BE = 285.48

import_XPS_data             = True

Element_Scan_NI             = True
Element_Scan_SI             = False

save_plot                   = False
save_legend                 = True

elements = [
    # 'Al',
    # 'C',
    # 'Pd',
    # 'Zn',
    # # 'ZnLMM',
    # # 'OKL',
    # 'Valence'
    # 'Al NI',
    # 'C NI',
    # 'Pd NI',
    # 'Zn NI',
    # 'ZnLMM NI',
    # 'OKL NI',
    'Valence NI'
    # 'Cu', 
    ]

" --------------------------------------------------------------- Create Paths"
if import_XPS_data:        
    " change to match experiment"
    " #1 "    
    exp_ID1 = 'SP32 Pd1Zn2 w Al2O3 fresh DP'
    # Is used as label when plotting!
    sample_description = exp_ID1     
    # std or XPS
    measurement_type1            = 'DP'    
    XPS_exps = get_XPS_exps(exp_ID1, 
                            composition = '', 
                            XRD_phase = '')     
        
    if Element_Scan_NI:
        " change to match experiment"
        exp_SingleElement_NI1  = \
            r'C:/Users/ceshuca/OneDrive - Danmarks Tekniske Universitet/PhD/Data/XPS/20200626 Cu, PdZn, Al2O3/20200626 Cu, PdZn, Al2O3/SP32 Pd1Zn2 w Al2O3 fresh DP/Element Scan - NF - NI - SP32 Pd1Zn2 - DP.xlsx'
        
        element = 'Pd NI'
        if element in elements:
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}            
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = '3d'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'Pd3d Scan'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_NI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1 

        element = 'Zn NI'
        if element in elements:            
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = '2p'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'Zn2p Scan'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_NI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1 
        
        element = 'ZnLMM NI'
        if element in elements:    
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = 'LMM'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'ZnLMM Scan'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_NI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1 

        element = 'Al NI'
        if element in elements:            
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}  
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = '2p'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'Al2p Scan'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_NI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1        

        element = 'OKL NI'
        if element in elements:       
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}  
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = 'KL'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'OKL1 Scan'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_NI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1             

        element = 'C NI'
        if element in elements:            
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}  
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = '1s'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'C1s Scan'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_NI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1  
        
        element = 'Valence NI'
        if element in elements:            
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}  
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = 'Valence'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'Valence'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_NI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1                   
        
    if Element_Scan_SI: #SE for single element
        " change to match experiment "
        exp_SingleElement_SI1  = \
            r'C:/Users/ceshuca/OneDrive - Danmarks Tekniske Universitet/PhD/Data/XPS/20200626 Cu, PdZn, Al2O3/20200626 Cu, PdZn, Al2O3/SP32 Pd1Zn2 w Al2O3 fresh DP/Element Scan - NF - NI - SP32 Pd1Zn2 - DP.xlsx'
        
        " don't change "
        element = 'Pd'
        if element in elements:            
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}  
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = '3d'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'Pd3d Scan'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_SI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1 
        
        element = 'Zn'
        if element in elements:               
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}  
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = '2p'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'Zn2p Scan'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_SI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1 
        
        element = 'ZnLMM'
        if element in elements:               
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}  
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = 'LMM'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'ZnLMM Scan'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_SI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1 
        
        element = 'Al'
        if element in elements:               
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}  
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = '2p'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'Al2p Scan'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_SI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1 
        
        element = 'OKL'
        if element in elements:       
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}  
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = 'KL'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'OKL1 Scan'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_SI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1 
        
        element = 'C'
        if element in elements:
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}  
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = '1s'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'C1s Scan'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_SI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1 
        
        element = 'Valence'
        if element in elements:            
            XPS_exps[exp_ID1]['Paths']['SE'][element] = {}  
            XPS_exps[exp_ID1]['Paths']['SE'][element]['band'] = 'Valence'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['sheet_name'] = 'Valence'
            XPS_exps[exp_ID1]['Paths']['SE'][element]['path'] = exp_SingleElement_SI1
            XPS_exps[exp_ID1]['Paths']['SE'][element]['measurement type'] = measurement_type1              
        ''' add Al, O KLM1 etc.... '''
    
    " Create new instances of the class XPSData."
    exp1 = XPSData(XPS_ID = exp_ID1,
                   XPS_exps = XPS_exps,
                   sample_description = sample_description, 
                   C1s_CC_BE = C1s_CC_BE) 
    
    save_as_pickle(pkl_data = XPS_exps, pkl_name = 'XPS_exps')
    
else:
    XPS_exps = get_saved_pickle(pkl_name = 'XPS_exps')
    
" change to match experiment"
exp1.DPs_to_plot = 1


if Element_Scan_NI:
    for element in elements:
        """ Doublet """
        exp1.quick_plot_SE(element = element, 
                           save_plot = save_plot, 
                           save_legend = save_legend,                           
                           main_peak_only = False, 
                           SE_type = 'NI')
        """ Main peak """    
        exp1.quick_plot_SE(element = element, 
                           save_plot = save_plot, 
                           save_legend = save_legend,                           
                           main_peak_only = True,
                           SE_type = 'NI') 
        
if Element_Scan_SI:
    for element in elements:
        """ Doublet """
        exp1.quick_plot_SE(element = element, 
                           save_plot = save_plot,
                           save_legend = save_legend,
                           main_peak_only = False, 
                           SE_type = 'SI')
        """ Main peak """    
        exp1.quick_plot_SE(element = element, 
                           save_plot = save_plot, 
                           save_legend = save_legend,
                           main_peak_only = True,
                           SE_type = 'SI')        

# if Element_Scan_SI:
#     for element in elements:
#         """ Doublet """
#         exp1.quick_plot_single_element_normalized(element = element, 
#                                                   save_plot = save_plot, main_peak_only = False)
#         """ Main peak """    
#         exp1.quick_plot_single_element_normalized(element = element, 
#                                                   save_plot = save_plot, main_peak_only = True)
 