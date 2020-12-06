#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on:                     Mar 2020

@author:                        celiacailloux

Updated:                        Sep 17 2020

Experiment name:                Example PEIS SINGLE

"""

#from ECLabData import ECLabDataCV, ECLabDataCP
from ECLabImportCAData import ECLabDataCA
from ECLabImportZIRData import ECLabDataZIR
from ECLabImportCIData import ECLabDataCI
from ECLabImportPEISData import ECLabDataPEIS
import PlottingFunctions as pltF
from PickleFunctions import save_as_pickle, get_saved_pickle

import matplotlib.pyplot as plt
import numpy as np
                          
'_____________ Step 1: Choose Experiment_____________________________________ '

importECLabData             = False

" change "
RE_position                 = 'T'
" Bode "
characteristic_frequency    = 120e3
x_major_locator             = 50e3
y1_major_locator            = 5 
x_minor_locator             = 5
y1_minor_locator            = 5 
x_min, x_max                = 50e3, 150e3
y1_min, y1_max              = 25, 40
" Nyquist "
ReZ_min, ReZ_max            = 20, 40
# ImZ_min, ImZ_max            = 20,  50
ReZ_major_loc, ReZ_minor_loc= 10, 5
ImZ_major_loc, ImZ_minor_loc= 5, 5


plot_Bodeplot               = False
plot_Nyquist                = True

save_plot                   = True

" change "
exp_dir                     = \
    r'O:\list-SurfCat\setups\307-059-largeCO2MEA\Data\Celia - EC largeCO2MEA data\EC-lab\20200916 Cu3 CO2R Staircase'

' ____________ Step 2: Import Data __________________________________________ '

if importECLabData:
    
    """ import PEISs """
    PEIS1 = ECLabDataPEIS(file_folder = exp_dir, 
                        pH = 6.8,
                        reference_electrode_potential = 'Ag/AgCl',
                        label = 'CO$_2$',
                        A_electrode = 1,                                             #cm2
                        uncompensated_R = 85,
                        )
    PEISs = [PEIS1]
        
    save_as_pickle(pkl_data = PEISs, pkl_name = 'PEISs')

else:
    PEISs = get_saved_pickle(pkl_name = 'PEISs') 
    PEIS1 = PEISs[0]
    
' _____________ Step 3: Import GC summary ___________________________________ '


''' Bodeplot '''    
if plot_Bodeplot:
    N = len(PEIS1.data)
    if N == 1:
        fig, axs = plt.subplots(N+1, 1,  sharex = False, gridspec_kw={'hspace': 0.1})   
        fig.set_size_inches(w=6,h=N+1*6)
        single_ax = True
    else:
        fig, axs = plt.subplots(N, 1,  sharex = True, gridspec_kw={'hspace': 0.1})   
        fig.set_size_inches(w=3,h=N*3)
        single_ax = False
    color = pltF.color_maps('jkib')  
    title = PEIS1.exp_name
    comment = 'Bode plot, R, phi vs f'
    
    idx = 0
    

    for filename, PEIS_data in PEIS1.data.items(): 
        phase_ax = axs[idx].twinx()            
        label = 'Change'
        # col = color(idx/(N))#*1.2))

        Z = PEIS_data['|Z|/Ohm']
        f = PEIS_data['freq/Hz']#.divide(1000)
        phi = PEIS_data['Phase(Z)/deg']
                    
        p1, = axs[idx].plot(f, Z, '-o', color = color(1/3), label = label, 
                   alpha = 1, 
                   linewidth = 2, 
                   markerfacecolor='white', 
                   markeredgewidth = 2)
        p2, = phase_ax.plot(f, phi, '-o', color = color(2/3), label = label, 
                   alpha = 1, 
                   linewidth = 2, 
                   markerfacecolor='white', 
                   markeredgewidth = 2)
        phi_Ru = 0
        pltF.global_settings(axs[idx])
        pltF.global_settings(phase_ax)
        axs[idx].axvline(x = characteristic_frequency, linewidth = 2, color='k', alpha = 0.6, linestyle = '--', zorder = 0)                
        phase_ax.axhline(y = phi_Ru, linewidth=2, color=color(2/3), alpha = 1, linestyle = '--', zorder = 0)        
        
        axs[idx].yaxis.label.set_color(color(1/3))
        phase_ax.yaxis.label.set_color(color(2/3))  
        axs[idx].tick_params(axis='y', colors=color(1/3))
        phase_ax.tick_params(axis='y', colors = color(2/3)) 
        " possibly change "
        axs[idx].set_ylim(bottom    = y1_min, 
                          top       = y1_max)
        phase_ax.set_ylim(bottom = -10, 
                          top = 2.5)
        phase_ax.set_xlim(left      = x_min,#-1e3, 
                          right     = x_max)
        pltF.global_minor_locator(axs[idx], 
                                  x_locator = x_minor_locator, 
                                  y_locator = y1_minor_locator)
        pltF.global_minor_locator(phase_ax, 
                                  x_locator = x_minor_locator, 
                                  y_locator = 5)
        pltF.global_mayor_ylocator(axs[idx], 
                                   y_locator = y1_major_locator)
        pltF.global_mayor_ylocator(phase_ax, 
                                   y_locator = 5)
        pltF.global_mayor_xlocator(axs[idx], x_locator = x_major_locator)
        pltF.PEIS_global(axs[idx], phase_ax, idx, N, grid = True, legend = False)

        idx += 1
        
    if single_ax:
        axs[-1].set_axis_off()
        axs.flat[-1].set_visible(False) 
    
    if save_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)
        plt.close()
    else:
        plt.show()
        
''' Nyquist '''    
if plot_Nyquist:
    print('Plotting Nyquist Plot ...')
    
    fig, ax = plt.subplots(1)
    fig.set_size_inches(w=4,h=4)
    color = pltF.color_maps('jkib')  
    title = PEIS1.exp_name
    comment = 'Nyquist, Im(Z) vs Re(Z)'
    N = len(PEIS1.data)
    idx = 0   
   
    for filename, PEIS_data in PEIS1.data.items():
        
        label = 'Change'
        col = color(idx/(N))

        Re = PEIS_data['Re(Z)/Ohm']
        Im = PEIS_data['-Im(Z)/Ohm']
        
        ax.plot(Re, Im, '-o', color = col, label = label, 
                   alpha = 1, 
                   linewidth = 2, 
                   markerfacecolor='white', 
                   markeredgewidth = 2)  
        if RE_position == 'T':
            ax.axvline(x = 24.8, linewidth=2, color = col, alpha = 1, linestyle = '--', zorder = 0)#, dashes=[3, 1])            
        elif RE_position == 'C':
            ax.axvline(x = 56.8, linewidth=2, color = col, alpha = 1, linestyle = '--', zorder = 0)#, dashes=[3, 1])            
        else:
            print('No RE position given')
        idx += 1
        
    ax.axhline(y = 0, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0)#, dashes=[3, 1])            
    pltF.Nyquist_global(ax, grid = True, legend = False)
    " possibly change "
    ax.set_xlim(left        = ReZ_min, 
                right       = ReZ_max)     
    # ax.set_ylim(bottom = 40, top = 80)
    pltF.global_mayor_xlocator(ax, 
                               x_locator    = ReZ_major_loc) 
    pltF.global_mayor_ylocator(ax, 
                               y_locator    = ImZ_major_loc)
    pltF.global_minor_locator(ax, 
                              x_locator     = ReZ_minor_loc, 
                              y_locator     = ImZ_minor_loc)
    pltF.global_settings(ax)
    
    if save_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)  
        plt.close()
    else:
        plt.show()

