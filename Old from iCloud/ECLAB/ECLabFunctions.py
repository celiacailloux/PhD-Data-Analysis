#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 11:38:40 2019

@author: celiacailloux

Updated on Wed Jul 3          2019
"""
import os

#import matplotlib.pyplot as plt
#from matplotlib.ticker import AutoMinorLocator
#import numpy as np
#import math
from ExperimentsDetails import experiments as exps_details
import OSfunctions as OSfunc
from ECLabData import ECLabDataCVNew, ECLabDataCPNew

import PlottingFunctions as pltF


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 07:40:09 2019

@author: celiacailloux
"""
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np
import math

'''_________ Updated on Wed Jul 3 2019 ________________________________________'''
def plot_single_CV(dataframe, ax, color):    
    cyc_i = dataframe.iloc[0]['cycle number']
    cyc_f = dataframe.iloc[-1]['cycle number']
      
    #num_intervals = get_number_of_intervals(color_interval, cyc_i, cyc_f)
    cyc_start = cyc_i    
    
    #for idx, interval in enumerate(np.arange(num_intervals)):
        #interval += 1
        #cyc_stop = cyc_i+interval*color_interval-1
        #print(cyc_i)
        #print('cycle stop: {}'.format(cyc_stop))
        
        #cyc_range = np.arange(cyc_start,cyc_stop+1, 1)
    #x, y = data_cyc_range(dataframe, dataframe, cyc_range)  
        #print('cycle range: {}'.format(cyc_range))
        
        #if cyc_stop not in x['cycle number'].values:
            #print('cycle stop: {}'.format(cyc_stop))
            #yc_stop = cyc_f
            #print('cycle f: {}'.format(cyc_f))
            
    label = dataframe.exp_name#'{:.0f}:{:.0f}'.format(cyc_start, cyc_stop)
    ax.plot(dataframe['Ewe/V'],dataframe['<I>/mA'], color = color, label = label, alpha = 1)


def plot_color_coded_CV(dataframe, ax, color, color_interval):    
    cyc_i = dataframe.iloc[0]['cycle number']
    cyc_f = dataframe.iloc[-1]['cycle number']
      
    num_intervals = get_number_of_intervals(color_interval, cyc_i, cyc_f)
    cyc_start = cyc_i    
    
    for idx, interval in enumerate(np.arange(num_intervals)):
        interval += 1
        cyc_stop = cyc_i+interval*color_interval-1
        #print(cyc_i)
        #print('cycle stop: {}'.format(cyc_stop))
        
        cyc_range = np.arange(cyc_start,cyc_stop+1, 1)
        x, y = data_cyc_range(dataframe, dataframe, cyc_range)  
        #print('cycle range: {}'.format(cyc_range))
        
        if cyc_stop not in x['cycle number'].values:
            #print('cycle stop: {}'.format(cyc_stop))
            cyc_stop = cyc_f
            #print('cycle f: {}'.format(cyc_f))
            
        label = '{:.0f}:{:.0f}'.format(cyc_start, cyc_stop)
        ax.plot(x['Ewe/V'],y['<I>/mA'], color = color(float(idx)/int((num_intervals*1.4))), label = label, alpha = 1)
        cyc_start += color_interval 
    return ax, x, y  
    
def get_number_of_intervals(cyc_interval, cyc_i, cyc_f):
    number_of_intervals = math.ceil((cyc_f+1-cyc_i)/cyc_interval)
    #cyc_interval * math.ceil(cyc_f / cyc_interval)                              # round up to nearst 10
    return number_of_intervals

def data_cyc_range(x, y, cyc_range):
    x = x.loc[x['cycle number'].isin(cyc_range)]
    y = y.loc[y['cycle number'].isin(cyc_range)]
    return x, y



'''___________Old functions ___________________________________________________'''

'''______________________COLOR CODED________________________________________'''
def get_CC_CV_Ar_plot(exp_data, CC_interval):
    Ar_cyc_i,Ar_cyc_f = exp_data.cycle_start, exp_data.Ar_cycle_end
    
    x_Ar = exp_data.get_potential_cyc_range(Ar_cyc_i, Ar_cyc_f)
    y_Ar = exp_data.get_current_cyc_range(Ar_cyc_i, Ar_cyc_f)
 
    plot(
            x_Ar, 
            y_Ar, 
            title = exp_data.name, 
            exp_details = exp_data.exp_details, 
            label = exp_data.path_file, 
            settings = {'color interval': CC_interval }) 


