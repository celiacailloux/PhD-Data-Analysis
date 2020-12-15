#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 19:38:09 2019

@author: celiacailloux
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator



# Convert the current (mA) to current density (mA/cm2) by the surface area
# of the rotating ring disc electrode (electrolyte) and also accounts for the 15 % extra
# in the resistance
def convert_current_density(current, electrolyte):
    if electrolyte == 'RDE':
        A = 0.196 #cm2
    elif electrolyte == 'KOH' or 'KHCO3':
        A = 1 #cm2 
    current = current.copy()
    current['<I>/mA'] = (current['<I>/mA'].mul(17/20)).divide(A)
    
    return current

# Converts the potential to V vs. RHE. 
# Depends on the reference electrode used!
def convert_RHE(voltage, electrolyte):
    # note that the electrolyte measurements are with KOH!
    if electrolyte == 'RDE':
        pH = 13
        E_ref =0.72
    elif electrolyte == 'KOH':
        pH = 13
        E_ref = 0.21
    elif 'KHCO3' in electrolyte:#electrolyte == 'KHCO3':
        pH = 10                                                                #http://www.aqion.de/site/191
        E_ref = 0#0.199                                                          # Ag/AgCl in saturated KCl
    voltage = voltage.copy()
    voltage['Ewe/V'] = voltage['Ewe/V'].add(E_ref+0.059*pH)      
    return voltage   

def convert_time(time):

    time = time.copy()
    time['time/s'] = time['time/s'].divide(60)
    
    return time

# This function returns the intercept of the measured potential (V vs. RHE)
# and 5 mA/cm2. The input is single cycle. 
def get_intercept(potential_cycle, current_cycle):
    j = [-5.5, -4.5]                                                            # current density where the CO shift is measured
    df = current_cycle
    df_next = df.loc[(df['<I>/mA'] >= j[0]) & (df['<I>/mA'] <= j[1])]
    if not df_next.empty:
        while len(df_next) >= 2:#not df_next.empty and len(df_next) >= 2:   
    
            df = df_next#df.loc[(df['<I>/mA'] >= j[0]) & (df['<I>/mA'] <= j[1])]
            j[0] +=0.005
            j[1] -=0.005
            df_next = df.loc[(df['<I>/mA'] >= j[0]) & (df['<I>/mA'] <= j[1])]
        
        df_pot = potential_cycle
        idx = df.index.values
    
    
        shift_point = df_pot[df_pot.index.isin(idx)]
        #print('Number of points intercepting with 5 mA/cm2: {}'.format(len(shift_point)))

        std = shift_point['Ewe/V'].std()
    
        if np.isnan(std):
            std = 0
        shift_point = shift_point['Ewe/V'].mean()
        intercept = shift_point
        
    else:
        intercept = []
        std = []
    return np.array([intercept, std])

def compute_CO_pot_shift(Ar_intercept, CO_intercept):
    shift = (Ar_intercept[0]-CO_intercept[0])*1000                              #convert from V to mV
    std = np.sqrt(np.power(CO_intercept[1],2))*1000
    #std = np.sqrt(np.power(Ar_intercept[1],2)+np.power(CO_intercept[1],2))*1000
    #print('Standard deviation: {} mV'.format(std))
    
    return np.array([shift,std])

