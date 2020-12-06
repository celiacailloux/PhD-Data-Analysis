#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on September 2019

@author: celiacailloux

Updated on Sep 30 2019
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator


class GammyDataCV:
    def __init__(self,
                 exp_name, 
                 file_path, 
                 reference_electrode_potential,
                 label,
                 A_electrode,
                 curve2_line):
        
        #attributes
        self.file_path = file_path
        self.label = label
        self.exp_name = exp_name
        self.A_electrode = A_electrode 
        self.upperlimit = curve2_line #11251
        self.E_ref = reference_electrode_potential
        #functions


        self.read_txt()
        #self.get_Ar_cycle_end()
        #self.get_cycle_range()
        #self.convert_to_RHE()
        self.convert_to_voltage()
        self.convert_to_current_density()
        #self.convert_to_SHE()
    ''' Read the txt file and save it in a pandas dataframe '''    
    def read_txt(self):
        
        
        row_range = list(range(0,63))
        row_range[-1] = 63  
        print(row_range[-1], row_range[-2])                                                    #makes a list of the range of numbers, that should be skipped
        self.dataframe = pd.read_csv(self.file_path, delimiter="\t", 
                                     sep='delimiter', skiprows = row_range, 
                                     nrows = self.upperlimit, encoding = "ISO-8859-1")
        
        row_range = list(range(0,self.upperlimit+63+3))
        row_range[-1] = self.upperlimit+63+3
        print(row_range[-1], row_range[-2])
        self.dataframe_cycle2 = pd.read_csv(self.file_path, delimiter="\t", 
                                     sep='delimiter', skiprows = row_range, 
                                     nrows = int(self.upperlimit*2/3), encoding = "ISO-8859-1")
        
        
        
        self.units = pd.read_csv(self.file_path, delimiter = '\t', 
                                 sep = 'delimiter', skiprows = 63, 
                                 nrows = 0, index_col = None, encoding = 'ISO-8859-1')
        # error_bad_lines=False
        
       
    ''' Returns the current as a current density '''  
    def convert_to_current_density(self):
        self.dataframe['I/mAcm-2-cyc1'] = self.dataframe['Im'].divide(self.A_electrode).mul(1000)
        self.dataframe_cycle2['I/mAcm-2-cyc2'] = self.dataframe_cycle2['Im'].divide(self.A_electrode).mul(1000)
        #print(type(self.dataframe['Im'][0]))
        print(self.dataframe.columns.values)
        print(self.dataframe_cycle2.columns.values)
      
    ''' convert the potential to vs RHE scale '''
    def convert_to_RHE(self):                                                   # http://www.consultrsr.net/resources/ref/refpotls.htm
        if type(self.E_ref) is str:
            if self.E_ref == 'Ag/AgCl':      # Ag/AgCl in saturated KCl
                self.E_ref = 0.199
            elif self.E_ref == 'Hg/Hg2SO4':
                self.E_ref = 0.72
            else:
                print('Unknown reference electrode')
        i = self.dataframe['<I>/mA'].div(1000)                                  #mA to A
        iR = (i.mul(self.R)).mul(1-self.uncompensated_R)
        E_compensated = self.dataframe['Ewe/V'].sub(iR) # compensated means the electrolyte resistance has been accounted for
        self.dataframe['Ewe/V'] = E_compensated.add(self.E_ref+0.059*self.pH)  
    
    ''' creates and extra column with the potential vs SHE '''
    def convert_to_voltage(self):
        #self.dataframe = self.dataframe.copy()
        self.dataframe['Vf/VvsRef-cyc1'] = self.dataframe['Vf']
        self.dataframe_cycle2['Vf/VvsRef-cyc2'] = self.dataframe_cycle2['Vf']
        print(self.dataframe.columns.values)
        print(self.dataframe_cycle2.columns.values)
        #self.header = self.dataframe.iloc[0]
        #self.dataframe.rename(columns = self.header)


    