'''________________________________________________________________________'''
                    
def color_map():
    col = ['steelblue', 'limegreen','orangered', 'palevioletred','olive',
           'dimgray','indigo', 'b','g', 'r','m', 'y', 'k', 'c']
    return col


def plot(x, y, title, exp_details, label, settings, x_add = None, y_add = None, subsetting = None):
    c = color_map()
    
    color = plt.get_cmap('viridis')                                             #
    
    fig, ax = plt.subplots(1, figsize = (7,6)) 
     
    if settings == 'I_vs_V':
        ax.plot(x, y, label = label, color = c[0], linewidth = 1.2)#, marker = 'o')
        ax.set_xlim([-1.2, 0])
        ax.set_ylim([-8, 0])
           

        ax.yaxis.tick_right()
        ax.xaxis.tick_top()
        ax.yaxis.set_label_position('right')
        ax.xaxis.set_label_position('top')
        ax.set_xlabel('V / V vs. RHE ', fontsize=16)
        ax.set_ylabel('j / mA cm$^{-2}$', fontsize=16) 
        ax.legend(loc='center left', bbox_to_anchor=(1.2, 0.5))
        ax.yaxis.set_minor_locator(AutoMinorLocator(4))
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        
        if x_add is not None and subsetting is None:
            ax.plot(x_add, y_add, label = 'Ar', color = c[1], linewidth = 1.1)
            ax.axhline(y = -5.00, linewidth=2, color='k', alpha = 0.5, linestyle = ':')
        elif x_add is not None and subsetting == 'intercept' :
            ax.plot(x, y, label = label, color = c[0], linewidth = 1.2, markersize = 4)
            x_min = math.floor(x_add.min()*100)/100
            x_max = math.ceil(x_add.max()*100)/100
            ax.set_xlim([x_min, x_max])
            ax.set_ylim([-5.5, -4.5]) 
            ax.axhline(y = -5.00, linewidth=2, color='k', alpha = 0.5, linestyle = ':')
            ax.plot(x_add, y_add, label = 'Intercepts', color = c[0], marker ='o', markersize = 6, markeredgecolor = 'k', linestyle = 'None')# alpha = 1, s = 100)#), edgecolor = 'k', linewidths = 0.5)#, 
                       #linewidth = 1.1, s = 6, capsize = 5, mec ='k')        
          
        else:
            ax.axhline(y = -5.00, linewidth=2, color='k', alpha = 0.5, linestyle = ':')
    elif settings == 'CO pot shift':
        ax.errorbar(x, y, y_add, fmt='o', color = c[0], markersize = 6, capsize = 5, mec ='k', linestyle = '-', linewidth = 1)
        ax.set_xlabel('CO cycles / N$^\circ$', fontsize=16)
        ax.set_ylabel('Potential shift \n at 5 mA cm$^{-2}$ / mV ', fontsize=16)        
        ax.yaxis.set_minor_locator(AutoMinorLocator(4))
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        ax.set_ylim([0, 350])
        ax.set_xlim([0,x.max()+1])
        if subsetting == 'zoom':
            ax.set_ylim([0, math.ceil(y.max()+y_add.max())])
    elif 'color interval' in settings:
        #fig, (ax, ax0) = plt.subplots(2, sharex=True, sharey=True)
        
        cyc_interval = settings['color interval']
        
       
        if x_add is not None: #For Ar
            ax, x_Ar, y_Ar = plot_coded_CV(x_add, y_add, cyc_interval, ax, gas = 'Ar')  
        
        ax, x_CO, y_CO = plot_coded_CV(x, y, cyc_interval, ax, gas = 'CO')# For CO
        
        pltF.detail_annotation(ax, text = exp_details['WE'], pos = 1)
        pltF.global_annotation(ax, text_title = label, text_list = exp_details, pos = 1)            
        pltF.CV_global(ax, hline = False)
        pltF.global_minor_locator(ax, x_locator = 4, y_locator = 1) 
        pltF.global_mayor_locator(ax, x_locator = 0.2, y_locator = 0.02)  
        pltF.global_legendbox(ax, loc = 'right')
        pltF.global_lim(ax, x_lim = [-0.5,0.5], y_lim = [-0.08,0.05])
        
    elif settings == 'CP' or settings == 'OCV':

        ax.plot(x, y, label = label, color = color(float(3)/4), linewidth = 3)
        ax = CP_plot_settings(ax)
        x_min = -2.5
        
        ax.set_xlim(left = x_min)
        ax.set_ylim(-1.4,1)
