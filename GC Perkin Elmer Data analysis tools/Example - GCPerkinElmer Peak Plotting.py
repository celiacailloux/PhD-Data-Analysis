# -*- coding: utf-8 -*-
"""
Created             Jun 2020

@author:            ceshuca

Last Edited         Aug 27 2020

Experiment          Example on plotting raw GC files

"""
from GCPerkinElmerPlotting import GC_EC_analyzer
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
#import fit_info
from pylab import rcParams
import os
from OSfunctions import get_application_data_location, join_paths
from PickleFunctions import save_as_pickle, get_saved_pickle
from PlottingFunctions import global_savefig


rcParams['figure.figsize'] = 6, 6
#fonts for matplotlib
font = {#'family' : 'Palatino Linotype',
        'size'   : 14}
mpl.rc('font', **font)

#plt.close('all')

# ---------------------------------------------------------------------------
assign_important_parameters     = True
object_initialization           = True                       

# ---------------------------------------------------------------------------
save_plot                   = True

show_peak_plotting          = True
show_fitting                = False
show_fitting_all_figures    = False

# ---------------------------------------------------------------------------
if assign_important_parameters:

    filepath = \
        r'O:\list-SurfCat\setups\307-059-largeCO2MEA\Data\Celia - EC largeCO2MEA data\GC - Perkin Elmer\20200827 Ag CO2R Staircase'
    GC_plot_title = os.path.basename(filepath)
    
    """
    Assign important variables/parameters for analysis and plotting functions 
    in the GC_EC_analyzer object
    
    Specify 
        * the i,v measurement id (can be found in the cinfdata database (?)) 
        * the catalyst mass loading (mg/cm2) (?)
        * the measured ECSA (ECSA/geometric)
    Optional
        * the number of raw files to analyse (raw_to_analyse / a slice object)
        * the time correction (s or min?)
    """    
    raw_to_analyse = slice(0,13)#None                               
    time_correction = 0     

    if object_initialization:
        
        " potentially change "
        offset_TCD = 0
        offset_FID = 0
        
        fit_info = {}
        
        fit_info['settings'] = {}
        fit_info['settings']['background_range']    = 0.1  #minutes, used for integration
        fit_info['settings']['flow_rate']           = 10    #sccm
        
        fit_info['TCD'] = {}
        fit_info['FID'] = {}
       
        fit_info['TCD']['H2'] = {}
        peak_center = 2.9 + offset_TCD                                            
        peak_width = 0.4
        fit_info['TCD']['H2']['start'] = peak_center-peak_width/2
        fit_info['TCD']['H2']['end'] = peak_center+peak_width/2   
    
        fit_info['TCD']['O2'] = {}
        peak_center = 3.85   + offset_TCD                           
        peak_width = 0.3   
        fit_info['TCD']['O2']['start'] = peak_center-peak_width/2
        fit_info['TCD']['O2']['end'] = peak_center+peak_width/2  
        
        fit_info['TCD']['N2'] = {}
        peak_center = 4.75 + offset_TCD                                                
        peak_width = 0.6 
        fit_info['TCD']['N2']['start'] = peak_center-peak_width/2       
        fit_info['TCD']['N2']['end'] = peak_center+peak_width/2  
        
        fit_info['TCD']['CO'] = {}
        peak_center = 9.0        + offset_TCD
        peak_width = 1.2    
        fit_info['TCD']['CO']['start'] = peak_center-peak_width/2
        fit_info['TCD']['CO']['end'] = peak_center+peak_width/2  
        
        fit_info['TCD']['CO2'] = {}
        peak_center =  13.75 + offset_TCD                                       
        peak_width = 1.2    
        fit_info['TCD']['CO2']['start'] = peak_center-peak_width/2
        fit_info['TCD']['CO2']['end'] = peak_center+peak_width/2 

        # #propylene        
        # fit_info['TCD']['C3H6'] = {}   
        # peak_center = 23.25     + offset_FID                                          
        # peak_width = 2                                               
        # fit_info['TCD']['C3H6']['start'] = peak_center-peak_width/2                                         
        # fit_info['TCD']['C3H6']['end'] = peak_center+peak_width/2            
        
        fit_info['FID']['CH4'] = {}  
        peak_center = 7.55 + offset_FID                                       
        peak_width = 0.7                                              
        fit_info['FID']['CH4']['start'] = peak_center-peak_width/2                                        
        fit_info['FID']['CH4']['end'] = peak_center+peak_width/2                                       
        
        fit_info['FID']['CO'] = {}      
        peak_center = 9.1 + offset_FID
        peak_width = 1.2                                           
        fit_info['FID']['CO']['start'] = peak_center-peak_width/2                                        
        fit_info['FID']['CO']['end'] = peak_center+peak_width/2                                      
        
        #ethylene 
        fit_info['FID']['C2H4'] = {}  
        peak_center = 16.25          + offset_FID                               
        peak_width = 1#0.8                                           
        fit_info['FID']['C2H4']['start'] = peak_center-peak_width/2                                        
        fit_info['FID']['C2H4']['end'] = peak_center+peak_width/2                                          
        
        #ethane
        fit_info['FID']['C2H6'] = {} 
        peak_center = 17.7     + offset_FID                                     
        peak_width = 2#1.2                                                
        fit_info['FID']['C2H6']['start'] = peak_center-peak_width/2                                                  
        fit_info['FID']['C2H6']['end'] = peak_center+peak_width/2                                                    
    
        #propylene        
        fit_info['FID']['C3H6'] = {}   
        peak_center = 23.8     + offset_FID                                          
        peak_width = 1                                               
        fit_info['FID']['C3H6']['start'] = peak_center-peak_width/2                                         
        fit_info['FID']['C3H6']['end'] = peak_center+peak_width/2      
    
        #propane
        fit_info['FID']['C3H8'] = {} 
        peak_center = 24.5        + offset_FID                                          
        peak_width = 2                                                 
        fit_info['FID']['C3H8']['start'] = peak_center-peak_width/2                                         
        fit_info['FID']['C3H8']['end'] = peak_center+peak_width/2   
        
        save_as_pickle(pkl_data = fit_info, pkl_name = 'fit_info')       
        
        GC_exp = GC_EC_analyzer(filepath, 
                                fit_info, 
                                raw_to_analyse,
                                GC_plot_title,
                                iv_average = 180)    
        save_as_pickle(pkl_data = GC_exp, pkl_name = 'GC_exp')
        
        " Examples "
        # print(GC_exp.raw_time_stamp['TCD']['\\datb_tcd_021'])
        # print(GC_exp.raw_time_stamp['FID']['\\data_fid_021'])
        # print(GC_exp.raw_files)
        # print(GC_exp.raw_time_stamp['FID'].keys())
        #print(GC_exp.fitting_data['TCD']['\\datb_tcd_021'].keys())
          
else: 
    fit_info = get_saved_pickle(pkl_name = 'fit_info')
    GC_exp = get_saved_pickle(pkl_name = 'GC_exp')
        
if show_peak_plotting:
    GC_exp.show_peak_plotting(save_plot = save_plot)
    
if show_fitting:
    GC_exp.show_fitting(save_plot = False)
    
if show_fitting_all_figures:
    GC_exp.show_fitting_all_figures(save_plot = False)      

