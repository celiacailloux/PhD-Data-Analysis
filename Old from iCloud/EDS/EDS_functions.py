#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 19:59:15 2019

@author: celiacailloux
"""
from EDSData import EDSData
import PlottingFunctions as pltF

import matplotlib.pyplot as plt
import numpy as np

def gather_all_sample_composition(sample_compositions):
    dict_all = {}
    for idx, sample_composition in enumerate(sample_compositions):
        dict_all.update(sample_composition)
    return dict_all

def color_map():
    return ['b', 'g','r','c','m','y','k']

def plot_settings(ax):
    major_ticks = np.arange(0, 101, 25)
    line = np.linspace(0, 100, 1000)
    ax.plot(line,line, color = 'k', alpha = 0.4)
    ax.set_xlabel('Intended Composition / %', fontsize = 16)
    ax.set_ylabel('Measured Composition / %', fontsize = 16)
    #ax.legend(fontsize =12, loc = 'lower right')
    ax.set_ylim([0,100])
    ax.set_xlim([0,100])
    ax.set_aspect('equal', adjustable='box')
    ax.grid(which='major', color = 'k', alpha=0.4)
    ax.set_xticks(major_ticks)
    ax.set_yticks(major_ticks)
    ax.tick_params(axis='both', which='major', labelsize=12)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    return ax

def plot_samples_of_choice(elements, catalysts, intended_composition,
                           measured_sample_composition, plt_title):   
    col = color_map()
    c = dict(zip(elements, col))
        
    for i,element in enumerate(elements):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        
#        ax2 = ax.twiny()
#        newlabel = [273.15,290,310,330,350,373.15] 
    

        x = np.zeros(len(measured_sample_composition.keys()))
        y = np.zeros(len(measured_sample_composition.keys()))
        y
        yerror = np.zeros(len(measured_sample_composition.keys()))
        
        j = 0
        for sample in measured_sample_composition:
            #print('**********')
            
            #print()
            #print(measured_sample_composition[sample][element][0])
            y[j] = measured_sample_composition[sample][element][0]
            yerror[j] = measured_sample_composition[sample][element][1]
            #print(intended_composition[sample][element])
            x[j] = intended_composition[sample][element]
            '''
            #element = 'Ga'
            #sample = '20190315 NP1 After CO pot shift'
            y_box = y[j]#measured_sample_composition[sample][element][0]
            x_box = intended_composition[sample][element]

            print(y_box,x_box)
            print(type(y_box))
            '''
            #ax.annotate(catalysts[sample],(x[j]*100-x[j]*2.5, y[j]*100-yerror[j]*200),ha='center', bbox=dict(boxstyle="square", fc="w"))
            #ax.annotate(catalysts[sample],(x[j]*100-x[j]*2.5, 10),ha='center',va = 'bottom', size = 10, bbox=dict(boxstyle="square", pad = 0.2, fc="w"))
            print(sample)
            if element == 'Ti' or 'O': 
                ax.annotate(catalysts[sample],(x[j]*100+10, y[j]*100),ha='center',va = 'center', size = 10, bbox=dict(boxstyle="square", pad = 0.2, fc="w"))
            else:
                ax.annotate(catalysts[sample],(x[j]*100-x[j]*2.5, 10),ha='center',va = 'center', size = 10, bbox=dict(boxstyle="square", pad = 0.2, fc="w"))
            ax.annotate(element, (5,90), fontsize = 16, bbox=dict(boxstyle="square", fc="w"))
            j += 1

        ax.errorbar(x*100, y*100,label = element, yerr=yerror*100, fmt='o', 
                     color = c[element], markersize = 6, capsize = 5, mec ='k')
        
        
        ax = plot_settings(ax)
        
        pltF.global_savefig(fig, plt_title = plt_title , addcomment = element)
        
# _____________ Plot Ga_xPd_Y
        
        
        
        
    

def plot_rel_to_Ti(elements, catalysts, intended_composition,
                           measured_sample_composition, plt_title):  
    col = color_map()
    c = dict(zip(elements, col))
        
    for i,element in enumerate(elements):
        fig = plt.figure(figsize=(5,5))
        ax = fig.add_subplot(1,1,1)
        
        x = np.zeros(len(measured_sample_composition.keys()))
        y = np.zeros(len(measured_sample_composition.keys()))
        
        yerror = np.zeros(len(measured_sample_composition.keys()))
        
        j = 0
        x_tick_labels = []
        for sample in measured_sample_composition:
            #print('**********')
            
            x_tick_labels.append(catalysts[sample])
            y[j] = measured_sample_composition[sample][element][0]
            yerror[j] = measured_sample_composition[sample][element][1]
            #print(intended_composition[sample][element])
            x[j] = j+1 #intended_composition[sample][element]
            '''
            #element = 'Ga'
            #sample = '20190315 NP1 After CO pot shift'
            y_box = y[j]#measured_sample_composition[sample][element][0]
            x_box = intended_composition[sample][element]

            print(y_box,x_box)
            print(type(y_box))
            '''
            #ax.annotate(catalysts[sample],(x[j]*100-x[j]*2.5, y[j]*100-yerror[j]*200),ha='center', bbox=dict(boxstyle="square", fc="w"))
            #ax.annotate(catalysts[sample],(x[j]*100-x[j]*2.5, 10),ha='center',va = 'bottom', size = 10, bbox=dict(boxstyle="square", pad = 0.2, fc="w"))
            print(sample)
            if element == 'Ti' or 'O': 
                ax.annotate(catalysts[sample],(x[j]*100+10, y[j]*100),ha='center',va = 'center', size = 10, bbox=dict(boxstyle="square", pad = 0.2, fc="w"))
            else:
                ax.annotate(catalysts[sample],(x[j]*100-x[j]*2.5, 10),ha='center',va = 'center', size = 10, bbox=dict(boxstyle="square", pad = 0.2, fc="w"))
            ax.annotate(element, (5,90), fontsize = 16, bbox=dict(boxstyle="square", fc="w"))
            j += 1

        ax.errorbar(x, y*100,label = element, yerr=yerror*100, fmt='o', 
                     color = c[element], markersize = 6, capsize = 5, mec ='k')
        ax.x_tick_labels = ['Millipore'] 
        
        ax = plot_settings_rel_to_Ti(ax, element, x_tick_labels)
        #ax.set_title(plt_title + '\n')
        
        save_title = 'results_py/' + plt_title + ' ' + element
        #print(plt_title)
        fig.savefig(save_title,bbox_inches='tight', dpi=1000)
        

def plot_settings_rel_to_Ti(ax, element, x_tick_labels):

    #line = np.linspace(0, 100, 1000)
    #ax.plot(line,line, color = 'k', alpha = 0.4)
    #ax.set_xlabel('Intended Composition / %', fontsize = 16)
    ax.set_ylabel(element + ':Ti / at%', fontsize = 16)
    #ax.legend(fontsize =12, loc = 'lower right')
    ymin = 0
    ymax = 15
    ax.set_ylim([ymin,ymax])
    #ax.set_xlim([0,100])
    
    ha = 'right'
    t = np.arange(1,len(x_tick_labels)+1)
    ax.set_xticks(t)
    ax.set_xticklabels( x_tick_labels, rotation = 45, fontsize = 14, ha=ha)
    #ax.set_aspect('equal', adjustable='box')
    ax.grid(which='major', axis = 'y', color = 'k', alpha=0.4)
    major_ticks = np.arange(ymin, ymax+1, 5)
    ax.set_yticks(major_ticks)
    #ax.set_yticks(major_ticks)
    ax.tick_params(axis='both', which='major', labelsize=12)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    return ax
    
