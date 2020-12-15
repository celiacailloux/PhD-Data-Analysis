#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 19:59:15 2019

@author: celiacailloux
"""
from EDSData import EDSData
import matplotlib.pyplot as plt
import numpy as np


def plot_samples_of_choice(elements, intended_composition,
                           measured_sample_composition, plt_title):   
    c = dict.fromkeys(elements, 0)
    col = ['b', 'g','r','c','m','y','k']
    col = col[:len(elements)]
    c = dict(zip(elements, col))
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    major_ticks = np.arange(0, 101, 25)
    #minor_ticks = np.arange(0, 101, 10)
    
    for i,element in enumerate(elements):
        x = np.zeros(len(measured_sample_composition.keys()))
        y = np.zeros(len(measured_sample_composition.keys()))
        yerror = np.zeros(len(measured_sample_composition.keys()))
        j = 0
        for sample in measured_sample_composition:
            print('**********')
            print(sample)
            #print(element)
            #print(measured_sample_composition[sample][element][0])
            y[j] = measured_sample_composition[sample][element][0]
            yerror[j] = measured_sample_composition[sample][element][1]
            #print(intended_composition[sample][element])
            x[j] = intended_composition[sample][element]
            j += 1
        #print('********')
        #print(x)
        #print(y)
        #print(yerror)
        #plt.scatter(x,y, label = element, color = c[element])
        
        ax.errorbar(x*100, y*100,label = element, yerr=yerror*100, fmt='o', 
                     color = c[element], markersize = 6, capsize = 5, mec ='k')
    line = np.linspace(0, 100, 1000)
    ax.plot(line,line, color = 'k', alpha = 0.4)
    ax.set_xlabel('Intended Composition / %', fontsize = 16)
    ax.set_ylabel('Measured Composition / %', fontsize = 16)
    ax.set_title(plt_title + '\n')
    ax.legend(fontsize =12, loc = 'lower right')
    ax.set_ylim([0,100])
    ax.set_xlim([0,100])
    ax.set_aspect('equal', adjustable='box')
    ax.grid(which='major', color = 'k', alpha=0.4)
    ax.set_xticks(major_ticks)
    ax.set_yticks(major_ticks)
    ax.tick_params(axis='both', which='major', labelsize=12)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
    plt.show()
    #ax.spines['top'](linewidth = 0.5)

#    plt.ylim([0,1])
#    plt.xlim([0,1])
#
#    #plt.axis('scaled')
#    plt.gca().set_aspect('equal', adjustable='box')
#    plt.grid(True, axis = 'y')
#    
        #plt.ylim(ymin=0)
    plt_title = 'Graphs_py/' + plt_title 
    
    fig.savefig(plt_title,bbox_inches='tight', dpi=1000)




#_____________ Step 1: Choose experiment_______________________________________

# Key is name of subsub directory. Value is true if RDE has been used and False
# if the flow cell has been used, and the number is the cycle where the gas was 
# switched to CO
all_experiments = {'NP1':0, 'NP2':0}

#KHO3
# Cu #1 trial 2, last Ar 39, CO start at 40

#chosen_exp = {k: v for k, v in all_experiments.items() if k in choice_of_exp}

elements = ['Ga', 'Pd']

#_____________ Step 2: Make classes____________________________________________

NP1 = EDSData(exp = '20190315 NP1 After CO pot shift')
NP1.get_sample_composition(elements)
NP1.sample_composition

print('\n')


NP2 = EDSData(exp = '20190315 NP2 After CO pot shift')
NP2.get_sample_composition(elements)
NP2.sample_composition

print('\n')


NP3 = EDSData(exp = '20190315 NP3 After CO pot shift 20kV')
NP3.get_sample_composition(elements)
NP3.sample_composition

print('\n')

all_sample_compositions = NP1.sample_composition
all_sample_compositions.update(NP2.sample_composition)
all_sample_compositions.update(NP3.sample_composition)


print(all_sample_compositions)

measured_sample_composition = all_sample_compositions
#_____________ Step 3: Intended values_________________________________________

#samples_of_choice = ['NP1', 'NP2', 'NP3']
samples_of_choice = ['20190315 NP1 After CO pot shift', '20190315 NP2 After CO pot shift', '20190315 NP3 After CO pot shift 20kV']
compositions = [{'Ga':1/3, 'Pd':2/3}, {'Ga':1/2, 'Pd':1/2}, {'Ga':2/3, 'Pd':1/3}]
intended_composition = dict.fromkeys(samples_of_choice, 0)
intended_composition = dict(zip(samples_of_choice, compositions))

#_____________ Step 3: Make plot_______________________________________________

plt_title = 'NP1to3_after'
plot_samples_of_choice(elements,intended_composition,
                       measured_sample_composition, plt_title)