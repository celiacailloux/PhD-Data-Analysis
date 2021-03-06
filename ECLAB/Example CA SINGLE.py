#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on:                     Tue Mar 12 09:57:32 2019

@author:                        celiacailloux

Updated:                        Jun 14          2020

Experiment name:                TEMPLATE

                                FOR SINGLE CA ANALYSIS AND OHMIC DROP
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

plot_IVvstime = False
save_Ivvstime_plot = True

plot_Rvstime = True
save_Rvstime_plot = True

plot_RvsVvsRHE = False
save_RvsVvsRHE_plot = True

exp_dir = r'O:\list-SurfCat\setups\307-059-largeCO2MEA\Data\Celia - EC largeCO2MEA data\EC-lab\20200602 Cu KHCO3 Stability'

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
    
#_____________ Step 4: Plotting ____________________________________________
''' j and V over time ''' 
if plot_IVvstime:
    fig, axs = plt.subplots(3,1, sharex = True,  gridspec_kw={'hspace': 0.1}) 
    fig.set_size_inches(w=11,h=9)
    color = pltF.color_maps('jkib')  
    title = CA1.exp_name
    comment = 'j, VvsRHE, VvsAgAgCl'
    N = len(CA1.CA_data)
    idx = 0
    
        
    for filename, CA_data in CA1.CA_data.items():
            
        label = 'Change'
        col = color(idx/(N))#*1.2))

        VvsRHE = CA_data['Ewe/RHE']
        VvsREF = CA_data['Ewe/V']
        j = CA_data['I/mAcm-2']
        t = CA_data['time/h']
        
        axs[0].plot(t, j, color = col, label = label, alpha = 1, linewidth = 2)       
        axs[1].plot(t, VvsRHE, color = col, label = label, alpha = 1, linewidth = 2)       
        axs[2].plot(t, VvsREF, color = col, label = label, alpha = 1, linewidth = 2)      
        idx += 1
    #axs.axhline(y = -1.00, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder=1)
    #pltF.global_legendbox(axs[0])

    for ax in axs:
        #ax.set_ylim(-2,0)   
        ax.set_xlim(left = 0)             
        pltF.global_mayor_xlocator(ax, x_locator = 1)
        pltF.global_settings(ax)
    pltF.global_minor_locator(axs[0], x_locator = 2, y_locator = 2)                
    pltF.global_minor_locator(axs[1], x_locator = 2, y_locator = 5)                
    pltF.global_mayor_ylocator(axs[0], y_locator = 2)
    pltF.global_mayor_ylocator(axs[1], y_locator = 0.2)
    pltF.global_mayor_ylocator(axs[2], y_locator = 0.2)      
    pltF.CA_global(axs[0], ylabel = j.name, xlabel = None, legend = False)
    pltF.CA_global(axs[1], ylabel = VvsRHE.name, xlabel = None, legend = False)
    pltF.CA_global(axs[2], ylabel = VvsREF.name, xlabel = t.name, legend = False)
    
    if save_Ivvstime_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)
    else:
        plt.show()
    

''' Resistance over time '''    
if plot_Rvstime:
    
    fig, axs = plt.subplots(2,1, sharex = True,  gridspec_kw={'hspace': 0.1}) 
    fig.set_size_inches(w=11,h=6)
    color = pltF.color_maps('jkib')  
    title = CA1.exp_name
    comment = 'R_uncomp, Ohmic Drop'
    N = len(CA1.CA_data)
    idx = 0
    
   
    for filename, CA_data in CA1.CA_data.items():
        label = 'Change'  
        col = color(idx/(N))
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
    
    if save_Ivvstime_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)




    
''' Compring two experiments - RvsVvsRHE '''
if plot_RvsVvsRHE:
    fig, axs = plt.subplots(2,1, sharex = True,  gridspec_kw={'hspace': 0.1}) 
    fig.set_size_inches(w=11,h=6)
    # color = plt.get_cmap('tab20c')  
    color = pltF.color_maps('jkib')  
    title = CA1.exp_name
    comment = 'RvsVvsRHE'
    N = len(CA1.CA_data)
    idx = 0
    
    ViRRu = {'iR': [], 'V': [], 'Ru':[], 'color': []}
        
    iR_list = []
    V_list = []
    Ru_list = []
    
    for filename, CA_data in CA1.CA_data.items():
        col = color(idx/(N))
            
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
        pltF.global_minor_locator(ax, x_locator = 5, y_locator = 5)    
        pltF.global_mayor_xlocator(ax, x_locator = 0.1) 
        pltF.global_settings(ax)
    # pltF.global_legendbox(ax[1])

    axs[0].set_ylim(bottom = 40, top = 80)
    axs[1].set_ylim(bottom = 0)
    
    pltF.global_mayor_ylocator(axs[0], y_locator = 10)      
    pltF.global_mayor_ylocator(axs[1], y_locator = 0.5)         
    pltF.CA_global(axs[0], ylabel = R.name, xlabel = V.name, legend = False)
    pltF.CA_global(axs[1], ylabel = 'V', xlabel = V.name, legend = False)
    
    if save_RvsVvsRHE_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)        

# Old Rvstime in case I fuck up        
# ''' Resistance over time '''    
# if plot_Rvstime:
    
#     fig, axs = plt.subplots(2,1, sharex = True,  gridspec_kw={'hspace': 0.1}) 
#     fig.set_size_inches(w=11,h=6)
#     color = pltF.color_maps('jkib')  
#     title = CA1.exp_name
#     comment = 'R_uncomp, Ohmic Drop'
#     N = len(CA1.CA_data)
#     idx = 0
    
   
#     for filename, CA_data in CA1.CA_data.items():
        
#         label = 'Change'
#         col = color(idx/(N))#*1.2))

#         R = CA_data['Ru/Ohm']
#         t = CA_data['time/h']
        
#         R_uncompensated = R.mean()
#         if R_uncompensated == 0.00:
#             print('NB! \nFor \'{}\' no resitance measured/detected (Ru = 0.00).'.format(filename))
#         else:
#             iR = abs(CA_data['I/mA'].divide(1000).mean()*R_uncompensated)    # ohmic drop = iR
#             t_iR = t.iloc[0]
            
#             axs[0].plot(t_iR, R_uncompensated, '-o', color = col, label = label, 
#                        alpha = 1, 
#                        linewidth = 2, 
#                        markerfacecolor='white', 
#                        markeredgewidth = 2)
#             axs[1].plot(t_iR, iR, '-o',color = col,  label = label, alpha = 1, 
#                        linewidth = 2, 
#                        markerfacecolor='white', 
#                        markeredgewidth = 2)    
#             idx += 1
#     R_nom = 56.2    
#     axs[0].axhline(y = R_nom, linewidth=2, color='k', alpha = 0.5, linestyle = '--')
    
#     for ax in axs:
#         ax.set_xlim(left = 0)
#         pltF.global_minor_locator(ax, x_locator = 6, y_locator = 5)
#         pltF.global_mayor_xlocator(ax, x_locator = 1) 
#         pltF.global_settings(ax)
#     # pltF.global_legendbox(ax[1])

#     axs[0].set_ylim(bottom = 40, top = 80)
#     axs[1].set_ylim(bottom = 0)
#     pltF.global_mayor_ylocator(axs[1], y_locator = 0.2)         
#     pltF.CA_global(axs[0], ylabel = R.name, xlabel = None, legend = False)
#     pltF.CA_global(axs[1], ylabel = 'V', xlabel = t.name, legend = False)
    
#     if save_Ivvstime_plot:
#         pltF.global_savefig(fig, plt_title = title, addcomment = comment)        
