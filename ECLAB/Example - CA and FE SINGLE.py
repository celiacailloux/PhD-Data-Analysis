#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on:                     Mar 12 2020

@author:                        celiacailloux

Updated:                        Sep 20 2020

Experiment name:                EXAMPLE

                                SINGLE CA and GC summary report and FE plot
                                & 
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
                           
                           
#---------------------------------------------------- Step 1: Choose Experiment

importECLabData         = False
importGCSummaryReport   = False

plot_IVvstime           = False
plot_jvstimestamp       = False

plot_FE                 = False
plot_TafelPlot          = True
save_plot               = False
plot_label              = False
print_FE_sum_FE         = True

save_plot               = True
plot_label              = False

" change "

" exp_dir usually in ...O:\list-SurfCat\...\EC-lab\..."
" GC_dir usually in ...O:\list-SurfCat\GC - Perkin Elmer\..."
exp_dir     = r'O:\list-SurfCat\setups\307-059-largeCO2MEA\Data\Celia - EC largeCO2MEA data\EC-lab\20200916 Cu3 CO2R Staircase'
GC_dir      = r'O:\list-SurfCat\setups\307-059-largeCO2MEA\Data\Celia - EC largeCO2MEA data\GC - Perkin Elmer\20200916 Cu CO2R Staircase'

# ----------------------------------------------------------------------------
''' General setting for Ru-plotting '''

Ru_mean = 26.13         # run 'plot_RvsVvsRHE' to get mean value

t_minor_locator = 2
t_major_locator = 1
j_major_locator = 5
j_minor_locator = 5
V_minor_locator = 4 
V_major_locator = 0.4

# ----------------------------------------------------------------------------
''' General setting for IVvsTime-plotting '''
# potentially copy from " ... - CA and iR-DROP SINGLE"
j_min, j_max            = -18, 0.1
Vref_min, Vref_max      = -1.7, -0.5 
Vrhe_min, Vrhe_max      = -1.2, 0

# ----------------------------------------------------------------------------
" ------ Info required for the script to plot Tafel Plots "
Ru_mean = 32.42         # run 'plot_RvsVvsRHE' to get mean value
products                = ['FID-CO FE',     # carbonmonoxide
                           'FID-C2H4 FE',   # ethylene
                           'TCD-H2 FE',
                           'FID-CH4 FE',
                           ]

# -------------------------------------------------------- Step 2: Import Data 
''' Use the different classes (CV, CP etc)'''
if importECLabData:

    """ import CAs """
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



# ------------------------------------------------------Step 4: Plot j vs Time 
if plot_IVvstime:
    fig, axs = plt.subplots(3,1, 
                            sharex = True,  
                            gridspec_kw={'hspace': 0.1})  
    fig.set_size_inches(w=6,h=9)
    color = pltF.color_maps('jkib')   
    title = CA1.exp_name
    comment =  'j, VvsRHE, VvsAgAgCl, GC injection'
    N = len(CA1.CA_data)
    idx = 0
    
    # j = []
    # GC = GCs[len(CAs)-1]
    injection_time = \
        GC1.data[list(GC1.data.keys())[0]]['Time of Injection'].astype(str)
    
    " the following is only necessary if "
    " the CA file has been recorded pr every "
    " 2 or more seconds."
    # injection_time = [x[:-1] for x in injection_time]
    #print(list(injection_time))
    
    for filename, CA_data in CA1.CA_data.items():
        
        label = filename
        col = color(idx/(N))
        VvsRHE = CA_data['Ewe/RHE']
        VvsREF = CA_data['Ewe/V']
        j = CA_data['I/mAcm-2']
        t = CA_data['time/h']

        
        time = CA_data['time/datetime'].dt.time.astype(str)
        # print('test time {}'.format(time[1][:5]))
        # _time = time[1][:5]
        # print(injection_time[0][:5])
        
        #for injection in injection_time:
        _bool = \
            CA_data['time/datetime'].dt.time.astype(str).str.contains('|'.join(injection_time))
        t_datetime = CA_data['time/h'][_bool]
        VvsSHE_injection = CA_data['Ewe/V'][_bool]
        j_injection = CA_data['I/mAcm-2'][_bool]
        
        ''' write some code that checks wether the first injection
        is injected before EC-start '''
                       
     
        axs[0].plot(t, j, color = col, label = label, alpha = 1, linewidth = 2)       
        axs[0].plot(t_datetime, 
                    j_injection, 
                    'o', 
                    color = 'k',#"col, 
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
        ax.set_xlim(left = 0)#, right = 6)             
        pltF.global_mayor_xlocator(ax, x_locator = t_major_locator)
        pltF.global_settings(ax)
             
    " possibly change "
    axs[0].set_ylim(bottom  = j_min, 
                    top     = j_max)
    axs[1].set_ylim(bottom  = Vrhe_min, 
                    top     = Vrhe_max)
    axs[2].set_ylim(bottom  = Vref_min, 
                    top     = Vref_max)
    
    pltF.global_mayor_ylocator(axs[0], y_locator = j_major_locator)        
    pltF.global_mayor_ylocator(axs[1], y_locator = V_major_locator)
    pltF.global_mayor_ylocator(axs[2], y_locator = V_major_locator)
    pltF.global_minor_locator(axs[0], 
                              x_locator = t_minor_locator, 
                              y_locator = j_minor_locator)                
    pltF.global_minor_locator(axs[1], 
                              x_locator = t_minor_locator, 
                              y_locator = V_minor_locator)  
    pltF.global_minor_locator(axs[2], 
                              x_locator = t_minor_locator, 
                              y_locator = V_minor_locator)  
    pltF.CA_global(axs[0], ylabel = j.name, xlabel = None, legend = False)
    pltF.CA_global(axs[1], ylabel = VvsRHE.name, xlabel = None, legend = False)
    pltF.CA_global(axs[2], ylabel = VvsREF.name, xlabel = t.name, legend = False)
    pltF.global_settings(axs[0])
    pltF.global_settings(axs[1])
    pltF.global_settings(axs[2])
    # axs[1].axhline(y = -0.1, linewidth=2, color='k', alpha = 0.5, linestyle = '--')
    
    
    print('Printing \'{}\' but remember that there most likely will have', \
          'occured a GC injection prior to the experiment!')
    
    if save_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)
        plt.close()
    else:
        plt.show()
        
        
        
