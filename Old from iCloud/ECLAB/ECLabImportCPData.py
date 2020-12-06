#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 19:38:09 2019

@author: celiacailloux

Updated on Wed Jul 3          2019
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator
      

class ECLabDataCP:
    def __init__(self, 
                 file_path, 
                 pH, 
                 reference_electrode_potential,
                 exp_name, 
                 A_electrode):
        #attributes

        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)
        self.pH = pH
        self.exp_name = exp_name
        self.A_electrode = A_electrode 
        self.E_ref = reference_electrode_potential
        #functions
        self.read_txt()
        self.create_min_column()
        self.convert_to_RHE()
        self.create_SHE_column()
        self.convert_to_current_density()
        
    ''' Read the txt file and save it in a pandas dataframe '''    
    def read_txt(self):
        #self.dataframe = pd.read_csv(self.path_d,delimiter="\t", names = names, header = 1, index_col=None)#header = 0)
        self.dataframe = pd.read_csv(self.file_path,delimiter="\t", index_col=None)
        self.dataframe.name = self.exp_name
 
        
    ''' Returns the current as a current density '''  
    def convert_to_current_density(self):
        #self.dataframe = self.dataframe
        if 'I/mA' in self.dataframe.columns:  
            self.dataframe['I/mA'] = self.dataframe['I/mA'].divide(self.A_electrode)
        
    ''' Returns the time in min '''
    def create_min_column(self):
        self.dataframe['time/min'] = self.dataframe['time/s'].divide(60)

      
    ''' convert the potential to vs RHE scale '''
    def convert_to_RHE(self):                                                  # http://www.consultrsr.net/resources/ref/refpotls.htm
      
        if type(self.E_ref) is str:
            if self.E_ref == 'Ag/AgCl':      # Ag/AgCl in saturated KCl
                self.E_ref = 0.199
            elif self.E_ref == 'Hg/Hg2SO4':
                self.E_ref = 0.72
            else:
                print('Unknown reference electrode')

        if 'I/mA' in self.dataframe.columns: #only OCV doesn't have 'I/mA'
            self.dataframe['Ewe/V'] = self.dataframe['Ewe/V'].add(self.E_ref+0.059*self.pH)
            if 'Rcmp/Ohm' in self.dataframe:
                R = self.dataframe['Rcmp/Ohm'].mean()
     
            else:
                R = 70  
            I = self.dataframe['I/mA'].mean()*0.001 # From mA to A
            #self.potential['Ewe/V'] = self.potential['Ewe/V'].add(I*R) 
            self.dataframe['Ewe/V'] = self.dataframe['Ewe/V'].sub(I*R)
        else:
            self.dataframe['Ewe/V'] = self.dataframe['Ewe/V'].add(0.059*self.pH)
        
    
    ''' creates and extra column with the potential vs SHE '''
    def create_SHE_column(self):
        #already iR-corrected
        #self.dataframe = self.dataframe.copy()

        self.dataframe['Ewe/SHE'] = self.dataframe['Ewe/V'].sub(0.059*self.pH)
        self.header = self.dataframe.iloc[0]
        self.dataframe.rename(columns = self.header)

        

