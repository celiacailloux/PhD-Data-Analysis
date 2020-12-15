#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 19:55:33 2019

@author: celiacailloux
"""

import pandas as pd
import os
import numpy as np

class EDSData:
    def __init__(self, exp):
        self.exp = exp
        self.sample = exp
        self.find_exp_txts()

        
    # This function reads the txt file and saves the columns using by the 
    # variable "names"
    def read_txt(self, sub_d, path_file):
        #self.dataframe = pd.read_csv(self.path_d,delimiter="\t", names = names, header = 1, index_col=None)#header = 0)
        dataframe = pd.read_csv(path_file,delimiter="\t", index_col=None)
        header = dataframe.iloc[0]
        dataframe.rename(columns = header)
        dataframe.name = dataframe.columns[0]
        dataframe.rename(columns={dataframe.name:'Element'}, inplace=True)
        if dataframe.empty:
            print('dataframe: {} is empty'.format(dataframe.name))
        #print(dataframe)
        return dataframe
        
        
    def find_exp_txts(self):
        # find subdirectories
        subdirectories = next(os.walk('.'))[1]

        # iterates over all sub_directories to find subsubdirectories
        for sub_d in subdirectories:
            #print(sub_d)
            if sub_d == self.sample:
                self.txts = []
                print('********* The following txt files were found in subfolder {} and saved:'.format(sub_d))
                for file in os.listdir(sub_d):
                    #print(sub_d)
                    if file.endswith(".txt"):
                        path_file = os.path.join(sub_d,file)
                        print('File: {} in subfolder: {}'.format(file, sub_d))
                        #print('******* Returned sub directory: \'{0}\' and path: \'{1}\' for experiment: \'{2}\''.format(sub_d, path_file, self.exp))
                        #print(self.read_txt(sub_d, path_file))
                        self.txts.append(self.read_txt(sub_d, path_file))  
                        
    def get_sample_composition(self,elements):

        self.sample_composition = {}
        multiple = {}
        #print(self.txts)
        
        for i, dataframe in enumerate(self.txts):
#            #temp = data.loc[data['Element'].isin()]
            atomic_composition = {}
            for j, element in enumerate(elements):
                
                #some_value = 'Ga'
                row = dataframe.loc[dataframe['Element'] == element]
                #print(row)
                if not row.empty:                    
                    atomic_perc = row.iat[0,1]
                    atomic_composition[element] = atomic_perc
                else: 
                    print('Data: {0} is empty: {1}'.format(dataframe.name,row.empty))
                    
            print('Atomic    composition: {}'.format(atomic_composition))
            rel_atomic_composition = self.compute_relative_atomic_composition(atomic_composition)
            multiple[dataframe.name] = rel_atomic_composition
        
        self.sample_composition[self.exp] = self.compute_avg_std(multiple,elements)

        print('********* Done with sample composition *******')

            
    def compute_relative_atomic_composition(self,atomic_composition):
        tot_perc = sum(atomic_composition.values())
        
        for element, atomic_perc in atomic_composition.items():
            atomic_composition[element] = round(atomic_perc/tot_perc,2)
        '''
        mol_composition = {}                          
        mol_composition['Ga'] = atomic_composition['Ga']/69.723  
        mol_composition['Pd'] = atomic_composition['Pd']/106.42 
        
        tot_mol = sum(mol_composition.values())
        
        for element, atomic_perc in mol_composition.items():
            mol_composition[element] = atomic_perc/tot_mol
        '''
        print('Relative composition: {}'.format(atomic_composition))
        return atomic_composition
        #return mol_composition 
    
    def compute_avg_std(self, multiple, elements):  
        avg_std = {}
        for element in elements:
    
            pr_element = np.array([d[element] for d in multiple.values()])
            avg = round(np.mean(pr_element),5)
            std = round(np.std(pr_element),5)
            avg_std[element] = [avg,std]
            #print(avg,std)
        #    for n, atomic_composition in multiple_EDXS.items():
        #        print(atomic_composition)
        #print(avg_std)
        print('\n')
        print('Average and standard: {}'.format(avg_std))
        return avg_std
    
    def get_rel_to_Ti_composition(self,elements):
        self.rel_to_Ti_composition = {}
        multiple = {}
        #print(self.txts)
        for i, dataframe in enumerate(self.txts):
            
#            #temp = data.loc[data['Element'].isin()]

            atomic_composition = {}
            row_Ti = dataframe.loc[dataframe['Element'] == 'Ti']
            if not row_Ti.empty:                    
                atomic_perc_Ti = row_Ti.iat[0,1]
            else: 
                print('Data: {0} is empty: {1}'.format(dataframe.name,row_Ti.empty))
            
            for j, element in enumerate(elements):
                
                #some_value = 'Ga'
                row = dataframe.loc[dataframe['Element'] == element]

                if not row.empty:                    
                    atomic_perc = row.iat[0,1]
                    atomic_composition[element] = atomic_perc
                    
                else: 
                    print('Data: {0} is empty: {1}'.format(dataframe.name,row.empty))
                
                #print('{},{}'.format(atomic_composition[element], atomic_composition['Ti']))
                tot_perc = sum([atomic_composition[element], atomic_perc_Ti])
                print('Ti (%): {0}, {1} (%): {2}'.format(atomic_perc_Ti, element, atomic_composition[element]))
                
                atomic_composition[element] = atomic_composition[element]/tot_perc
#                
            #print('atomic composition: {}'.format(atomic_composition))
            #print(dataframe.name)

            multiple[dataframe.name] = atomic_composition
        
        #print('multiple:{}'.format(multiple))
        self.rel_to_Ti_composition[self.exp] = self.compute_avg_std(multiple,elements)
        print('********* Done with sample composition *******')
        #print(self.rel_to_Ti_composition)    