' _____________________________________________ Plot j vs timestamp (Step 5) '
if plot_jvstimestamp:
    
    fig, axs = plt.subplots(3,1, 
                            sharex = True,  
                            gridspec_kw={'hspace': 0.1})
    fig.set_size_inches(w=9,h=9)
    color = pltF.color_maps('jkib')   
    title = CA1.exp_name
    comment =  'j, VvsRHE, VvsAgAgCl, GC injection, timestamp'
    N = len(CA1.CA_data)
    idx = 0
    
    
    
    GC = GCs[len(CAs)-1]
    # get time of injection from GC_summary.excel
    injection_time = \
        GC1.data[list(GC1.data.keys())[0]]['Time of Injection'].astype(str)
    
    " the following is only necessary if "
    " the CA file has been recorded pr every "
    " 2 or more seconds."
    # injection_time = [x[:-1] for x in injection_time]
    #print(list(injection_time))
    # removes the last digit in timestamp (eg. 06:52:15 > 06:52:1)
    # injection_time = [x[:-1] for x in injection_time]
    
    j_avg_df = GC1.compute_j_avg_df(CA1)
    jt_data = \
        pd.DataFrame(columns=['time/datetime','I/mAcm-2'])
    
    for filename, CA_data in CA1.CA_data.items():
        
        label = filename
        col = color(idx/(N))

        j       = CA_data['I/mAcm-2']
        VvsRHE  = CA_data['Ewe/RHE']
        VvsREF  = CA_data['Ewe/V']
        t       = CA_data['time/datetime']
        
        # t = CA_data['time/h']
        
        # find all j that have the same timestamp as GC (should)
        # only be 1 file
        _bool = \
            CA_data['time/datetime'].dt.time.astype(str).str.\
                contains('|'.join(injection_time))
        jt_data  = \
            jt_data.append(CA_data[['time/datetime','I/mAcm-2']][_bool])                        

        " plots current as a function of time "
        axs[0].plot(t.dt.strftime('%H:%M'), 
                    j, 
                    color = col, 
                    label = label, 
                    alpha = 1, 
                    linewidth = 2)             
        axs[1].plot(t.dt.strftime('%H:%M'), 
                    VvsRHE, 
                    color = col, 
                    label = label, 
                    alpha = 1, 
                    linewidth = 2)             
        
        idx += 1
    jt_data['time/datetime'] = jt_data['time/datetime'].dt.strftime('%H:%M')
    print('---------- For time stamp plotting ---------')
    print(jt_data)
    print('Total number of overlapping timestamps:   {}'.\
          format(len(jt_data['time/datetime'])))
                                                
    print('--------------------------------------------')      
    
    axs[0].plot(jt_data['time/datetime'], 
              jt_data['I/mAcm-2'], 
              'o', 
              color = 'k',
              label = 'GC injection timestamps', 
              markersize = 4,
              markerfacecolor='white',
              markeredgewidth = 1)                
    axs[0].plot(j_avg_df['time/timestamp'], 
              j_avg_df['j avg'], 'o', 
              color = 'r',
              label = 'Average current density', 
              markersize = 4,
              markerfacecolor='white',
              markeredgewidth = 1)
         
    " possibly change "
    pltF.global_settings(axs[0])
    pltF.global_settings(axs[1])
    pltF.global_settings(axs[2])
    axs[1].set_ylim(top     = 0,
                    bottom  = -1.2)
    pltF.global_mayor_ylocator(axs[0], y_locator = j_major_locator)        
    pltF.global_minor_locator(axs[0], 
                              x_locator = None, 
                              y_locator = j_minor_locator)                
    pltF.CA_global(axs[0], ylabel = j.name, xlabel = None, legend = True)
    pltF.CA_global(axs[1], ylabel = VvsRHE.name, xlabel = None, legend = False)
    pltF.CA_global(axs[2], ylabel = VvsREF.name, xlabel = None, legend = False)
    # plt.xticks(j_avg_df['time/timestamp'])
    axs[0].set_xticks(j_avg_df['time/timestamp'])
    plt.xticks(rotation = 45, ha = 'right')
    # axs.set_xlim(left = 0)#, right = 6)             
    
    if save_plot:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)
        plt.close()
    else:
        plt.show()        

