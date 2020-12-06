#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created             Mon Mar 11 19:38:09 2019

@author:            celiacailloux

Updated             12 of  June 2020
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator
from OSfunctions import find_all_txt_files_containing_str
from datetime import datetime

pd.set_option('display.max_columns', 5)

class ECLabDataCA:
    def __init__(self, 
                 file_folder, 
                 pH, 
                 reference_electrode_potential,
                 label, 
                 A_electrode, 
                 uncompensated_R,
                 Ru = None):
        #attributes
        self.file_folder = file_folder
        self.pH = pH
        self.label = label
        self.exp_name = os.path.basename(self.file_folder)
        self.A_electrode = A_electrode 
        self.uncompensated_R = uncompensated_R
        self.Ru = Ru
        self.E_ref = reference_electrode_potential
        self.CA_data = {}

        #functions
        self.get_electrolyte()
        self.read_txt()
        self.convert_to_RHE()
        self.create_SHE_column()
        self.convert_to_current_density()
        self.create_timestamp_column()
        self.create_time_columns(self.time_start)
        self.check_if_loop_CA() # this function only checks it, does
                                # really do anything
        
        #self.convert_to_SHE()
    def get_electrolyte(self):
        if self.pH == 6.8:
            self.electrolyte = '0.1 M KHCO3'
        else:
            self.electrolyte = 'unknown'
    ''' Read the txt file and save it in a pandas dataframe '''    
    def read_txt(self):
        print('\n')
        self.CA_file_paths = \
            find_all_txt_files_containing_str(rootdir = self.file_folder, 
                                                               _str = 'CA_C')
        print('\n')
        for CA_file_path in self.CA_file_paths:
            #self.dataframe = pd.read_csv(self.path_d,delimiter="\t", names = names, header = 1, index_col=None)#header = 0)
            file_name = os.path.basename(CA_file_path)
            df = pd.read_csv(CA_file_path, 
                             delimiter="\t", 
                             encoding = "ISO-8859-1",  
                             index_col=None)
            try:
                if int(df['dQ/C'].iloc[0]) == 0:    
                    # self.CA_data[file_name] = df.drop(df.index[[0]])#.reset_index(drop = True)                        
                    # print('Removed 1st row in {}'.format(file_name))
                    self.CA_data[file_name] = df
                    print('Does not remove 1st row!')
                else:
                    self.CA_data[file_name] = df
            except IndexError:
                print('NB! \n{} probably does not contain data!'.format(file_name))
    ''' Returns the current as a current density '''  
    def convert_to_current_density(self):
        for file_name, CA_data in self.CA_data.items():
            
            'renames I/mA column if it is called <I>/mA' 
            if 'I/mA' not in CA_data:
                print('no I/mA')
                CA_data.rename(columns={'<I>/mA': 'I/mA'})            
            CA_data['I/mAcm-2'] = (CA_data['I/mA']).divide(self.A_electrode)
            # print(self.CA_data.columns[10])
        
    ''' convert the potential to vs RHE scale '''
    def convert_to_RHE(self): 
        # http://www.consultrsr.net/resources/ref/refpotls.htm
        print('\n')                                         
        for file_name, CA_data in self.CA_data.items():
            # determining the RE
            print('{}'.format(file_name))
            if type(self.E_ref) is str:
                if self.E_ref == 'Ag/AgCl':      # Ag/AgCl in saturated KCl
                    self.E_ref = 0.197
                elif self.E_ref == 'Hg/Hg2SO4':
                    self.E_ref = 0.72
                else:
                    print('Unknown reference electrode')
            i = CA_data['I/mA'].div(1000)                                  #mA to A
            # determining iR. Either using 1) a theoretical Ru, \
            # 2) compensated resistance (typically 85%) 
            
            if 'Rcmp/Ohm' in CA_data and CA_data['Rcmp/Ohm'].mean() != 0:
                CA_data['Ru/Ohm'] = \
                    CA_data['Rcmp/Ohm'].div(self.uncompensated_R).mul(100)   
                CA_data['iR/V'] = i*CA_data['Ru/Ohm']               
                # print(CA_data['iR/V'].mean())
                # iR = (i.mul(Ru)).mul(1-self.uncompensated_R)        
                CA_data['Ewe/VvsREF'] = CA_data['Ewe/V']-\
                    CA_data['iR/V'].mul((100-self.uncompensated_R)/100)                 # compensated means the electrolyte resistance has been accounted for
                CA_data['Ewe/RHE'] = CA_data['Ewe/VvsREF'].add(self.E_ref+0.059*self.pH)                 
                # print(CA_data['Ru/Ohm'].mean())
                
            elif 'Rcmp/Ohm' in CA_data and CA_data['Rcmp/Ohm'].mean() == 0:
                if self.Ru == None:
                    print('NB! \nNo uncompensated resistance Ru is given NOR determined!'\
                          ' Please calculate the average Ru')
                else:
                    print('NB! \Ru not determined by PEIS, ZIR nor CI: \n'\
                          '\'{}\', \nthus Ru = {} Ohm used \n'.format(file_name, self.Ru))
                    CA_data['Ru/Ohm'] = self.Ru
                    CA_data['iR/V'] = i.mul(self.Ru)  
                    # print('{:,.2f}'.format(CA_data['Ewe/V'].mean()))
                    # print('{:,.2f}'.format(CA_data['iR/V'].mean()))
                    CA_data['Ewe/VvsREF'] = CA_data['Ewe/V']-CA_data['iR/V']                 # compensated means the electrolyte resistance has been accounted for
                    # print('{:,.2f}'.format(CA_data['Ewe/VvsREF'].mean()))
                    CA_data['Ewe/RHE'] = CA_data['Ewe/VvsREF'].add(self.E_ref+0.059*self.pH)  
            elif 'Rcmp/Ohm' not in CA_data:
                print('No \'Rcmp/Ohm\' column found in {}'.format(file_name))
            else:
                print('Something wrong with Ru determination')
            #     # CA_data['Ns'
            
            # Ru = CA_data['Ru/Ohm'].mean()
            # if int(Ru) == 0:
            #     Ru = 56.2
            #     print('Ru not determined by PEIS, ZIR nor CI for '\
            #           '\'{}\', \nthus R = {} Ohm used'.format(file_name, Ru))                    
            #     iR = i.mul(Ru)
            # else:                         
            #     iR = (i.mul(Ru)).mul(1-self.uncompensated_R)                     #calculates the last 15 % of the uncompensated R            
            # # ---- 
            # if CA_loop:
            #     print('this is a loop CA measurment')
            # else:
            #     CA_data['Ewe/VvsREF'] = CA_data['Ewe/V'].sub(iR)                    # compensated means the electrolyte resistance has been accounted for
            #     CA_data['Ewe/RHE'] = CA_data['Ewe/VvsREF'].add(self.E_ref+0.059*self.pH)  
    def check_if_loop_CA(self):
        for file_name, CA_data in self.CA_data.items():
            # return the difference between each row. Since the first row will be Nan, it fills Nan to 0
            Ru_diff = CA_data['Ru/Ohm'].diff().fillna(0)
            CA_data['Ru difference/bool'] = Ru_diff != 0            
            
            # this mean that the Ru varies! Hence, its a loop with ZIR measurements!
            if len(CA_data['Ru difference/bool'].value_counts()) == 2: 
                df_idx_new_loop_start = CA_data.loc[CA_data['Ru difference/bool']]
                print('NB! \nBeware, found a looped CA \n({})'.format(file_name))
                idx_list = list(df_idx_new_loop_start.index.values)
                N_loops = len(idx_list)
                # fill Ns
                for idx_loop in np.arange(N_loops):
                    CA_data.loc[idx_list[idx_loop], 'Ns'] = idx_loop+1
                # 'Ns' contains the idx of loop (zero-indexed)
                # 'CA loop' gives the total number of loops
                CA_data['Ns'] = CA_data['Ns'].replace(to_replace=0, method='ffill')    
                CA_data['CA loop'] = CA_data['mode'].replace(to_replace=0, value = True)
                
                # CA_data.idx_loop_start = idx_list
                # self.idx_list = idx_list
            # else:
            #     CA_data.CA_loops = False    
                # print(CA_data.CA_loops)
                # print(CA.data.Ns)
                # print(CA_data['Ns'])
                
                
            
            
    def create_GC_timestamp_column(self, injection_time):
        ''' at some point I need to write a script that slices 
        that find the exact average between two GC injections. For the 
        time being, Ns slicing (hence is used) '''
        # injection_time is a HH:MM:S time stamp, eg. 05:52:0 (str)
        for file_name, CA_data in self.CA_data.items():
            # return the difference between each row. Since the first row will be Nan, it fills Nan to 0
            
            
            
            j = CA_data['I/mAcm-2']
            t = CA_data['time/datetime']
            
            # # find all j that have the same timestamp as GC
            # _bool = CA_data['time/datetime'].dt.time.astype(str).str.contains('|'.join(injection_time))
            # t_datetime = CA_data['time/datetime'][_bool]
            # j_injection = CA_data['I/mAcm-2'][_bool]

            
            # Ru_diff = CA_data['Ru/Ohm'].diff().fillna(0)
            # CA_data['Ru difference/bool'] = Ru_diff != 0            
            
            # # this mean that the Ru varies! Hence, its a loop with ZIR measurements!
            # if len(CA_data['Ru difference/bool'].value_counts()) == 2: 
            #     df_idx_new_loop_start = CA_data.loc[CA_data['Ru difference/bool']]
            #     print('NB! \nBeware, found a looped CA \n({})'.format(file_name))
            #     idx_list = list(df_idx_new_loop_start.index.values)
            #     N_loops = len(idx_list)
            #     for idx_loop in np.arange(N_loops):
            #         CA_data.loc[idx_list[idx_loop], 'Ns'] = idx_loop+1
            #     CA_data['Ns'] = CA_data['Ns'].replace(to_replace=0, method='ffill')    
            #     CA_data['CA loop'] = CA_data['mode'].replace(to_replace=0, value = True)
            #     # CA_data.CA_loops = True
            #     # CA_data.N_loops = N_loops
            #     # CA_data.idx_loop_start = idx_list
            #     # self.idx_list = idx_list
            # # else:
            # #     CA_data.CA_loops = False    
            # # print(CA_data.CA_loops)
            # print('\n')
          
    ''' creates and extra column with the potential vs SHE '''
    def create_SHE_column(self):
        for file_name, CA_data in self.CA_data.items():
            #self.dataframe = self.dataframe.copy()
            CA_data['Ewe/SHE'] = CA_data['Ewe/V'].sub(0.059*self.pH)
            header = CA_data.iloc[0]
            CA_data.rename(columns = header)

    ''' Returns the time in min '''
    def create_timestamp_column(self):
        for file_name, CA_data in self.CA_data.items():
            #date_time_str = CA_data['time/s']
            #date_time_obj = datetime.strptime(date_time_str, '%m-%d-%Y %H:%M:%S.%f')
            #print(date_time_obj)
            # CA_data['time/timestamp'] = datetime.timestamp(CA_data['time/s'])
            CA_data['time/datetime'] = pd.to_datetime(CA_data['time/s'])
            CA_data['time/timestamp'] = CA_data['time/datetime'].astype('int64') // 10**9
            # starts t = 0 at the time stamp of the first file!
            file1 = list(self.CA_data.keys())[0]
            self.time_start = self.CA_data[file1]['time/timestamp'].iloc[0]            
            
    def create_time_columns(self, time_start):
        for file_name, CA_data in self.CA_data.items():
            CA_data['time/h'] = CA_data['time/timestamp'].sub(time_start).divide(3600)
            CA_data['time/min'] = CA_data['time/timestamp'].sub(time_start).divide(60)
    
    ''' Returns data in a potential range '''
    def get_dataframe_single_potential(self, potential, potential_scale = 'Ewe/V'):        
        #print(self.dataframe[potential_scale].between(potential-0.01, potential+0.01, inclusive=True))
        dataframe_potential_range = self.dataframe.loc[self.dataframe[potential_scale].between(potential-0.01, potential+0.01, inclusive=True)]

        return dataframe_potential_range
