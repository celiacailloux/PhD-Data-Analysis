#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on:                     Mar 12 2020

@author:                        celiacailloux

Updated:                        Jun 19 2020

Experiment name:                XX

                                SINGLE CA and GC summary report
"""

#from ECLabData import ECLabDataCV, ECLabDataCP
from ECLabImportCAData import ECLabDataCA
from ECLabImportZIRData import ECLabDataZIR
from GCPerkinElmerSummaryReport import GCPESummaryData
#import ECLabFunctions

import matplotlib.pyplot as plt
import numpy as np

#from matplotlib.ticker import AutoMinorLocator, AutoLocator, MultipleLocator
from ECLabExperimentalPaths import exp_paths 

import PlottingFunctions as pltF
from PickleFunctions import save_as_pickle, get_saved_pickle
#from ExperimentsDetails import exps

import pandas as pd
pd.set_option('display.max_rows', 80)
                           
                           
#_____________ Step 1: Choose Experiment_______________________________________
''' 
* make pkl so that you don't have to ... every time '''

importECLabData = False
importGCSummaryReport = True

plot_IVvstime = False
save_Ivvstime_plot = False

plot_jvstimestamp = False
save_plot_jvstimestamp = False

plot_FE = True
save_FE_plot = True

exp_dir = r'O:\list-SurfCat\setups\307-059-largeCO2MEA\Data\Celia - EC largeCO2MEA data\EC-lab\20200602 Cu KHCO3 Stability'
GC_dir = r'O:\list-SurfCat\setups\307-059-largeCO2MEA\Data\Celia - EC largeCO2MEA data\GC - Perkin Elmer\20200602 Cu KHCO3 Stability'


#_____________ Step 2: Import Data ____________________________________________
''' Use the different classes (CV, CP etc)'''
if importECLabData:

    """ import CAs """
    CA1 = ECLabDataCA(file_folder = exp_dir, 
                       pH = 6.8,
                       reference_electrode_potential = 'Ag/AgCl',
                       label = 'CO$_2$',
                       A_electrode = 1,                                             #cm2
                       uncompensated_R = 85,
                       )
    
    # print(list(CA1.CA_data.keys()))
    # file_CA1_time_start = list(CA1.CA_data.keys())[0]
    # CA_ex = CA1.CA_data[file_CA1_time_start]
    
    CAs = [CA1]
    
    save_as_pickle(pkl_data = CAs, pkl_name = 'CAs')
else:
    CAs = get_saved_pickle(pkl_name = 'CAs')
    
    CA1 = CAs[0]    

#_____________ Step 3: Import GC summary ____________________________________________

''' GC summary class '''
if importGCSummaryReport:
    GC1 = GCPESummaryData(file_folder = GC_dir)
    
    
    # print(test['datetime'])
    # print(test['timestamp'])
    #GC1.create_time_columns(time_start)
    
    GCs = [GC1]
    
    save_as_pickle(pkl_data = GCs, pkl_name = 'GCs')
else:
    GCs = get_saved_pickle(pkl_name = 'GCs')
    
    GC1 = GCs[0]   
    

#_____________ Step 4: Plotting ____________________________________________
if plot_IVvstime:
    fig, axs = plt.subplots(3,1, sharex = True,  gridspec_kw={'hspace': 0.1})  
    fig.set_size_inches(w=11,h=9)
    color = pltF.color_maps('jkib')   
    title = CA1.exp_name
    comment =  'j, VvsRHE, VvsAgAgCl, GC injection'
    N = len(CA1.CA_data)
    idx = 0
    
    j = []
    GC = GCs[len(CAs)-1]
    injection_time = GC1.data[list(GC1.data.keys())[0]]['Time of Injection'].astype(str)
    # injection_time = GCs[N-1]['Time of Injection'].astype(str)
    injection_time = [x[:-1] for x in injection_time]
    # print(list(injection_time))
    
    for filename, CA_data in CA1.CA_data.items():
        
        label = 'Change'
        col = color(idx/(N*1.2))

        VvsRHE = CA_data['Ewe/RHE']
        VvsREF = CA_data['Ewe/V']
        j = CA_data['I/mAcm-2']
        t = CA_data['time/h']

        
        time = CA_data['time/datetime'].dt.time.astype(str)
        # print('test time {}'.format(time[1][:5]))
        # _time = time[1][:5]
        
        
        # print(injection_time[0][:5])
        
        #for injection in injection_time:
        _bool = CA_data['time/datetime'].dt.time.astype(str).str.contains('|'.join(injection_time))
        t_datetime = CA_data['time/h'][_bool]
        VvsSHE_injection = CA_data['Ewe/V'][_bool]
        j_injection = CA_data['I/mAcm-2'][_bool]
                       
     
        axs[0].plot(t, j, color = col, label = label, alpha = 1, linewidth = 2)       
        axs[0].plot(t_datetime, j_injection, 'o', color = 'k',#"col, 
                    label = label, 
                    markersize = 4,
                    markerfacecolor='white',
                    markeredgewidth = 1)
        axs[1].plot(t, VvsRHE, color = col, label = label, alpha = 1, linewidth = 2)       
        axs[2].plot(t, VvsREF, color = col, label = label, alpha = 1, linewidth = 2)  

        axs[2].plot(t_datetime, VvsSHE_injection, 'o', color = 'k',#col, 
                    label = label, 
                    markersize = 4,
                    markerfacecolor='white',
                    markeredgewidth = 1)
        idx += 1
    # print('j is {}'.format(j))
    # pltF.global_legendbox(axs[0])

    for ax in axs:
        #ax.set_ylim(-2,0)   
        ax.set_xlim(left = 0)             
        pltF.global_mayor_xlocator(ax, x_locator = 2)
        pltF.global_settings(ax)
    pltF.global_mayor_ylocator(axs[0], y_locator = 5)        
    pltF.global_mayor_ylocator(axs[1], y_locator = 0.5) 
    pltF.global_minor_locator(axs[0], x_locator = 1, y_locator = 5)                
    pltF.global_minor_locator(axs[1], x_locator = 1, y_locator = 5)  
    pltF.CA_global(axs[0], ylabel = j.name, xlabel = None, legend = False)
    pltF.CA_global(axs[1], ylabel = VvsRHE.name, xlabel = None, legend = False)
    pltF.CA_global(axs[2], ylabel = VvsREF.name, xlabel = t.name, legend = False)
    pltF.global_settings(axs[0])
    pltF.global_settings(axs[1])
    pltF.global_settings(axs[2])
    
    if save_Ivvstime_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)
    else:
        plt.show()
' __________________________________________________ Plot j vs Time (Step 4) '        
if plot_IVvstime:
    fig, axs = plt.subplots(3,1, sharex = True,  gridspec_kw={'hspace': 0.1})  
    fig.set_size_inches(w=11,h=9)
    color = pltF.color_maps('jkib')   
    title = CA1.exp_name
    comment =  'j, VvsRHE, VvsAgAgCl, GC injection'
    N = len(CA1.CA_data)
    idx = 0
    
    j = []
    # GC = GCs[len(CAs)-1]
    injection_time = GC1.data[list(GC1.data.keys())[0]]['Time of Injection'].astype(str)
    # injection_time = GCs[N-1]['Time of Injection'].astype(str)
    injection_time = [x[:-1] for x in injection_time]
    # print(list(injection_time))
    
    for filename, CA_data in CA1.CA_data.items():
        
        label = 'Change'
        col = color(idx/(N*1.2))
        VvsRHE = CA_data['Ewe/RHE']
        VvsREF = CA_data['Ewe/V']
        j = CA_data['I/mAcm-2']
        t = CA_data['time/h']

        
        time = CA_data['time/datetime'].dt.time.astype(str)
        # print('test time {}'.format(time[1][:5]))
        # _time = time[1][:5]
        
        
        # print(injection_time[0][:5])
        
        #for injection in injection_time:
        _bool = CA_data['time/datetime'].dt.time.astype(str).str.contains('|'.join(injection_time))
        t_datetime = CA_data['time/h'][_bool]
        VvsSHE_injection = CA_data['Ewe/V'][_bool]
        j_injection = CA_data['I/mAcm-2'][_bool]
        
        ''' write some code that checks weather the first injection
        is injected before EC-start '''
                       
     
        axs[0].plot(t, j, color = col, label = label, alpha = 1, linewidth = 2)       
        axs[0].plot(t_datetime, j_injection, 'o', color = 'k',#"col, 
                    label = label, 
                    markersize = 4,
                    markerfacecolor='white',
                    markeredgewidth = 1)
        axs[1].plot(t, VvsRHE, color = col, label = label, alpha = 1, linewidth = 2)       
        axs[2].plot(t, VvsREF, color = col, label = label, alpha = 1, linewidth = 2)  
        
        # NB! Color-coding depends on when the first injection was made.
        # Typically and injection is done BEFORE any ELECTROCHEMISTRY has 
        # been initiated.
        
        axs[2].plot(t_datetime, VvsSHE_injection, 'o', color = 'k',#col, 
                    label = label, 
                    markersize = 4,
                    markerfacecolor='white',
                    markeredgewidth = 1)
        idx += 1
    # print('j is {}'.format(j))
    # pltF.global_legendbox(axs[0])

    for ax in axs:
        #ax.set_ylim(-2,0)   
        ax.set_xlim(left = 0)             
        pltF.global_mayor_xlocator(ax, x_locator = 2)
        pltF.global_settings(ax)
    pltF.global_mayor_ylocator(axs[0], y_locator = 5)        
    pltF.global_mayor_ylocator(axs[1], y_locator = 0.5) 
    pltF.global_minor_locator(axs[0], x_locator = 1, y_locator = 5)                
    pltF.global_minor_locator(axs[1], x_locator = 1, y_locator = 5)  
    pltF.CA_global(axs[0], ylabel = j.name, xlabel = None, legend = False)
    pltF.CA_global(axs[1], ylabel = VvsRHE.name, xlabel = None, legend = False)
    pltF.CA_global(axs[2], ylabel = VvsREF.name, xlabel = t.name, legend = False)
    pltF.global_settings(axs[0])
    pltF.global_settings(axs[1])
    pltF.global_settings(axs[2])
    
    print('Printing \'{}\' but remember that there most likely will have', \
          'occured a GC injection prior to the experiment!')
    
    if save_Ivvstime_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)
    else:
        plt.show()
' _____________________________________________ Plot j vs timestamp (Step 5) '
if plot_jvstimestamp:
    
    fig, axs = plt.subplots(1,1)
    fig.set_size_inches(w=11,h=3)
    color = pltF.color_maps('jkib')   
    title = CA1.exp_name
    comment =  'j, VvsRHE, VvsAgAgCl, GC injection, timestamp'
    N = len(CA1.CA_data)
    idx = 0
    
    
    GC = GCs[len(CAs)-1]
    injection_time = GC1.data[list(GC1.data.keys())[0]]['Time of Injection'].astype(str)
    # removes the last digit in timestamp (eg. 06:52:15 > 06:52:1)
    injection_time = [x[:-1] for x in injection_time]
    
    
    for filename, CA_data in CA1.CA_data.items():
        
        label = 'Change'
        col = color(idx/(N*1.2))

        j = CA_data['I/mAcm-2']
        t = CA_data['time/datetime']
        
        # find all j that have the same timestamp as GC
        _bool = CA_data['time/datetime'].dt.time.astype(str).str.contains('|'.join(injection_time))
        t_datetime = CA_data['time/datetime'][_bool]
        j_injection = CA_data['I/mAcm-2'][_bool]
        
        if idx == 0:
            j_accum = j_injection
            t_accum = t_datetime
            # print(j_injection)
            # print(j_accum)
        else:
            j_accum = j_accum.append(j_injection, ignore_index=True)
            t_accum = t_accum.append(t_datetime, ignore_index=True)
            # print(j_injection)
                       
     
        axs.plot(t.dt.strftime('%H:%M'), j, color = col, label = label, alpha = 1, linewidth = 2)             
        idx += 1
    
    axs.plot(t_accum.dt.strftime('%H:%M'), j_accum, 'o', color = 'k',
                label = label, 
                markersize = 4,
                markerfacecolor='white',
                markeredgewidth = 1)
    plt.xticks(rotation=45, ha = 'right')
    pltF.global_mayor_xlocator(axs, x_locator = 60)
    # print('GC plot N: {}, GC total N {}'.format(len(t_accum), len(injection_time)))
    pltF.global_settings(axs)
    
    if save_plot_jvstimestamp:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)
    else:
        plt.show()        
    
if plot_FE:    
    '''
    This code is definitely not ideal BUT for the moment is serves
    the purpose. However, the average currents might not be the exact averages
    '''
    
    GC_file_name = list(GC1.data.keys())[0]
    GC_summary_data = GC1.data[GC_file_name]
    injection_time = GC1.data[GC_file_name]['Time of Injection'].astype(str)
    # removes the last digit in timestamp (eg. 06:52:15 > 06:52:1)
    injection_time = [x[:-1] for x in injection_time]
    calibration_CO2R = GC1.calibration_CO2R
    
    flow = 5 #sccm
    molar_volume = 22.4 #
    molar_flow = flow * 1/molar_volume*1e-3/60
    F = 96485.33212 #C/
    
    j_test = 5e-3 #mA to A
    
    j_avg = {}
    j_avg_df = GC1.j_avg
    
    ' find average current between two injections '
    for filename, CA_data in CA1.CA_data.items():
        N_Ns = CA_data['Ns'].unique() # gets number of loops in this CA file (np array)
        j_avg[filename] = {}
        
        'iterate over number of loops in CA file'        
        for Ns in N_Ns:   
            # print(CA_data.loc[CA_data['Ns'] == Ns]['Ns'])
            CA_data_Ns = CA_data.loc[CA_data['Ns'] == Ns]
            
            j = CA_data_Ns['I/mAcm-2']
            V = CA_data_Ns['Ewe/V']
            t = CA_data_Ns['time/datetime']
            
            j_avg[filename][Ns] = [j.mean(), j.std()]
            # j_avg_df['File name'] = filename
            # j_avg_df['Ns'] = Ns
            # j_avg_df['j avg'] = j.mean()
            # j_avg_df['j std'] = j.std()

            j_avg_df = j_avg_df.append({'File Name':filename, 
                                        'Ns': Ns,
                                        'j avg': j.mean(), 
                                        'j std': j.std(),
                                        'V avg': V.mean()},
                                        ignore_index = True)
    ''' Be careful using the next lines '''
    j_avg_df = j_avg_df.drop(j_avg_df.index[0]).reset_index()
    j_avg_df = j_avg_df.drop(j_avg_df.index[-1])
    
    FE_calculator = {}    
    for detector, gases in calibration_CO2R.items():
        for gas, gas_items in gases.items():
            FE_calculator[detector + '-' + gas] = \
                gas_items['z']*F/gas_items['slope']*molar_flow
                
    peak_areas = GC1.peaks_areas
    
    '''
    Note that number of injections (N_GC) should be larger than the number
    of CAs (N_CA). Hence the first GC measurement is a background measurement,
    and thus SHOULD NOT BE used for FE calculations. N_GC > N_CA
    '''
    N_GC = peak_areas[GC_file_name].shape[0]
    N_CA = j_avg_df.shape[0]
    if N_CA >= N_GC:
        print('\nNB!')
        print('Something is wrong with the number of GCs vs.', \
              'the number of average currents/CAs. Check it!')
        print(j_avg_df[['j avg', 'V avg']])
    else:
                    
        for detector_gas, z_F_inv_slope_mflow in FE_calculator.items():
            temp = peak_areas[GC_file_name][detector_gas].mul(z_F_inv_slope_mflow)
            FE = temp.div(j_avg_df['j avg'].mul(1e-3).abs())
            peak_areas[GC_file_name][detector_gas + ' FE'] = FE
                
        # for col in list(peak_areas[GC_file_name].columns):
        #     if 'FE' in col:
        #         # print(col)
        #         FE = peak_areas[GC_file_name][col]
        #         print('gas: {} \FE: {}'.format( col, FE)                    )
        FE_sum_df = peak_areas[GC_file_name].filter(regex='FE')
        ax = FE_sum_df.plot.bar(rot=0, stacked = True, figsize=(11,3))
        
        peak_areas[GC_file_name]['FE sum'] = FE_sum_df.sum(axis=1)
        
        # labels = peak_areas[GC_file_name].index.values.tolist()
        # fig, ax = plt.subplots()

        # margin_bottom = np.zeros(FE_sum_df.iloc[0])
        # for col_name, col_data in FE_sum_df.iteritems():

        #     ax.bar(labels, col_data, width = 0.35, bottom = margin_bottom)
        #     margin_bottom += col_data
    
    title = CA1.exp_name
    comment =  'FE plot'     
    # FE_sum_df.plot(figsize=(11,3));
    if save_FE_plot:
        ax.figure.savefig('Figures/'+ title + comment +'.png')
    else:
        plt.show()            


    # if 
    #     print('Printing plot')