# ----------------------------------------- Step 6: FE plottimg and Tafel Plot
if plot_FE or plot_TafelPlot:
    
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
    
    " j average "
    " Remove all the following indeces AND resets index"
    # removes a specific index of j_avg - not commonly used!
    j_avg_df = j_avg_df.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19]).reset_index(drop = True)#j_avg_df.index[0])
    
    # j_avg_df = j_avg_df.drop([j_avg_df.index[8]]).reset_index(drop = True)
    # removes the first row
    # j_avg_df = j_avg_df.drop(j_avg_df.index[0]).reset_index()
    # removes the last row average j
    # j_avg_df = j_avg_df.drop(j_avg_df.index[-1])
    
    " GC"
    " Keep index = 1 and 9"
    # removes the first row of GC
    peak_areas[GC_file_name] = peak_areas[GC_file_name].drop([0,1,2,3,4,5,6]).reset_index(drop = True)
    # peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[0]).reset_index(drop = True) 
    # removes the last row of GC
    # peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[-1])
    # peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[-1])
    # peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[-1])
    # peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[-1])
     
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
        # [row,col]
        # axs[0,0].set_ylim(bottom = 1e-2, top = 1.5e1)            
        # axs[0,1].set_ylim(bottom = 1e-2, top = 1.5e1)            
        # axs[1,0].set_ylim(bottom = 1e-1, top = 5e0)            
        # axs[1,1].set_ylim(bottom = 1e-1, top = 5e0)   
        # fig.canvas.draw()         
        pltF.TafelPlot_global(axs,
                         V_major_locator = 0.1,
                         j_major_locator = 1,                          
                         grid = True)  
        
        
        
    if save_plot:
        # plt.tight_layout()
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)
        plt.close()
    else:
        plt.show()          
  
# ------------------------------------------------ OLD FE PLOT SCRIPT

# if plot_FE:    
#     '''
#     This code is definitely not ideal BUT for the moment is serves
#     the purpose. However, the average currents might not be the exact averages
#     '''
#     fig, ax = plt.subplots()
#     ax_right = ax.twinx()
    
    
#     " ----- Get GC data and calibration "
#     GC_file_name = list(GC1.data.keys())[0]
#     GC_summary_data = GC1.data[GC_file_name]
#     injection_time = GC1.data[GC_file_name]['Time of Injection'].astype(str)
#     # removes the last digit in timestamp (eg. 06:52:15 > 06:52:1)
#     injection_time = [x[:-1] for x in injection_time]
#     calibration_CO2R = GC1.calibration_CO2R
#     title = CA1.exp_name
#     comment =  'FE plot'  
#     # color = pltF.color_maps('jkib')
#     # color = pltF.color_maps('inv_jkib')
#     color = pltF.color_maps('FE_gb')
    
#     " ----- GC settings"       
#     flow = 5 #sccm
#     molar_volume = 22.4 #
#     molar_flow = flow * 1/molar_volume*1e-3/60
#     F = 96485.33212 #C/
    
#     " ----- Average current"       
#     j_avg_df = GC1.compute_j_avg_df(CA1)
#     peak_areas = GC1.peaks_areas
    
#     " possibly change "
#     ''' Be careful using the next lines '''
#     j_avg_all = j_avg_df
#     print('--------------------------------------')
#     print('       All current and potentials are: \n{}'.format(j_avg_all[['j avg','V avg/RHE', 'time/timestamp']]))
#     print('       All GCs are: \n{}'.format(peak_areas[GC_file_name][['TCD-H2', 'Time of Injection']]))
#     print('--------------------------------------')
    
