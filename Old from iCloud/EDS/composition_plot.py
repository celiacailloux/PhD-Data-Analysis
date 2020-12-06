#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 23:07:45 2019

@author: celiacailloux
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

def read_txt(path):
    dataframe = pd.read_csv(path,delimiter="\t", names = ['Element', 'Atomic %'], header = 0)#header = 0)

    return dataframe

def collect_all_txt():
    EDXS = {}
    
    subdirectories = next(os.walk('.'))[1]
    print('Choose samples from the follwing list!')
    for sub_d in subdirectories:
        print('      ' + sub_d)
        txt = []
        for file in os.listdir(sub_d):
            if file.endswith(".txt"):
                #print(file)
                data = read_txt(os.path.join(sub_d,file))
                txt.append(data)
                #print(file)
                #print()
        EDXS[sub_d] = txt
    return EDXS

def compute_sample_composition(data, elements):
    sample_composition = {}
    multiple_EDXS = {}

    for sample, EDXS_results in data.items(): 
        #print(len(EDXS_results))
        
        
        #print(sample)
        #i_results = range(len(EDXS_results))
        #= np.zeros(len(EDXS_results))
        for i, dataframe in enumerate(EDXS_results):
            
#            #temp = data.loc[data['Element'].isin()]
            atomic_composition = {}
            for j, element in enumerate(elements):
                print('HERE')
                #some_value = 'Ga'
                row = dataframe.loc[dataframe['Element'] == element]
                if not row.empty:
                    
                    print('sample: {}'.format(sample))
                    print(row)
                    atomic_perc = row.iat[0,1]
                    #print(element,atomic_perc)
                    
                    atomic_composition[element] = atomic_perc#at_listcl
                    #print(atomic_composition)   # flere elementer
                else: 
                    print('Data: {0} is empty: {1}'.format(sample,row.empty))
                
            rel_atomic_composition = compute_relative_atomic_composition(atomic_composition)
            multiple_EDXS[i] = rel_atomic_composition          

        #print('****************')
        #print(multiple_EDXS)
        sample_composition[sample] = compute_avg_std(multiple_EDXS,elements)  

    return sample_composition

def compute_relative_atomic_composition(atomic_composition):
    tot_perc = sum(atomic_composition.values())
    for element, atomic_perc in atomic_composition.items():
        atomic_composition[element] = atomic_perc/tot_perc
    
    #print(atomic_composition)
    return atomic_composition

def compute_avg_std(multiple_EDXS, elements):  
    avg_std = {}
    for element in elements:

        #print(element)
        #print(multiple_EDXS.values())
        
        pr_element = np.array([d[element] for d in multiple_EDXS.values()])
        avg = np.mean(pr_element)
        std = np.std(pr_element)
        avg_std[element] = [avg,std]
    #    for n, atomic_composition in multiple_EDXS.items():
    #        print(atomic_composition)
    #print(avg_std)
    return avg_std
        

def plot_samples_of_choice(samples_of_choice,elements, intended_composition,
                           measured_sample_composition, plt_title):   
    c = dict.fromkeys(elements, 0)
    col = ['b', 'g','r','c','m','y','k']
    col = col[:len(elements)]
    c = dict(zip(elements, col))
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    major_ticks = np.arange(0, 101, 25)
    minor_ticks = np.arange(0, 101, 10)
    
    for i,element in enumerate(elements):
        x = np.zeros(len(measured_sample_composition.keys()))
        y = np.zeros(len(measured_sample_composition.keys()))
        yerror = np.zeros(len(measured_sample_composition.keys()))
        j = 0
        for sample in measured_sample_composition:
            if sample in samples_of_choice:
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

def main():
    
    data = collect_all_txt()       
    
    elements = ['Ga', 'Pd']
    
    measured_sample_composition = compute_sample_composition(data, elements)
    
    print(measured_sample_composition)
    
    samples_of_choice = ['NP1', 'NP2', 'NP3']
    compositions = [{'Ga':1/3, 'Pd':2/3}, {'Ga':1/2, 'Pd':1/2}, {'Ga':2/3, 'Pd':1/3}]
    intended_composition = dict.fromkeys(samples_of_choice, 0)
    intended_composition = dict(zip(samples_of_choice, compositions))
    
    plt_title = 'NP1to3_untreated'
    plot_samples_of_choice(samples_of_choice,elements,intended_composition,
                           measured_sample_composition, plt_title)
    

    
    


if __name__ == '__main__':
    main()


# to be continued!