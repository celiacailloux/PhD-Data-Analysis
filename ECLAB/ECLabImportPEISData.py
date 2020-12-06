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

class ECLabDataPEIS:
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
        self.data = {}

        #functions
        self.read_txt()            
        # self.convert_to_RHE()
        # self.create_SHE_column()
        # self.convert_to_current_density()
        self.create_timestamp_column()
        self.create_time_columns(self.time_start)
        
        
        #self.convert_to_SHE()
    ''' Read the txt file and save it in a pandas dataframe '''    
    def read_txt(self):
        self.file_paths = find_all_txt_files_containing_str(rootdir = self.file_folder, _str = '_PEIS_')
        for file_path in self.file_paths:
            #self.dataframe = pd.read_csv(self.path_d,delimiter="\t", names = names, header = 1, index_col=None)#header = 0)
            file_name = os.path.basename(file_path)
            df = pd.read_csv(file_path, 
                             delimiter = "\t", 
                             encoding = "ISO-8859-1",
                             header = 0,
                             index_col = None)            
            # self.data[file_name] = df#df.drop(df.index[[0]]).reset_index(drop = True)
            # print(df.iloc[0])
            self.data[file_name] = df.drop(df.index[[0]]).reset_index(drop = True)                        
            # print('Removed 1st row in {}'.format(file_name))            
            # print(self.data[file_name].iloc[0])
        
    ''' Returns the current as a current density '''  
    def convert_to_current_density(self):
        for file_name, data in self.data.items():
            #self.dataframe = self.dataframe
            #self.dataframe['<I>/mA'] = (self.dataframe['<I>/mA'].mul(self.uncompensated_R)).divide(self.A_electrode)
            data['I/mA'] = (data['I/mA']).divide(self.A_electrode)
      
        
    ''' convert the potential to vs RHE scale '''
    def convert_to_RHE(self): 
        # http://www.consultrsr.net/resources/ref/refpotls.htm                                         
        for file_name, data in self.data.items():
            if type(self.E_ref) is str:
                if self.E_ref == 'Ag/AgCl':      # Ag/AgCl in saturated KCl
                    self.E_ref = 0.197
                elif self.E_ref == 'Hg/Hg2SO4':
                    self.E_ref = 0.72
                else:
                    print('Unknown reference electrode')
            i = data['I/mA'].div(1000)                                  #mA to A
            print('que')
            if not self.R:
                R = data['Rcmp/Ohm'].mean()
                iR = (i.mul(R)).mul(1-self.uncompensated_R)
            E_compensated = data['Ewe/V'].sub(iR) # compensated means the electrolyte resistance has been accounted for
            data['Ewe/RHE'] = E_compensated.add(self.E_ref+0.059*self.pH)  
    
    ''' creates and extra column with the potential vs SHE '''
    def create_SHE_column(self):
        for file_name, data in self.data.items():
            #self.dataframe = self.dataframe.copy()
            data['Ewe/SHE'] = data['Ewe/V'].sub(0.059*self.pH)
            header = data.iloc[0]
            data.rename(columns = header)
    
    ''' Returns the time in min '''
    def create_timestamp_column(self):
        for file_name, data in self.data.items():
            #date_time_str = data['time/s']
            #date_time_obj = datetime.strptime(date_time_str, '%m-%d-%Y %H:%M:%S.%f')
            #print(date_time_obj)
            # data['time/timestamp'] = datetime.timestamp(data['time/s'])
            data['time/datetime'] = pd.to_datetime(data['time/s'])
            data['time/timestamp'] = data['time/datetime'].astype('int64') // 10**9
            
            file1 = list(self.data.keys())[0]
            self.time_start = self.data[file1]['time/timestamp'].iloc[0]            
            
    ''' Returns the time in min '''
    def create_time_columns(self, time_start):
        for file_name, data in self.data.items():
            data['time/h'] = data['time/timestamp'].sub(time_start).divide(3600)
            data['time/min'] = data['time/timestamp'].sub(time_start).divide(60)
    
    ''' Returns data in a potential range '''
    def get_dataframe_single_potential(self, potential, potential_scale = 'Ewe/V'):        
        #print(self.dataframe[potential_scale].between(potential-0.01, potential+0.01, inclusive=True))
        dataframe_potential_range = self.dataframe.loc[self.dataframe[potential_scale].between(potential-0.01, potential+0.01, inclusive=True)]

        return dataframe_potential_range