#     " j average "
#     " Remove all the following indeces AND resets index"
#     # removes a specific index of j_avg - not commonly used!
#     j_avg_df = j_avg_df.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19]).reset_index(drop = True)#j_avg_df.index[0])
    
#     # j_avg_df = j_avg_df.drop([j_avg_df.index[8]]).reset_index(drop = True)
#     # removes the first row
#     # j_avg_df = j_avg_df.drop(j_avg_df.index[0]).reset_index()
#     # removes the last row average j
#     # j_avg_df = j_avg_df.drop(j_avg_df.index[-1])
    
#     " GC"
#     " Keep index = 1 and 9"
#     # removes the first row of GC
#     peak_areas[GC_file_name] = peak_areas[GC_file_name].drop([0,1,2,3,4,5,6]).reset_index(drop = True)
#     # peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[0]).reset_index(drop = True) 
#     # removes the last row of GC
#     # peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[-1])
#     # peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[-1])
#     # peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[-1])
#     # peak_areas[GC_file_name] = peak_areas[GC_file_name].drop(peak_areas[GC_file_name].index[-1])
    

#     '''
#     Note that number of injections (N_GC) should be larger than the number
#     of CAs (N_CA). Hence the first GC measurement is a background measurement,
#     and thus SHOULD NOT BE used for FE calculations. N_GC > N_CA
#     '''
#     N_GC = peak_areas[GC_file_name].shape[0]
#     N_CA = j_avg_df.shape[0]
    
#     if N_CA > N_GC or N_GC > N_CA:
#         print('\nNB!')
#         print('Something is wrong with the number of GCs vs.', \
#               'the number of average currents/CAs. Check it!')
#         print(j_avg_df[['j avg', 'V avg/RHE', 'time/timestamp']])
#         print(peak_areas[GC_file_name][['TCD-H2', 'Time of Injection']])
#     else:
#         print('--------------------------------------')
#         print('\nNB!')
#         print('Correct number of GCs vs.', \
#               'the number of average currents/CAs. However, double check it!')
#         print(j_avg_df[['j avg', 'V avg/RHE', 'time/timestamp']])
#         print(peak_areas[GC_file_name][['TCD-H2', 'Time of Injection']])
#         print('--------------------------------------')
#         peak_areas = GC1.update_peak_areas_with_FE(peak_areas, GC_file_name, 
#                                       calibration_CO2R, 
#                                       F, molar_flow, j_avg_df)           
        
#         " ----- Collect all FEs in one dataframe "
#         FE_sum_df = peak_areas[GC_file_name].filter(regex='FE')

#         # plot FE with pandas plot
#         FE_sum_df.plot.bar(rot=0, 
#                            stacked = True, 
#                            figsize=(9,4), 
#                            colormap = color,
#                            ax = ax)
#         j_avg_df['j avg'].abs().plot.line(rot=0,
#                                           color = 'k',
#                                           marker = 'o',
#                                           # color = 'k',
#                                           markersize=6 ,
#                                           mfc = 'white',
#                                           linestyle = '--',
#                                           ax = ax_right)    
#         # s = 2,
#         # facecolors=None,
#         # edgecolors='k',
#         # linewidth = 3,  
#         # figsize=(9,3), 
#         # colormap = color,
#         ax.set_ylim(top = 100)
#         ax_right.set_ylim(bottom = 0)
#         " change "
#         xtick_labels_df = j_avg_df['V avg/RHE']
#             # [j_avg_all['V avg/RHE'].iloc[-1]] + [j_avg_all['V avg/RHE'].iloc[-1]]
#         pltF.global_settings(ax)
#         pltF.global_settings(ax_right)
#         pltF.FE_global(ax, 
#                        ax_right,
#                        x = FE_sum_df.index.tolist(),
#                        xtick_labels_df = xtick_labels_df,
#                        plot_label = plot_label)        
#         # pltF.global_legendbox(ax, 
#         #                       location = 'upper left', 
#         #                       loc = 'outside right' )
        
#         print(FE_sum_df.round(0).astype(int))
#         # sum of all FE
#         peak_areas[GC_file_name]['FE sum'] = FE_sum_df.sum(axis=1)
#         print(peak_areas[GC_file_name]['FE sum'].round(0).astype(int))
#     GC_file = list(peak_areas.keys())[0]           
   
 
#     if save_plot:
#         plt.tight_layout()
#         ax.figure.savefig('Figures/' + title + ' ' + comment +'.png',  
#                           dpi=200)
#         plt.close()
#     else:
#         plt.show()            
