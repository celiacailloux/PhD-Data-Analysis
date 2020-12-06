#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on:                     Tue Mar 12

@author:                        celiacailloux

Updated:                        15 of June 2020

Experiment name:                

                                FOR CA COMPARISON ANALYSIS
"""

#from ECLabData import ECLabDataCV, ECLabDataCP
from ECLabImportCAData import ECLabDataCA
from ECLabImportZIRData import ECLabDataZIR
from GCPerkinElmerSummaryReport import GCPESummaryData
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

plot_IVvstime_comparison = False
save_Ivvstime_comparison_plot = True

plot_Rvstime_comparison = True
save_Rvstime_comparison_plot = True

plot_RvsVvsRHE_comparison = False
save_RvsVvsRHE_comparison_plot = True


exp_dir = r'O:\list-SurfCat\setups\307-059-largeCO2MEA\Data\Celia - EC largeCO2MEA data\EC-lab\20200520 Ag KHCO3 Stability - f 20kHz'
exp2_dir = r'O:\list-SurfCat\setups\307-059-largeCO2MEA\Data\Celia - EC largeCO2MEA data\EC-lab\20200526 Ag KHCO3 Stability'

plt_title_extension = 'comparison of Stability 200200520 and 200200526'
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
    file_CA1_time_start = list(CA1.CA_data.keys())[0]
    CA_ex = CA1.CA_data[file_CA1_time_start]
    
    CA2 = ECLabDataCA(file_folder = exp2_dir, 
                       pH = 6.8,
                       reference_electrode_potential = 'Ag/AgCl',
                       label = 'CO$_2$',
                       A_electrode = 1,                                             #cm2
                       uncompensated_R = 85,
                       )
    
    # print(list(CA2.CA_data.keys()))
    file_CA2_time_start = list(CA2.CA_data.keys())[0]
    CA2_ex = CA2.CA_data[file_CA2_time_start]
    
    CAs = [CA1, CA2]
  
    save_as_pickle(pkl_data = CAs, pkl_name = 'CAs')
    
else:
    CAs = get_saved_pickle(pkl_name = 'CAs')
    
    CA1 = CAs[0]
    CA2 = CAs[1] 

#_____________ Step 4: COMPARISON ____________________________________________

    ''' Comparing two experiments - Ivstime '''

if plot_IVvstime_comparison:
    fig, axs = plt.subplots(3,1, sharex = True,  gridspec_kw={'hspace': 0.1}) 
    fig.set_size_inches(w=11,h=9)
    # color = plt.get_cmap('tab20c')  
    color = pltF.color_maps('jkib')  
    title = 'IvsTime - ' + plt_title_extension
    comment = 'j, VvsRHE, VvsAgAgCl'
    N = len(CAs)
    idx = 0
    
    
    for idx_CA, CA in enumerate(CAs):
        col = color(idx/(N))
        
        for filename, CA_data in CA.CA_data.items():
                
            label = 'Change'    
            VvsRHE = CA_data['Ewe/RHE']
            VvsREF = CA_data['Ewe/V']
            j = CA_data['I/mAcm-2']
            if idx_CA == 1:
                t = CA_data['time/h'].add(10/60)    
            else:
                t = CA_data['time/h']
            
            axs[0].plot(t, j, color = col, label = label, alpha = 1, linewidth = 2)       
            axs[1].plot(t, VvsRHE, color = col, label = label, alpha = 1, linewidth = 2)       
            axs[2].plot(t, VvsREF, color = col, label = label, alpha = 1, linewidth = 2)      
        
        idx += 1

    for ax in axs:
        ax.set_xlim(left = 0)
        #ax.set_ylim(-2,0)
                        
        pltF.global_mayor_xlocator(ax, x_locator = 1)
        pltF.global_settings(ax)
    pltF.global_minor_locator(axs[0], x_locator = 2, y_locator = 5)
    pltF.global_minor_locator(axs[1], x_locator = 2, y_locator = 2)
    pltF.global_mayor_ylocator(axs[0], y_locator = 1)
    pltF.global_mayor_ylocator(axs[1], y_locator = 0.2)
    pltF.global_mayor_ylocator(axs[2], y_locator = 0.2)      
    pltF.CA_global(axs[0], ylabel = j.name, xlabel = None, legend = False)
    pltF.CA_global(axs[1], ylabel = VvsRHE.name, xlabel = None, legend = False)
    pltF.CA_global(axs[2], ylabel = VvsREF.name, xlabel = t.name, legend = False)
    plt.show()
    
    if save_Ivvstime_comparison_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment) 
            

''' Comparing two experiments - Rvstime '''
if plot_Rvstime_comparison:
    fig, axs = plt.subplots(2,1, sharex = True,  gridspec_kw={'hspace': 0.1}) 
    fig.set_size_inches(w=11,h=6)
    # color = plt.get_cmap('tab20c')  
    color = pltF.color_maps('jkib')  
    title = 'RvsTime - '+ plt_title_extension
    comment = 'R_uncomp, Ohmic Drop'
    N = len(CAs)
    idx = 0
    
    
    for idx_CA, CA in enumerate(CAs):
        col = color(idx/(N))#*1.5))
        
        for filename, CA_data in CA.CA_data.items():
            label = 'Change'  
            if 'CA loop' in CA_data: 
                df_idx_new_loop_start = CA_data.loc[CA_data['Ru difference/bool']]
                idx_list = list(df_idx_new_loop_start.index.values)

                Ru = CA_data['Ru/Ohm'][idx_list]
                iR = CA_data['iR/V'][idx_list]
                t = CA_data['time/h'][idx_list]
            else:
                label = 'Change'    
                Ru = CA_data['Ru/Ohm'].mean()
                iR = CA_data['iR/V'].mean()
                t = CA_data['time/h'].iloc[0]
                # Ru = R.mean()
                # iR = 
            # if Ru == 0.00:
            #     print('NB! \nFor \'{}\' no resitance measured/detected (Ru = 0.00).'.format(filename))
            # else:
            #     iR = abs(CA_data['I/mA'].divide(1000).mean()*R_uncompensated)    # ohmic drop = iR
                # t_iR = t.iloc[0]
                
            axs[0].plot(t, Ru, 'o', color = col,  label = label, alpha = 1, 
                       linewidth = 2, 
                       markerfacecolor='white', 
                       markeredgewidth = 2)
            axs[1].plot(t, abs(iR), 'o', color = col,  label = label, alpha = 1, 
                       linewidth = 2, 
                       markerfacecolor='white', 
                       markeredgewidth = 2)    
        idx += 1
                
    R_nom = 56.2    
    axs[0].axhline(y = R_nom, linewidth=2, color='k', alpha = 0.5, linestyle = '--')
    
    for ax in axs:
        ax.set_xlim(left = 0)
        pltF.global_minor_locator(ax, x_locator = 2, y_locator = 5)
        pltF.global_mayor_xlocator(ax, x_locator = 1) 
        pltF.global_settings(ax)
    # pltF.global_legendbox(ax[1])

    axs[0].set_ylim(bottom = 40, top = 80)
    # axs[1].set_ylim(bottom = 0, top = 1)
    pltF.global_mayor_ylocator(axs[1], y_locator = 0.1)         
    pltF.CA_global(axs[0], ylabel = CA_data['Ru/Ohm'].name, xlabel = None, legend = False)
    pltF.CA_global(axs[1], ylabel = 'V', xlabel = CA_data['time/h'].name, legend = False)
    
    if save_Rvstime_comparison_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)               
        
''' Compring two experiments - RvsVvsRHE '''
if plot_RvsVvsRHE_comparison:
    fig, axs = plt.subplots(2,1, sharex = True,  gridspec_kw={'hspace': 0.1}) 
    fig.set_size_inches(w=3,h=6)
    # color = plt.get_cmap('tab20c')  
    color = pltF.color_maps('jkib')  
    title = 'RvsVvsRHE - ' + plt_title_extension
    comment = 'R_uncomp, Ohmic Drop'
    N = len(CAs)
    idx = 0
    
    ViRRu = {'iR': [], 'V': [], 'Ru':[], 'color': []}

    
    for idx_CA, CA in enumerate(CAs):
        col = color(idx/(N))#*1.5))
        
        iR_list = []
        V_list = []
        Ru_list = []
        
        for filename, CA_data in CA.CA_data.items():
                
            label = 'Change'    
            R = CA_data['Ru/Ohm']
            V = CA_data['Ewe/RHE']
            
            
            R_uncompensated = R.mean()
            if R_uncompensated == 0.00:
                print('NB! \nFor \'{}\' no resitance measured/detected (Ru = 0.00).'.format(filename))
            else:
                iR = abs(CA_data['I/mA'].divide(1000).mean()*R_uncompensated)    # ohmic drop = iR
                V_iR = V.mean()
                if V_iR < -0.59:
                    iR_list.append(iR)
                    V_list.append(V_iR)
                    Ru_list.append(R_uncompensated)            
                    
        ViRRu['iR'].append(iR_list)
        ViRRu['V'].append(V_list)
        ViRRu['Ru'].append(Ru_list)
        ViRRu['color'].append(col)
        
        idx += 1

    for j, V_plot in enumerate(ViRRu['V']):
        axs[0].plot(V_plot, ViRRu['Ru'][j], 'o', color = ViRRu['color'][j], label = label, 
                   alpha = 1, 
                   linewidth = 2, 
                   markerfacecolor='white', 
                   markeredgewidth = 2)
        axs[1].plot(V_plot, ViRRu['iR'][j], '-o', color = ViRRu['color'][j], label = label,
                    alpha = 1, 
                    linewidth = 2,
                    linestyle = '--',
                    markerfacecolor='white', 
                    markeredgewidth = 2
                    )                     
    R_nom = 56.2    
    axs[0].axhline(y = R_nom, linewidth=2, color='k', alpha = 0.5, linestyle = '--')
    
 
    
    for ax in axs:
        # ax.set_xlim(left = 0)
        # pltF.global_minor_locator(ax, x_locator = 5, y_locator = 5)    
        # pltF.global_mayor_xlocator(ax, x_locator = 0.1) 
        pltF.global_settings(ax)
    # pltF.global_legendbox(ax[1])
    
    axs[1].set_xlim(left = -1, right = 0)
    axs[0].set_ylim(bottom = 40, top = 80)
    axs[1].set_ylim(bottom = 0)
    
    # pltF.global_mayor_ylocator(axs[0], y_locator = 10)      
    # pltF.global_mayor_ylocator(axs[1], y_locator = 0.5)         
    pltF.CA_global(axs[0], ylabel = R.name, xlabel = V.name, legend = False)
    pltF.CA_global(axs[1], ylabel = 'V', xlabel = V.name, legend = False)
    
    if save_RvsVvsRHE_comparison_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)               
            

    





    