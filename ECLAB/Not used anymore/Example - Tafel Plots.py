#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on:                     Aug 26 2020


@author:                        celiacailloux

Updated:                        Aug 26 2020

Experiment name:                EXAMPLE

                                Tafel Plots Comparing Data from Kuhl 2012 
                                (Jaramillo's group')
"""

#from ECLabData import ECLabDataCV, ECLabDataCP
from ECLabImportCAData import ECLabDataCA
# from ECLabImportZIRData import ECLabDataZIR
from GCPerkinElmerSummaryReport import GCPESummaryData
#import ECLabFunctions

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 10)

#from matplotlib.ticker import AutoMinorLocator, AutoLocator, MultipleLocator
from ECLabExperimentalPaths import exp_paths 

import PlottingFunctions as pltF
from PickleFunctions import save_as_pickle, get_saved_pickle
#from ExperimentsDetails import exps

# import pandas as pd
# pd.set_option('display.max_rows', 80)
                           
                           
# --------------------------------------------------- Step 1: Choose Experiment
importECLabData         = False
importGCSummaryReport   = False

plot_FE                 = False
plot_TafelPlot          = True
save_plot               = False
plot_label              = False
print_FE_sum_FE         = True

" ------ Info required for the script to plot Tafel Plots "
Ru_mean = 32.42         # run 'plot_RvsVvsRHE' to get mean value
products                = ['FID-CO FE',     # carbonmonoxide
                           'FID-C2H4 FE',   # ethylene
                           'TCD-H2 FE',
                           'FID-CH4 FE',
                           ]

" change "
" ------ exp_dir usually in ...O:\list-SurfCat\...\EC-lab\..."
" ------ GC_dir usually in ...O:\list-SurfCat\GC - Perkin Elmer\..."
exp_dir = r'O:\list-SurfCat\setups\307-059-largeCO2MEA\Data\Celia - EC largeCO2MEA data\EC-lab\20200821 CO2R Staircase'
GC_dir = r'O:\list-SurfCat\setups\307-059-largeCO2MEA\Data\Celia - EC largeCO2MEA data\GC - Perkin Elmer\20200821 Cu CO2R Staircase'


# -------------------------------------------------------- Step 2: Import Data 

''' Use the different classes (CV, CP etc)'''
if importECLabData:

    " ----- import CAs "
    CA1 = ECLabDataCA(file_folder = exp_dir, 
                       pH = 6.8,
                       reference_electrode_potential = 'Ag/AgCl',
                       label = 'CO$_2$',
                       A_electrode = 1,                                             #cm2
                       uncompensated_R = 85,
                       Ru = Ru_mean
                       )
    
    # print(list(CA1.CA_data.keys()))
    # file_CA1_time_start = list(CA1.CA_data.keys())[0]
    # CA_ex = CA1.CA_data[file_CA1_time_start]
    
    CAs = [CA1]
    
    save_as_pickle(pkl_data = CAs, pkl_name = 'CAs')
else:
    CAs = get_saved_pickle(pkl_name = 'CAs')
    
    CA1 = CAs[0]    

# ---------------------------------------------------Step 3: Import GC summary

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



' __________________________________________________ Plot j vs Time (Step 4) '        

" ----- Get GC data and calibration "
GC_file_name        = list(GC1.data.keys())[0]
GC_summary_data     = GC1.data[GC_file_name]
injection_time      = \
    GC1.data[GC_file_name]['Time of Injection'].astype(str)
calibration_CO2R    = GC1.calibration_CO2R
peak_areas = GC1.peaks_areas
# # removes the last digit in timestamp (eg. 06:52:15 > 06:52:1)
# injection_time = [x[:-1] for x in injection_time]

" ----- GC settings"    
flow                = 5 #sccm
molar_volume        = 22.4 #
molar_flow          = flow * 1/molar_volume*1e-3/60
F                   = 96485.33212 # Faradaic Constant

" ----- Average current"    
j_avg_df            = GC1.compute_j_avg_df(CA1) #avg j from EClab txt file
j_avg_all           = j_avg_df
print('--------------------------------------')
print('       All current and potentials are: \n{}'.\
      format(j_avg_all[['j avg','V avg/RHE', 'time/timestamp']]))
print('       All GCs are: \n{}'.\
      format(peak_areas[GC_file_name][['TCD-H2', 'Time of Injection']]))
print('--------------------------------------')

" ----- possibly change "
" Be careful using the next lines "

" ----- j average "
" ----- Remove index = 2 and 9"
# ----- removes a specific index of j_avg - not commonly used!
j_avg_df        = j_avg_df.drop([2]).reset_index(drop = True)#j_avg_df.index[0])
j_avg_df        = j_avg_df.drop([j_avg_df.index[8]]).reset_index(drop = True)
# ----- removes the first row
# j_avg_df        = j_avg_df.drop(j_avg_df.index[0]).reset_index()
# ----- removes the last row average j
# j_avg_df        = j_avg_df.drop(j_avg_df.index[-1])

" ----- GC injections"
" ----- Keep index = 1 and 9"
# removes the first row of GC
peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[0]).reset_index(drop = True) 
# removes the last row of GC
peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[-1])
peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[-1])
peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[-1])
peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[-1])    

'''
Note that number of injections (N_GC) should be larger than the number
of CAs (N_CA). Hence the first GC measurement is a background measurement,
and thus SHOULD NOT BE used for FE calculations. N_GC > N_CA
'''
N_GC        = peak_areas[GC_file_name].shape[0]
N_CA        = j_avg_df.shape[0]

if N_CA > N_GC or N_GC > N_CA:
    print('--------------------------------------')
    print('\nNB!')
    print('Something is wrong with the number of GCs vs.', \
          'the number of average currents/CAs. Check it!')
    print(j_avg_df[['j avg', 'V avg/RHE', 'time/timestamp']])
    print(peak_areas[GC_file_name][['TCD-H2', 'Time of Injection']])
    print('--------------------------------------')
else:
    print('--------------------------------------')
    print('Correct number of GCs vs.', \
          'the number of average currents/CAs. However, double check it!')
    print(j_avg_df[['j avg', 'V avg/RHE', 'time/timestamp']])
    print(peak_areas[GC_file_name][['TCD-H2', 'Time of Injection']])
    print('--------------------------------------')
    peak_areas      = GC1.update_peak_areas_with_FE(peak_areas, 
                                                    GC_file_name, 
                                                    calibration_CO2R, 
                                                    F, molar_flow, 
                                                    j_avg_df)           
    " ----- Collect all FEs in one dataframe "
    FE_df           = peak_areas[GC_file_name].filter(regex='FE')
    # ----- Add sum of all FEs to peaks_areas (containing peaks areas)
    peak_areas_GC1              = peak_areas[GC_file_name]
    peak_areas_GC1['FE sum']    = FE_df.sum(axis=1)         

    " ----- Plot FE with pandas plot "
    if plot_FE:
        " ----- figure settings "        
        fig, ax = plt.subplots(1,
                                sharex = True, 
                                gridspec_kw={'hspace': 0.1}) 
        # fig.set_size_inches(w=3,h=30)
        color = pltF.color_maps('FE_gb')  
        title = CA1.exp_name
        comment = 'Tafel Plots'
        N = len(CA1.CA_data)        # number of EClab txt files
        idx = 0        
        ax_right = ax.twinx()
        
        FE_df.plot.bar(rot=0, 
                           stacked = True, 
                           # figsize=(9,4), 
                           colormap = color,
                           ax = ax)
        j_avg_df['j avg'].abs().plot.line(rot=0,
                                          color = 'k',
                                          marker = 'o',
                                          # color = 'k',
                                          markersize=6 ,
                                          mfc = 'white',
                                          linestyle = '--',
                                          ax = ax_right)    
        ax.set_ylim(top = 100)
        ax_right.set_ylim(bottom = 0)
        " change "
        xtick_labels_df = j_avg_df['V avg/RHE']
            # [j_avg_all['V avg/RHE'].iloc[-1]] + [j_avg_all['V avg/RHE'].iloc[-1]]
        pltF.global_settings(ax)
        pltF.global_settings(ax_right)
        pltF.FE_global(ax, 
                        ax_right,
                        x = FE_df.index.tolist(),
                        xtick_labels_df = xtick_labels_df,
                        plot_label = plot_label)        
        pltF.global_legendbox(ax, 
                              location = 'upper left', 
                              loc = 'outside right' )
        
        
        if print_FE_sum_FE:
            print('--------------------------------------')
            print('Product and its respective FE')
            print(FE_df.round(0).astype(int))
            print('--------------------------------------')
            print('Total sum of GC FE:')
            print(peak_areas_GC1['FE sum'].round(0).astype(int))
            print('--------------------------------------')

if plot_TafelPlot:            
    " ----- Settings "
    N_of_products = len(products)
    fig, axs = plt.subplots(int(N_of_products/2), 
                            int(N_of_products/2),
                            sharex = True, 
                            sharey = False,
                            gridspec_kw={'hspace': 0.3, 
                                         'wspace': 0.3}) 
    fig.set_size_inches(w=6,h=6)
    color = pltF.color_maps('FE_gb')  
    title = CA1.exp_name
    comment = 'Tafel Plots'
    N       = len(CA1.CA_data)        # number of EClab txt files
    ax_row  = 0
    ax_col  = 0
    idx     = 0
    
   
    for GC_product in FE_df:        
        if GC_product in products:
            print(GC_product)
            print(ax_row, ax_col)
            print('--------------------------------------')
            V_avg = j_avg_df['V avg/RHE']
            j_avg = j_avg_df['j avg']
            j_FE = FE_df[GC_product].div(100).mul(j_avg)
            
            # ----- remove first row
            V_avg   = V_avg.drop([0])
            j_FE    = j_FE.drop([0])
            col = color(idx/N_of_products)
            axs[ax_row, ax_col].plot(V_avg, 
                                     np.abs(j_FE),
                                     # j_FE, 
                                     '-o', 
                                     color = col,   
                                     alpha = 1, 
                                     linewidth = 2, 
                                     markerfacecolor='white', 
                                     markeredgewidth = 2)
            pltF.global_annotation(axs[ax_row, ax_col],
                                   text_title = GC_product, 
                                   pos = 'Tafel Plot')            
            pltF.global_settings(axs[ax_row, ax_col]) 

            

            # print(V_avg)
            # print(j_avg)    
            if ax_row == ax_col:
                ax_row += 1
            elif ax_row > ax_col:
                ax_row -= 1
                ax_col += 1
            elif ax_row < ax_col:
                ax_row += 1              
            idx += 1
    axs[0,0].set_ylim(bottom = 1e-2, top = 1.5e1)            
    axs[0,1].set_ylim(bottom = 1e-2, top = 1.5e1)            
    axs[1,0].set_ylim(bottom = 1e-1, top = 5e0)            
    axs[1,1].set_ylim(bottom = 1e-1, top = 5e0)            
    pltF.TafelPlot_global(axs,
                     V_major_locator = 0.2,
                     j_major_locator = 1,                          
                    grid = True)  
    
    plt.tight_layout()
    if save_plot:        
        ax.figure.savefig('Figures/' + title + ' ' + comment +'.png',  
                          dpi=200)
        plt.close()
    else:
        plt.show()    

        
        
    
    
    