''' ________________________  New ones_____________'''
class ECLabDataCVNew:
    def __init__(self, subsub_d, path_file, exp_details):
        self.subsub_d = subsub_d
        self.path_file = path_file
        self.exp_details = exp_details
        self.electrolyte = exp_details['Electrolyte']
        self.exp_type = exp_details['Experiment type']
        self.membrane = exp_details['Membrane']
        self.CO_cycle_start = exp_details['CO cycle start']
        self.name = subsub_d

        #self.dataframe = None
        self.read_txt()
        self.dataframe_name = self.dataframe.name
        #self.get_Ar_cycle_end()
        self.get_cycle_range()
        self.get_current()
        self.get_potential()





        # make a function that return the text file
        # for file in...
        # return what-comes-after "/" in path_d
        
        
    # This function reads the txt file and saves the columns using by the 
    # variable "names"
    def get_Ar_cycle_end(self):
        if self.CO_cycle_start != 0.0:
            self.Ar_cycle_end = self.CO_cycle_start-1
        else:
            #df_cycles = self.dataframe[['cycle number']]
            #self.cycle_start = df_cycles.iloc[0]['cycle number']
            self.Ar_cycle_end =  self.dataframe.iloc[-1]['cycle number']           
            
    def read_txt(self):
        #self.dataframe = pd.read_csv(self.path_d,delimiter="\t", names = names, header = 1, index_col=None)#header = 0)
        self.dataframe = pd.read_csv(self.path_file,delimiter="\t", index_col=None)
        self.header = self.dataframe.iloc[0]
        self.dataframe.rename(columns = self.header)
        self.dataframe.name = self.subsub_d
    
    def get_current(self):
        self.current = convert_current_density(self.dataframe[['<I>/mA','cycle number']], electrolyte = self.electrolyte)
        
    def get_potential(self):
        self.potential = convert_RHE(self.dataframe[['Ewe/V','cycle number']], electrolyte = self.electrolyte)
        
    #return the cycle range
    def get_cycle_range(self):
        df_cycles = self.dataframe[['cycle number']]
        self.cycle_start = df_cycles.iloc[0]['cycle number']
        self.cycle_end = df_cycles.iloc[-1]['cycle number']
        #self.cycle_range = [self.cycle_start, cycle_end]

    # This function returns the current in a specific cycle range. Eg. cycle 21
    # to cycle 24
    def get_current_cyc_range(self, cyc_i = None, cyc_f = None):
        if cyc_i is None:
            cyc_i = self.CO_cycle_start
        if cyc_f is None:
            cyc_f = self.cycle_end
        cyc_range = np.arange(cyc_i,cyc_f+1, 1)#list(range(cyc_i,cyc_f+1))
        df_cyc_range = self.dataframe_cyc_range(cyc_range)

        current_cyc_range = df_cyc_range[['<I>/mA','cycle number']]
        current_cyc_range = convert_current_density(current_cyc_range, electrolyte = self.electrolyte)
        return current_cyc_range

    # This function return the potential in a specific cycle range. Eg. cycle 21 
    # to cycle 24. 
    def get_potential_cyc_range(self, cyc_i = None, cyc_f = None):
        if cyc_i is None:
            cyc_i = self.CO_cycle_start
        if cyc_f is None:
            cyc_f = self.cycle_end
        cyc_range = np.arange(cyc_i,cyc_f+1, 1)#list(range(cyc_i,cyc_f+1))
        
        df_cyc_range = self.dataframe_cyc_range(cyc_range)
        #print(df_cyc_range[['cycle number']])
        
        potential_cyc_range = df_cyc_range[['Ewe/V','cycle number']]
        potential_cyc_range = convert_RHE(potential_cyc_range, electrolyte = self.electrolyte)
        
        return potential_cyc_range
    
    # This function extracts the data from the entire dataframe (EC lab data)
    # in a specific cycle range    
    def dataframe_cyc_range(self, cyc_range):
        return self.dataframe.loc[self.dataframe['cycle number'].isin(cyc_range)]
    
    # This function returns a dataframe containing three columns: 'cycle number', 'potential shift'
    # and 'standard deviation'
    def get_potential_shift(self, cyc_i = None, cyc_f = None):
        if cyc_i is None:
            cyc_i = self.CO_cycle_start
        if cyc_f is None:
            cyc_f = self.cycle_end
        Ar_potential = self.get_potential_cyc_range(self.Ar_cycle_end, self.Ar_cycle_end)
        Ar_current = self.get_current_cyc_range(self.Ar_cycle_end, self.Ar_cycle_end)
        Ar_intercept = get_intercept(Ar_potential, Ar_current)
        #print(Ar_intercept)
        print('Ar start: {0} \n cyc_start: {1} \n CO_cycle_start: {2}'.format(self.Ar_cycle_end,cyc_i,self.CO_cycle_start ))
        
        cyc_range = np.arange(cyc_i, cyc_f+1)
        potential_shift = []
        potential_shift_std = []
        intercepts = []
        
        
        for cycle in cyc_range:
            CO_potential_cycle = self.get_potential_cyc_range(cycle, cycle)
            CO_current_cycle = self.get_current_cyc_range(cycle, cycle)
            
            CO_intercept = get_intercept(CO_potential_cycle, CO_current_cycle)
            if CO_intercept.size != 0:
                #print('Cycle:{0}, shift: {1}'.format(cycle, CO_intercept))
                intercepts.append(CO_intercept[0])
                
                potential_shift_cycle = compute_CO_pot_shift(Ar_intercept, CO_intercept)
                potential_shift.append(potential_shift_cycle[0])
                potential_shift_std.append(potential_shift_cycle[1])
                
            else:
                intercepts.append(None)
                potential_shift.append(None)
                potential_shift_std.append(None)
            
        
        d = {'cycles': cyc_range, 'potential shift (mV)': potential_shift, 'std (mV)': potential_shift_std, 'CO intercept': intercepts}
        df = pd.DataFrame(data=d)
        return df
        
