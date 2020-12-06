#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on:                     Tue Mar 12 09:57:32 2019

@author:                        celiacailloux

Updated:                        Jun 23          2020

Experiment name:                20200616 Cu KHCO3 Stability

                                FOR PEIS SINGLE
"""

#from ECLabData import ECLabDataCV, ECLabDataCP
from ECLabImportCAData import ECLabDataCA
from ECLabImportZIRData import ECLabDataZIR
from ECLabImportCIData import ECLabDataCI

#import ECLabFunctions
import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
#from matplotlib.ticker import AutoMinorLocator, AutoLocator, MultipleLocator
from ECLabExperimentalPaths import exp_paths 

import PlottingFunctions as pltF
from PickleFunctions import save_as_pickle, get_saved_pickle
#from ExperimentsDetails import exps
                           
#_____________ Step 1: Choose Experiment_______________________________________

importECLabData = False
zero_time = True

plot_Rvstime = False
save_Rvstime_plot = True

plot_RvsI = True
save_RvsI_plot = True

exp_dir = r'O:\list-SurfCat\setups\307-059-largeCO2MEA\Data\Celia - EC largeCO2MEA data\EC-lab\20200507 Ag KHCO3 - Ar'

#_____________ Step 2: Import Data ____________________________________________

''' Use the different classes (CV, CP etc)'''
if importECLabData:
    
    """ import CIs """
    CI1 = ECLabDataCI(file_folder = exp_dir, 
                        pH = 6.8,
                        reference_electrode_potential = 'Ag/AgCl',
                        label = 'CO$_2$',
                        A_electrode = 1,                                             #cm2
                        uncompensated_R = 85,
                        )
    
    CIs = [CI1]

    
    """ write function that gets time_start by checking if the 0-index exists, 
    if not and an index-error occurs, the proceed to 1-index"""
    # if zero_time:
    #     for CI in CIs:
    #         time_start = CI_ex['time/timestamp'].iloc[0]
    #         CI.create_time_columns(time_start)
        
    save_as_pickle(pkl_data = CIs, pkl_name = 'CIs')

else:
    CIs = get_saved_pickle(pkl_name = 'CIs') 
    CI1 = CIs[0]
    
#_____________ Step 3: Import GC summary ____________________________________________

''' empty '''

#_____________ Step 4: Plotting ____________________________________________
 

''' Resistance over time '''    
if plot_Rvstime:
    
    fig, axs = plt.subplots(2,1, sharex = True,  gridspec_kw={'hspace': 0.1}) 
    fig.set_size_inches(w=11,h=6)
    color = pltF.color_maps('jkib')  
    title = CI1.exp_name
    comment = 'R_uncomp, Ohmic Drop'
    N = len(CI1.data)
    idx = 0
    
   
    for filename, CI_data in CI1.data.items():
        
        label = 'Change'
        col = color(idx/(N))#*1.2))

        R = CI_data['Rcmp/Ohm']
        t = CI_data['time/h']
        
        R_uncompensated = R.mean()
        if R_uncompensated == 0.00:
            print('NB! \nFor \'{}\' no resitance measured/detected (Ru = 0.00).'.format(filename))
        else:
            iR = abs(CI_data['I/mA'].divide(1000).mean()*R_uncompensated)    # ohmic drop = iR
            t_iR = t.iloc[0]
            
            axs[0].plot(t_iR, R_uncompensated, '-o', color = col, label = label, 
                       alpha = 1, 
                       linewidth = 2, 
                       markerfacecolor='white', 
                       markeredgewidth = 2)
            axs[1].plot(t_iR, iR, '-o',color = col,  label = label, alpha = 1, 
                       linewidth = 2, 
                       markerfacecolor='white', 
                       markeredgewidth = 2)    
            idx += 1
    R_nom = 56.2    
    axs[0].axhline(y = R_nom, linewidth=2, color='k', alpha = 0.5, linestyle = '--')
    
    for ax in axs:
        ax.set_xlim(left = 0)
        pltF.global_minor_locator(ax, x_locator = 6, y_locator = 5)
        pltF.global_mayor_xlocator(ax, x_locator = 1) 
        pltF.global_settings(ax)
    # pltF.global_legendbox(ax[1])

    axs[0].set_ylim(bottom = 40, top = 80)
    axs[1].set_ylim(bottom = 0)
    pltF.global_mayor_ylocator(axs[1], y_locator = 0.2)         
    pltF.CA_global(axs[0], ylabel = R.name, xlabel = None, legend = False)
    pltF.CA_global(axs[1], ylabel = 'V', xlabel = t.name, legend = False)
    
    if save_Rvstime_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)
        
''' Resistance vs current '''    
if plot_RvsI:
    
    fig, axs = plt.subplots(2,1, sharex = True,  gridspec_kw={'hspace': 0.1}) 
    fig.set_size_inches(w=11,h=6)
    color = pltF.color_maps('jkib')  
    title = CI1.exp_name
    comment = 'R_uncomp vs. I'
    N = len(CI1.data)
    idx = 0
    jR = {}
    j_old = 0    
   
    for filename, CI_data in CI1.data.items():
        
        label = 'Change'
        col = color(idx/(N))#*1.2))

        R = CI_data['Rcmp/Ohm'].iloc[-1]
        j = CI_data['control/mA'].iloc[0]/CI1.A_electrode
        
        if j_old != j:
            R_list = []
            R_list.append(R)
        else:
            R_list.append(R)
        jR[j] = [R_list, col]
                  
        axs[0].plot(j, R, '-o', color = col, label = label, 
                   alpha = 1, 
                   linewidth = 2, 
                   markerfacecolor='white', 
                   markeredgewidth = 2)  
        idx += 1
        j_old = j
    
    
    # print(jR)
    
    for _j, Rcol in jR.items():        
        axs[1].plot(_j, np.mean(Rcol[0]), '-o', color = Rcol[1],  label = label, alpha = 1, 
                linewidth = 2, 
                markerfacecolor='white', 
                markeredgewidth = 2)  
        
        axs[1].errorbar(_j,np.mean(Rcol[0]), yerr=np.std(Rcol[0]), color = Rcol[1],fmt='o', 
                        capsize=5, elinewidth=2, mec = Rcol[1], markeredgewidth=2, markerfacecolor='white')
        
    
    R_nom = 56.2    
    for ax in axs:
        ax.axhline(y = R_nom, linewidth=2, color='k', alpha = 0.5, linestyle = '--')
        ax.set_ylim(bottom = 40, top = 80)
        pltF.global_mayor_xlocator(ax, x_locator = 2) 
        pltF.global_mayor_ylocator(ax, y_locator = 10)        
        pltF.global_minor_locator(ax, x_locator = 2, y_locator = 5)
        pltF.global_settings(ax)
        
    pltF.CA_global(axs[0], ylabel = CI_data['Rcmp/Ohm'].name, xlabel = None, legend = False)
    pltF.CA_global(axs[1], ylabel = CI_data['Rcmp/Ohm'].name, xlabel = 'I/mAcm-2', legend = False)
    # ax.set_xlim(left = 0)      
    # pltF.global_legendbox(ax[1])
    # axs[1].set_ylim(bottom = 0)
    
    
    
    if save_RvsI_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)        

