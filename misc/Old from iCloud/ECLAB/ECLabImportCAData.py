#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 19:38:09 2019

@author: celiacailloux

Updated on Jul 12          2019
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator

class ECLabDataCA:
    def __init__(self, 
                 file_path, 
                 pH, 
                 reference_electrode_potential,
                 label,
                 exp_name, 
                 A_electrode, 
                 uncompensated_R,
                 R):
        #attributes
        self.file_path = file_path
        self.pH = pH
        self.label = label
        self.exp_name = exp_name
        self.A_electrode = A_electrode 
        self.uncompensated_R = uncompensated_R
        self.R = R
        self.E_ref = reference_electrode_potential

        #functions
        self.read_txt()
        self.convert_to_RHE()
        self.create_SHE_column()
        self.convert_to_current_density()
        self.create_min_column()
        #self.convert_to_SHE()
    ''' Read the txt file and save it in a pandas dataframe '''    
    def read_txt(self):
        #self.dataframe = pd.read_csv(self.path_d,delimiter="\t", names = names, header = 1, index_col=None)#header = 0)
        self.dataframe = pd.read_csv(self.file_path, delimiter="\t", encoding = "ISO-8859-1",  index_col=None)
        self.dataframe.name = self.exp_name
    
        
    ''' Returns the current as a current density '''  
    def convert_to_current_density(self):
        #self.dataframe = self.dataframe
        #self.dataframe['<I>/mA'] = (self.dataframe['<I>/mA'].mul(self.uncompensated_R)).divide(self.A_electrode)
        self.dataframe['I/mA'] = (self.dataframe['I/mA']).divide(self.A_electrode)
      
    ''' convert the potential to vs RHE scale '''
    def convert_to_RHE(self):                                                   # http://www.consultrsr.net/resources/ref/refpotls.htm
        if type(self.E_ref) is str:
            if self.E_ref == 'Ag/AgCl':      # Ag/AgCl in saturated KCl
                self.E_ref = 0.199
            elif self.E_ref == 'Hg/Hg2SO4':
                self.E_ref = 0.72
            else:
                print('Unknown reference electrode')
        i = self.dataframe['I/mA'].div(1000)                                  #mA to A
        iR = (i.mul(self.R)).mul(1-self.uncompensated_R)
        E_compensated = self.dataframe['Ewe/V'].sub(iR) # compensated means the electrolyte resistance has been accounted for
        self.dataframe['Ewe/V'] = E_compensated.add(self.E_ref+0.059*self.pH)  
    
    ''' creates and extra column with the potential vs SHE '''
    def create_SHE_column(self):
        #self.dataframe = self.dataframe.copy()
        self.dataframe['Ewe/SHE'] = self.dataframe['Ewe/V'].sub(0.059*self.pH)
        self.header = self.dataframe.iloc[0]
        self.dataframe.rename(columns = self.header)

    
#    ''' Returns the Ar cycles only '''
#    def get_dataframe_Ar_cyc_range(self):
#        cyc_i = self.dataframe['cycle number'].min()     
#        cyc_f = self.Ar_cycle_end
#        cyc_range = np.arange(cyc_i,cyc_f+1)
#        dataframe_cyc_range = self.dataframe.loc[self.dataframe['cycle number'].isin(cyc_range)]
#        return dataframe_cyc_range
    
#        ''' Returns the CO cycles only '''
#    def get_dataframe_CO_cyc_range(self):
#        cyc_i = self.CO_cycle_start
#        cyc_f = self.dataframe['cycle number'].max() 
#        cyc_range = np.arange(cyc_i,cyc_f+1)
#        dataframe_cyc_range = self.dataframe.loc[self.dataframe['cycle number'].isin(cyc_range)]
#        return dataframe_cyc_range
        
    ''' Returns the time in min '''
    def create_min_column(self):
        self.dataframe['time/min'] = self.dataframe['time/s'].divide(60)
    
    ''' Returns data in a potential range '''
    def get_dataframe_single_potential(self, potential, potential_scale = 'Ewe/V'):        
        #print(self.dataframe[potential_scale].between(potential-0.01, potential+0.01, inclusive=True))
        dataframe_potential_range = self.dataframe.loc[self.dataframe[potential_scale].between(potential-0.01, potential+0.01, inclusive=True)]

        return dataframe_potential_range
