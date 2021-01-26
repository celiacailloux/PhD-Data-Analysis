# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 17:17:54 2018

@author: patri
"""
from faraday_efficiency_uncertainty import FE_calculator
import numpy as np
#plot package
import matplotlib.pyplot as plt
import matplotlib as mpl
#import fit_info
from pylab import rcParams
rcParams['figure.figsize'] = 6, 6
#fonts for matplotlib
font = {#'family' : 'Palatino Linotype',
        'size'   : 14}
mpl.rc('font', **font)


# first sterlitech 1.2 mum
# Set the start and end times for the peaks. 
detector = 'TCD'
fit_info = {}
fit_info['settings'] = {}
fit_info['settings']['background_range'] = 0.05 #minutes, used for integration
fit_info[detector] = {}

fit_info[detector]['H2'] = {} #P is for peak in spectrum, and are ordered from low to high in retentiontime
fit_info[detector]['H2']['start'] = 2.60 #GL note: Original setting 3.5 (at 30 degrees)
fit_info[detector]['H2']['end'] = 3.70 #GL note: Original setting 8 (at 30 degrees)

fit_info[detector]['CO'] = {} #P is for peak in spectrum, and are ordered from low to high in retentiontime
fit_info[detector]['CO']['start'] = 14.25 #GL note: Original setting 16.3 (at 30 degrees)
fit_info[detector]['CO']['end'] = 15.20 #GL note: Original setting 17.3 (at 30 degrees)

fit_info[detector]['CO2'] = {} #P is for peak in spectrum, and are ordered from low to high in retentiontime
fit_info[detector]['CO2']['start'] = 24.60 #GL note: Original setting 28 (at 30 degrees)
fit_info[detector]['CO2']['end'] = 35 #GL note: Original setting 38 (at 30 degrees)


# Specify the folder for GC-data and the measurement id for iv data
#filepath = r'O:\FYSIK\list-SurfCat\setups\307-059-largeCO2MEA\Data\Jens_Patrick\16042018'
#measurement_id = 129

filepath = r'O:\FYSIK\list-SurfCat\setups\307-059-largeCO2MEA\Data\Gaston\GL18012'
measurement_id = 400
mass_st12 = 28.4 #mg/cm2
ECSA_st12 = 15.07 #ECSA/Geometric


#raw_to_analyse = slice(4,13)
raw_to_analyse = slice(4,10)
time_correction = 0 #Originally 0

# make the faraday calculator
sterl12 = FE_calculator(fit_info,180)
sterl12.plot_iv_correction(filepath,measurement_id,'Sterlitech 1.20 $\mu$m with Ag NPs',time_correction,raw_to_analyse)
sterl12.raw_visualization(filepath,raw_to_analyse)
sterl12.plot_FE_V_to_current(filepath,measurement_id,'Sterlitech 1.20 $\mu$m with Ag NPs',time_correction,raw_to_analyse)


faraday_eff_CO_st, current_CO_st, faraday_eff_H2_st,current_H2_st,gc_current_st,gc_voltage_st, cathode_size_st, gc_measurement_time_st,_,_=\
sterl12.FE_calculation(filepath,measurement_id, time_correction, raw_to_analyse)