# ________________CP class_____________________________________________________________
class ECLabDataCPNew:
    def __init__(self, subsub_d, path_file, exp_details):
        self.subsub_d = subsub_d
        self.path_file = path_file
        self.exp_details = exp_details
        self.electrolyte = exp_details['Electrolyte']
        self.exp_type = exp_details['Experiment type']
        self.membrane = exp_details['Membrane']
        self.CO_time_start = exp_details['CO cycle start']
        self.name = subsub_d

        self.read_txt()
        self.get_potential()
       
    def read_txt(self):
        #self.dataframe = pd.read_csv(self.path_d,delimiter="\t", names = names, header = 1, index_col=None)#header = 0)
        self.dataframe = pd.read_csv(self.path_file,delimiter="\t", index_col=None)
        self.header = self.dataframe.iloc[0]
        self.dataframe.rename(columns = self.header)
        self.dataframe.name = self.subsub_d
           
    def get_potential(self):
        self.potential = convert_RHE(self.dataframe[['Ewe/V','time/s']], electrolyte = self.electrolyte)
        self.potential = self.potential.copy()
        if 'CP' in self.path_file:
            if 'Rcmp/Ohm' in self.dataframe:
                R = self.dataframe['Rcmp/Ohm'].mean()
 
            else:
                R = 70  
            I = self.dataframe['I/mA'].mean()*0.001 # From mA to A
            #self.potential['Ewe/V'] = self.potential['Ewe/V'].add(I*R) 
            self.potential['Ewe/V'] = self.potential['Ewe/V'].sub(I*R)
                
        self.potential = convert_time(self.potential)


'''___________________ OLD ones ______________'''

