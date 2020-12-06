# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 17:17:54 2018

@author: patri

Edited and customized to Celia

To access surfcatdata.dk VNP is required. 

"""
from faraday_efficiency_uncertainty import FE_calculator
import numpy as np
#plot package
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

plt.close('all')

"""
Object initilization of GC experiment (FE calculator). Requires (VPN) access 
to the Surfcat Database if wanting to plot EC data. 

Creates a fit_info and FE_calculator and assigns important measurement 
parameters, and the file_path to the GC files.
""" 
assign_important_parameters     = True
object_initialization           = True                        

"""
FE calculator plotting. All plotting functions can be found in 'FE calculator'.
"""

plot_raw_visualization              = False
plot_FE_V_to_current                = False
plot_FE_n_to_time_voltage           = False
plot_FE_to_current                  = False
plot_FE_to_voltage                  = False
plot_iv_correction                  = False
show_fitting                        = False
show_fitting_all_figures            = False

"""
Calculation
"""
FE_calculation                      = True

if assign_important_parameters:
    """
    Specify
        * the filepath
        * a title to the plots
    """
    
    #filepath = r'O:\FYSIK\list-SurfCat\setups\307-059-largeCO2MEA\Data\Jens_Patrick\28052018'
    #measurement_id = 224
    #filepath = join_paths(get_application_data_location('OneDrive'),r'PhD/Data/GC testdata/GL18012')
    filepath = r'O:\list-SurfCat\setups\307-059-largeCO2MEA\Data\Gaston\GL18012'
    GC_plot_title = None#'Sterlitech 1.20 $\mu$m with Ag NPs'
    
    """
    Assign important variables/parameters for analysis and plotting functions 
    in the FE_calculator object
    
    Specify 
        * the i,v measurement id (can be found in the cinfdata database (?)) 
        * the catalyst mass loading (mg/cm2) (?)
        * the measured ECSA (ECSA/geometric)
    Optional
        * the number of raw files to analyse (raw_to_analyse / a slice object)
        * the time correction (s or min?)
    """    
    measurement_id = 400
    mass = 1                #mg/cm2
    ECSA = 1                #ECSA/Geometric

    raw_to_analyse = slice(6,10)#slice(4,14)                                    
    time_correction = 0     

if object_initialization:
    
    """ 
    fit_info is a dictionary that contains relevant information about the GC
    measurement and which affects fitting of the peaks.
    Necessary information
        * (fill out!)
        * 'detector' (FID or TCD)
            * Set the start and end times for the peaks (these are know calibration)
    Optional information is:
        * (fill out!)
        * 'settings'
            * 'background_range'
    """
    detector = 'TCD'
    fit_info = {}
    
    fit_info['settings'] = {}
    fit_info['settings']['background_range'] = 0.05 #minutes, used for integration
    
    fit_info[detector] = {}
   
    fit_info[detector]['H2'] = {}                                               #P is for peak in spectrum, and are ordered from low to high in retentiontime
    fit_info[detector]['H2']['start'] = 2                                    #GL note: Original setting 3.5 (at 30 degrees)
    fit_info[detector]['H2']['end'] = 4.5                                      #GL note: Original setting 8 (at 30 degrees)
    
    fit_info[detector]['CO'] = {}                                               #P is for peak in spectrum, and are ordered from low to high in retentiontime
    fit_info[detector]['CO']['start'] = 14                                  #GL note: Original setting 16.3 (at 30 degrees)
    fit_info[detector]['CO']['end'] = 15.20                                     #GL note: Original setting 17.3 (at 30 degrees)
    
    fit_info[detector]['CO2'] = {}                                              #P is for peak in spectrum, and are ordered from low to high in retentiontime
    fit_info[detector]['CO2']['start'] = 23                                  #GL note: Original setting 28 (at 30 degrees)
    fit_info[detector]['CO2']['end'] = 29.5                                       #GL note: Original setting 38 (at 30 degrees)
    
    save_as_pickle(pkl_data = fit_info, pkl_name = 'fit_info')       
    
    """
    Creates a faraday calculator (FE calculator). The FE calculator is an
    object that is capable of analyzing and plotting GC and EC data
    
    Specify 
        * the path to the folder containing the GC-data
        * the number of datapoints to average over in the current, voltage (iv_average)
    Optional
        * bump = None, 
        * peak_rise = None)        
    """
    GC_exp = FE_calculator(fit_info, iv_average = 180)    
    save_as_pickle(pkl_data = GC_exp, pkl_name = 'GC_exp')

      
else: 
    fit_info = get_saved_pickle(pkl_name = 'fit_info')
    GC_exp = get_saved_pickle(pkl_name = 'GC_exp')
    
      
    
if plot_raw_visualization:
    GC_exp.raw_visualization(filepath,
                              raw_to_analyse)
    
if plot_FE_V_to_current:
    GC_exp.plot_FE_V_to_current(filename = filepath,
                                 measurement_id = measurement_id,
                                 plot_title = GC_plot_title,
                                 time_correction = time_correction,
                                 raw_to_analyse = raw_to_analyse)
if plot_FE_n_to_time_voltage:
   print('fill out')
    
    
if plot_iv_correction:
    GC_exp.plot_iv_correction(filename = filepath,
                               measurement_id = measurement_id,
                               plot_title = GC_plot_title,
                               time_correction = time_correction,
                               raw_to_analyse = raw_to_analyse)
    
if FE_calculation:
    faraday_eff_CO_st, current_CO_st, faraday_eff_H2_st,current_H2_st, gc_current_st,gc_voltage_st, cathode_size_st, gc_measurement_time_st,_,_=\
    GC_exp.FE_calculation(filename = filepath,
                           measurement_id = measurement_id, 
                           time_correction = time_correction, 
                           raw_to_analyse = raw_to_analyse)
    
if show_fitting:
    GC_exp.show_fitting(filepath = filepath,
                        raw_to_analyse = raw_to_analyse)
    
if show_fitting_all_figures:
    GC_exp.show_fitting_all_figures(filepath = filepath,
                        raw_to_analyse = raw_to_analyse)