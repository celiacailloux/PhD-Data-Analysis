# -*- coding: utf-8 -*-
"""
Created on:             Thu Jun  4 06:54:38 2020

@author:                ceshuca

Updated:                June 2020
"""


import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator
from OSfunctions import find_all_txt_files_containing_str
from datetime import datetime

pd.set_option('display.max_columns', 5)

class ECLabDataZIR:
    def __init__(self, 
                 file_folder, 
                 pH, 
                 reference_electrode_potential,
                 label, 
                 A_electrode, 
                 uncompensated_R,
                 R = None):
        #attributes
        self.file_folder = file_folder
        self.pH = pH
        self.label = label
        self.exp_name = os.path.basename(self.file_folder)
        self.A_electrode = A_electrode 
        self.uncompensated_R = uncompensated_R
        self.R = R
        self.E_ref = reference_electrode_potential
        self.ZIR_data = {}

        #functions
        self.read_txt()            
        # self.convert_to_RHE()
        # self.create_SHE_column()
        # self.convert_to_current_density()
        self.create_timestamp_column()
        
        #self.convert_to_SHE()
    ''' Read the txt file and save it in a pandas dataframe '''    
    def read_txt(self):
        self.ZIR_file_paths = find_all_txt_files_containing_str(rootdir = self.file_folder, _str = 'ZIR')
        for ZIR_file_path in self.ZIR_file_paths:
            #self.dataframe = pd.read_csv(self.path_d,delimiter="\t", names = names, header = 1, index_col=None)#header = 0)
            file_name = os.path.basename(ZIR_file_path)
            df = pd.read_csv(ZIR_file_path, 
                             delimiter = "\t", 
                             encoding = "ISO-8859-1",
                             header = 0,
                             index_col = None)            
            self.ZIR_data[file_name] = df#df.drop(df.index[[0]])#.reset_index(drop = True)          
            
        
    ''' Returns the current as a current density '''  
    def convert_to_current_density(self):
        for file_name, ZIR_data in self.ZIR_data.items():
            #self.dataframe = self.dataframe
            #self.dataframe['<I>/mA'] = (self.dataframe['<I>/mA'].mul(self.uncompensated_R)).divide(self.A_electrode)
            ZIR_data['I/mA'] = (ZIR_data['I/mA']).divide(self.A_electrode)
      
        
    ''' convert the potential to vs RHE scale '''
    def convert_to_RHE(self): 
        # http://www.consultrsr.net/resources/ref/refpotls.htm                                         
        for file_name, ZIR_data in self.ZIR_data.items():
            if type(self.E_ref) is str:
                if self.E_ref == 'Ag/AgCl':      # Ag/AgCl in saturated KCl
                    self.E_ref = 0.197
                elif self.E_ref == 'Hg/Hg2SO4':
                    self.E_ref = 0.72
                else:
                    print('Unknown reference electrode')
            i = ZIR_data['I/mA'].div(1000)                                  #mA to A
            if not self.R:
                R = ZIR_data['Rcmp/Ohm'].mean()
                iR = (i.mul(R)).mul(1-self.uncompensated_R)
            E_compensated = ZIR_data['Ewe/V'].sub(iR) # compensated means the electrolyte resistance has been accounted for
            ZIR_data['Ewe/RHE'] = E_compensated.add(self.E_ref+0.059*self.pH)  
    
    ''' creates and extra column with the potential vs SHE '''
    def create_SHE_column(self):
        for file_name, ZIR_data in self.ZIR_data.items():
            #self.dataframe = self.dataframe.copy()
            ZIR_data['Ewe/SHE'] = ZIR_data['Ewe/V'].sub(0.059*self.pH)
            header = ZIR_data.iloc[0]
            ZIR_data.rename(columns = header)

    
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
    def create_timestamp_column(self):
        for file_name, ZIR_data in self.ZIR_data.items():
            #date_time_str = ZIR_data['time/s']
            #date_time_obj = datetime.strptime(date_time_str, '%m-%d-%Y %H:%M:%S.%f')
            #print(date_time_obj)
            # ZIR_data['time/timestamp'] = datetime.timestamp(ZIR_data['time/s'])
            ZIR_data['time/datetime'] = pd.to_datetime(ZIR_data['time/s'])
            ZIR_data['time/timestamp'] = ZIR_data['time/datetime'].astype('int64') // 10**9
            
    ''' Returns the time in min '''
    def create_time_columns(self, time_start):
        for file_name, ZIR_data in self.ZIR_data.items():
            ZIR_data['time/h'] = ZIR_data['time/timestamp'].sub(time_start).divide(3600)
            ZIR_data['time/min'] = ZIR_data['time/timestamp'].sub(time_start).divide(60)
    
    ''' Returns data in a potential range '''
    def get_dataframe_single_potential(self, potential, potential_scale = 'Ewe/V'):        
        #print(self.dataframe[potential_scale].between(potential-0.01, potential+0.01, inclusive=True))
        dataframe_potential_range = self.dataframe.loc[self.dataframe[potential_scale].between(potential-0.01, potential+0.01, inclusive=True)]

        return dataframe_potential_range