#        ax.set_xlim(x_min,320)
#        ax.set_ylim(-1.25,1)

        ax = include_details(ax, exp_details, title, x_min, settings = settings)
    else:
        print('REMEMBER TO CHOOSE settings!!')        


    pltF.global_settings(ax)    
    pltF.global_savefig(fig, plt_title = title , addcomment = label + ' Zn redox wave')
    



def plot_coded_CV(x, y, cyc_interval, ax, gas):
    if gas == 'Ar':
        color = pltF.color_maps('greenblue')
    elif gas == 'CO':
        color = pltF.color_maps('greenblue')
    
    cyc_i = x.iloc[0]['cycle number']
    cyc_f = x.iloc[-1]['cycle number']
    
    #print('numbers are: {}:{}'.format(cyc_i, cyc_f))
  
    num_intervals = get_number_of_intervals(cyc_interval, cyc_i, cyc_f)
    #print(num_intervals)
    cyc_start = cyc_i    
    
    for idx, interval in enumerate(np.arange(num_intervals)):
        interval += 1

        cyc_stop = cyc_i+interval*cyc_interval-1
        #print(cyc_i)
        #print('cycle stop: {}'.format(cyc_stop))
        
        cyc_range = np.arange(cyc_start,cyc_stop+1, 1)
        x_CO, y_CO = data_cyc_range(x,y, cyc_range)  
        #print('cycle range: {}'.format(cyc_range))
        
        if cyc_stop not in x_CO['cycle number'].values:
            #print('cycle stop: {}'.format(cyc_stop))
            cyc_stop = cyc_f
            #print('cycle f: {}'.format(cyc_f))
            
        label_CO = '{:.0f}:{:.0f}'.format(cyc_start, cyc_stop)
        ax.plot(x_CO['Ewe/V'],y_CO['<I>/mA'], color = color(float(idx)/num_intervals), label = label_CO, alpha = 0.95)
        cyc_start += cyc_interval 
    return ax, x_CO, y_CO       


def CP_plot_settings(ax, x_lim = [], y_lim = []):

    ax.set_xlabel('Time / min', fontsize=16)#ax.set_xlabel('Time / s', fontsize=16)    
    ax.set_ylabel('V / V vs. RHE ', fontsize=16) 
    #ax.legend(loc='center left', fontsize = 16, bbox_to_anchor=(1.3, 0.5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    
    if x_lim:
        ax.set_xlim(x_lim)
    if y_lim:
        ax.set_ylim(y_lim)
    else:
        ax.set_ylim(top = -0.0)

    return ax
    


'''_________________________________________________________________________'''

''' Chooses between the different experiment types.Eg. 'CV' or 'CP '''
def create_ECLabData_object(chosen_exp, number_of_experiments = 'multiple'):  
    # exp er fx 20190403 Ag

    
    # Master file directory
    if number_of_experiments == 'multiple':
        MFD = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC Lab'      
    elif number_of_experiments == 'single':
        MFD = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC Lab/CO potential shift'
    elif number_of_experiments == 'singleZn':
        MFD = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC Lab/Zn contamination'
        exp_type = exps_details[chosen_exp]['Experiment type']    

    exp_path = OSfunc.find_subsubd(chosen_exp, MFD)                             #returns DIRECTORY PATH    
    path_files = OSfunc.ECLab_find_txt_files(exp_path, exp_type)                #return FILE PATH (may be MULTIPLE)

    exps_data = {}
    for path_file in path_files:

        #print('pathfiles: {}'.format(path_files))
        subsub_d = os.path.basename(exp_path)
        filename = os.path.splitext(os.path.basename(path_file))[0]             #return only 'trial 1' in trial1.txt
        if exp_type == 'CV':
            exps_data[chosen_exp+filename] = ECLabDataCVNew(
                subsub_d, 
                path_file, 
                exp_details = exps_details[chosen_exp]
                )
        elif 'CP' in exp_type or 'OCV' in exp_type:
            print(filename)
            exps_data[chosen_exp+filename] = ECLabDataCPNew(
                subsub_d, 
                path_file, 
                exp_details = exps_details[chosen_exp]
                )
            #print(exps_data[chosen_exp+filename].potential)
        else:
            print('Error: Experiment type not recognized!')
        #print(exp_data.exp_details)
    
    return exps_data