class ECLabDataCV:
    def __init__(self, subsub_d, path_file, exp_details):
        self.subsub_d = subsub_d
        self.path_file = path_file
        self.exp_details = exp_details
        self.electrolyte = exp_details[0]
        self.exp_type = exp_details[2]
        self.membrane = exp_details[3]
        self.CO_cycle_start = exp_details[4]
        self.name = subsub_d

        #self.dataframe = None
        self.read_txt()
        self.dataframe_name = self.dataframe.name
        self.get_Ar_cycle_end()
        self.get_cycle_range()
        self.get_current()
        self.get_potential()



        # make a function that return the text file
        # for file in...
        # return what-comes-after "/" in path_d
        
        
    # This function reads the txt file and saves the columns using by the 
    # variable "names"
    def get_Ar_cycle_end(self):
        if self.CO_cycle_start != 0.0:
            self.Ar_cycle_end = self.CO_cycle_start-1
        else:
            #df_cycles = self.dataframe[['cycle number']]
            #self.cycle_start = df_cycles.iloc[0]['cycle number']
            self.Ar_cycle_end =  self.dataframe.iloc[-1]['cycle number']           
            
    def read_txt(self):
        #self.dataframe = pd.read_csv(self.path_d,delimiter="\t", names = names, header = 1, index_col=None)#header = 0)
        self.dataframe = pd.read_csv(self.path_file,delimiter="\t", index_col=None)
        self.header = self.dataframe.iloc[0]
        self.dataframe.rename(columns = self.header)
        self.dataframe.name = self.subsub_d
    
    def get_current(self):
        self.current = convert_current_density(self.dataframe[['<I>/mA','cycle number']], electrolyte = self.electrolyte)
        
    def get_potential(self):
        self.potential = convert_RHE(self.dataframe[['Ewe/V','cycle number']], electrolyte = self.electrolyte)
        
    #return the cycle range
    def get_cycle_range(self):
        df_cycles = self.dataframe[['cycle number']]
        self.cycle_start = df_cycles.iloc[0]['cycle number']
        self.cycle_end = df_cycles.iloc[-1]['cycle number']
        #self.cycle_range = [self.cycle_start, cycle_end]

    # This function returns the current in a specific cycle range. Eg. cycle 21
    # to cycle 24
    def get_current_cyc_range(self, cyc_i = None, cyc_f = None):
        if cyc_i is None:
            cyc_i = self.CO_cycle_start
        if cyc_f is None:
            cyc_f = self.cycle_end
        cyc_range = np.arange(cyc_i,cyc_f+1, 1)#list(range(cyc_i,cyc_f+1))
        df_cyc_range = self.dataframe_cyc_range(cyc_range)

        current_cyc_range = df_cyc_range[['<I>/mA','cycle number']]
        current_cyc_range = convert_current_density(current_cyc_range, electrolyte = self.electrolyte)
        return current_cyc_range

    # This function return the potential in a specific cycle range. Eg. cycle 21 
    # to cycle 24. 
    def get_potential_cyc_range(self, cyc_i = None, cyc_f = None):
        if cyc_i is None:
            cyc_i = self.CO_cycle_start
        if cyc_f is None:
            cyc_f = self.cycle_end
        cyc_range = np.arange(cyc_i,cyc_f+1, 1)#list(range(cyc_i,cyc_f+1))
        
        df_cyc_range = self.dataframe_cyc_range(cyc_range)
        #print(df_cyc_range[['cycle number']])
        
        potential_cyc_range = df_cyc_range[['Ewe/V','cycle number']]
        potential_cyc_range = convert_RHE(potential_cyc_range, electrolyte = self.electrolyte)
        
        return potential_cyc_range
    
    # This function extracts the data from the entire dataframe (EC lab data)
    # in a specific cycle range    
    def dataframe_cyc_range(self, cyc_range):
        return self.dataframe.loc[self.dataframe['cycle number'].isin(cyc_range)]
    
    # This function returns a dataframe containing three columns: 'cycle number', 'potential shift'
    # and 'standard deviation'
    def get_potential_shift(self, cyc_i = None, cyc_f = None):
        if cyc_i is None:
            cyc_i = self.CO_cycle_start
        if cyc_f is None:
            cyc_f = self.cycle_end
        Ar_potential = self.get_potential_cyc_range(self.Ar_cycle_end, self.Ar_cycle_end)
        Ar_current = self.get_current_cyc_range(self.Ar_cycle_end, self.Ar_cycle_end)
        Ar_intercept = get_intercept(Ar_potential, Ar_current)
        #print(Ar_intercept)
        print('Ar start: {0} \n cyc_start: {1} \n CO_cycle_start: {2}'.format(self.Ar_cycle_end,cyc_i,self.CO_cycle_start ))
        
        cyc_range = np.arange(cyc_i, cyc_f+1)
        potential_shift = []
        potential_shift_std = []
        intercepts = []
        
        
        for cycle in cyc_range:
            CO_potential_cycle = self.get_potential_cyc_range(cycle, cycle)
            CO_current_cycle = self.get_current_cyc_range(cycle, cycle)
            
            CO_intercept = get_intercept(CO_potential_cycle, CO_current_cycle)
            if CO_intercept.size != 0:
                #print('Cycle:{0}, shift: {1}'.format(cycle, CO_intercept))
                intercepts.append(CO_intercept[0])
                
                potential_shift_cycle = compute_CO_pot_shift(Ar_intercept, CO_intercept)
                potential_shift.append(potential_shift_cycle[0])
                potential_shift_std.append(potential_shift_cycle[1])
                
            else:
                intercepts.append(None)
                potential_shift.append(None)
                potential_shift_std.append(None)
            
        
        d = {'cycles': cyc_range, 'potential shift (mV)': potential_shift, 'std (mV)': potential_shift_std, 'CO intercept': intercepts}
        df = pd.DataFrame(data=d)
        return df
        
# ________________CP class_____________________________________________________________
class ECLabDataCP:
    def __init__(self, subsub_d, path_file, exp_details):
        self.subsub_d = subsub_d
        self.path_file = path_file
        self.exp_details = exp_details
        self.electrolyte = exp_details[0]
        self.exp_type = exp_details[2]
        self.membrane = exp_details[3]
        self.CO_time_start = exp_details[4]
        self.name = subsub_d

        self.read_txt()
        self.get_potential()
       
    def read_txt(self):
        #self.dataframe = pd.read_csv(self.path_d,delimiter="\t", names = names, header = 1, index_col=None)#header = 0)
        self.dataframe = pd.read_csv(self.path_file,delimiter="\t", index_col=None)
        self.header = self.dataframe.iloc[0]
        self.dataframe.rename(columns = self.header)
        self.dataframe.name = self.subsub_d
           
    def get_potential(self):
        self.potential = convert_RHE(self.dataframe[['Ewe/V','time/s']], electrolyte = self.electrolyte)
        self.potential = convert_time(self.potential)
