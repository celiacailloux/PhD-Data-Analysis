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

class ECLabDataCV:
    def __init__(self, 
                 file_path, 
                 CO_cycle_start, 
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
        self.CO_cycle_start = CO_cycle_start
        self.Ar_cycle_end = CO_cycle_start-1
        self.label = label
        self.exp_name = exp_name
        self.A_electrode = A_electrode 
        self.uncompensated_R = uncompensated_R
        self.R = R
        self.E_ref = reference_electrode_potential
        #functions


        self.read_txt()
        self.get_Ar_cycle_end()
        self.get_cycle_range()
        self.convert_to_RHE()
        self.create_SHE_column()
        self.convert_to_current_density()
        #self.convert_to_SHE()
    ''' Read the txt file and save it in a pandas dataframe '''    
    def read_txt(self):
        #self.dataframe = pd.read_csv(self.path_d,delimiter="\t", names = names, header = 1, index_col=None)#header = 0)
        #print(self.file_path)
        self.dataframe = pd.read_csv(self.file_path,delimiter="\t", index_col=None)#, encoding = "ISO-8859-1")#, error_bad_lines=False)
        self.dataframe.name = self.exp_name
        #print(self.dataframe)
        
    ''' Returns the last Ar cycle '''
    def get_Ar_cycle_end(self):
        if self.CO_cycle_start != 0.0:
            self.Ar_cycle_end = self.CO_cycle_start-1
        else:
            #df_cycles = self.dataframe[['cycle number']]
            #self.cycle_start = df_cycles.iloc[0]['cycle number']
            self.Ar_cycle_end =  self.dataframe.iloc[-1]['cycle number']   

    ''' Returns the cycle start and cycle end''' 
    def get_cycle_range(self):
        df_cycles = self.dataframe[['cycle number']]
        self.cycle_start = df_cycles.iloc[0]['cycle number']
        self.cycle_end = df_cycles.iloc[-1]['cycle number']  

        
    ''' Returns the current as a current density '''  
    def convert_to_current_density(self):
        #self.dataframe = self.dataframe
        #self.dataframe['<I>/mA'] = (self.dataframe['<I>/mA'].mul(self.uncompensated_R)).divide(self.A_electrode)
        self.dataframe['<I>/mA'] = (self.dataframe['<I>/mA']).divide(self.A_electrode)
      
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
    def create_SHE_column(self):
        #self.dataframe = self.dataframe.copy()
        self.dataframe['Ewe/SHE'] = self.dataframe['Ewe/V'].sub(0.059*self.pH)
        self.header = self.dataframe.iloc[0]
        self.dataframe.rename(columns = self.header)

    ''' creates a dataframe in a cycle chosen range '''
    def get_dataframe_cyc_range(self, cyc_i, cyc_f):        
        cyc_range = np.arange(cyc_i,cyc_f+1)
        dataframe_cyc_range = self.dataframe.loc[self.dataframe['cycle number'].isin(cyc_range)]
        return dataframe_cyc_range
    
    ''' Returns the Ar cycles only '''
    def get_dataframe_Ar_cyc_range(self):
        cyc_i = self.dataframe['cycle number'].min()     
        cyc_f = self.Ar_cycle_end
        cyc_range = np.arange(cyc_i,cyc_f+1)
        dataframe_cyc_range = self.dataframe.loc[self.dataframe['cycle number'].isin(cyc_range)]
        return dataframe_cyc_range
    
        ''' Returns the CO cycles only '''
    def get_dataframe_CO_cyc_range(self):
        cyc_i = self.CO_cycle_start
        cyc_f = self.dataframe['cycle number'].max() 
        cyc_range = np.arange(cyc_i,cyc_f+1)
        dataframe_cyc_range = self.dataframe.loc[self.dataframe['cycle number'].isin(cyc_range)]
        return dataframe_cyc_range
        

        #current_cyc_range = df_cyc_range[['<I>/mA','cycle number']]
        #current_cyc_range = convert_current_density(current_cyc_range, electrolyte = self.electrolyte)
        #return current_cyc_range  

#    ''' simple function where the '''
#    def dataframe_cyc_range(self, cyc_range):
#        return self.dataframe.loc[self.dataframe['cycle number'].isin(cyc_range)]
  
        
''' ________________________  New ones_____________'''#        

#
#    # This function return the potential in a specific cycle range. Eg. cycle 21 
#    # to cycle 24. 
#    def get_potential_cyc_range(self, cyc_i = None, cyc_f = None):
#        if cyc_i is None:
#            cyc_i = self.CO_cycle_start
#        if cyc_f is None:
#            cyc_f = self.cycle_end
#        cyc_range = np.arange(cyc_i,cyc_f+1, 1)#list(range(cyc_i,cyc_f+1))
#        
#        df_cyc_range = self.dataframe_cyc_range(cyc_range)
#        #print(df_cyc_range[['cycle number']])
#        
#        potential_cyc_range = df_cyc_range[['Ewe/V','cycle number']]
#        potential_cyc_range = convert_RHE(potential_cyc_range, electrolyte = self.electrolyte)
#        
#        return potential_cyc_range
#    

#    
#    # This function returns a dataframe containing three columns: 'cycle number', 'potential shift'
#    # and 'standard deviation'
#    def get_potential_shift(self, cyc_i = None, cyc_f = None):
#        if cyc_i is None:
#            cyc_i = self.CO_cycle_start
#        if cyc_f is None:
#            cyc_f = self.cycle_end
#        Ar_potential = self.get_potential_cyc_range(self.Ar_cycle_end, self.Ar_cycle_end)
#        Ar_current = self.get_current_cyc_range(self.Ar_cycle_end, self.Ar_cycle_end)
#        Ar_intercept = get_intercept(Ar_potential, Ar_current)
#        #print(Ar_intercept)
#        print('Ar start: {0} \n cyc_start: {1} \n CO_cycle_start: {2}'.format(self.Ar_cycle_end,cyc_i,self.CO_cycle_start ))
#        
#        cyc_range = np.arange(cyc_i, cyc_f+1)
#        potential_shift = []
#        potential_shift_std = []
#        intercepts = []
#        
#        
#        for cycle in cyc_range:
#            CO_potential_cycle = self.get_potential_cyc_range(cycle, cycle)
#            CO_current_cycle = self.get_current_cyc_range(cycle, cycle)
#            
#            CO_intercept = get_intercept(CO_potential_cycle, CO_current_cycle)
#            if CO_intercept.size != 0:
#                #print('Cycle:{0}, shift: {1}'.format(cycle, CO_intercept))
#                intercepts.append(CO_intercept[0])
#                
#                potential_shift_cycle = compute_CO_pot_shift(Ar_intercept, CO_intercept)
#                potential_shift.append(potential_shift_cycle[0])
#                potential_shift_std.append(potential_shift_cycle[1])
#                
#            else:
#                intercepts.append(None)
#                potential_shift.append(None)
#                potential_shift_std.append(None)
#            
#        
#        d = {'cycles': cyc_range, 'potential shift (mV)': potential_shift, 'std (mV)': potential_shift_std, 'CO intercept': intercepts}
#        df = pd.DataFrame(data=d)
#        return df
#        
## Convert the current (mA) to current density (mA/cm2) by the surface area
## of the rotating ring disc electrode (electrolyte) and also accounts for the 15 % extra
## in the resistance
#def convert_current_density(current, electrolyte):
#    if electrolyte == 'RDE':
#        A = 0.196 #cm2
#    elif electrolyte == 'KOH' or 'KHCO3':
#        A = 1 #cm2 
#    current = current.copy()
#    current['<I>/mA'] = (current['<I>/mA'].mul(17/20)).divide(A)
#    
#    return current
#
## Converts the potential to V vs. RHE. 
## Depends on the reference electrode used!
#def convert_RHE(voltage, electrolyte):
#    # note that the electrolyte measurements are with KOH!
#    if electrolyte == 'RDE':
#        pH = 13
#        E_ref =0.72
#    elif electrolyte == 'KOH':
#        pH = 13
#        E_ref = 0.21
#    elif 'KHCO3' in electrolyte:#electrolyte == 'KHCO3':
#        pH = 10                                                                #http://www.aqion.de/site/191
#        E_ref = 0#0.199                                                          # Ag/AgCl in saturated KCl
#    voltage = voltage.copy()
#    voltage['Ewe/V'] = voltage['Ewe/V'].add(E_ref+0.059*pH)      
#    return voltage   
#
#def convert_time(time):
#
#    time = time.copy()
#    time['time/s'] = time['time/s'].divide(60)
#    
#    return time
#
## This function returns the intercept of the measured potential (V vs. RHE)
## and 5 mA/cm2. The input is single cycle. 
#def get_intercept(potential_cycle, current_cycle):
#    j = [-5.5, -4.5]                                                            # current density where the CO shift is measured
#    df = current_cycle
#    df_next = df.loc[(df['<I>/mA'] >= j[0]) & (df['<I>/mA'] <= j[1])]
#    if not df_next.empty:
#        while len(df_next) >= 2:#not df_next.empty and len(df_next) >= 2:   
#    
#            df = df_next#df.loc[(df['<I>/mA'] >= j[0]) & (df['<I>/mA'] <= j[1])]
#            j[0] +=0.005
#            j[1] -=0.005
#            df_next = df.loc[(df['<I>/mA'] >= j[0]) & (df['<I>/mA'] <= j[1])]
#        
#        df_pot = potential_cycle
#        idx = df.index.values
#    
#    
#        shift_point = df_pot[df_pot.index.isin(idx)]
#        #print('Number of points intercepting with 5 mA/cm2: {}'.format(len(shift_point)))
#
#        std = shift_point['Ewe/V'].std()
#    
#        if np.isnan(std):
#            std = 0
#        shift_point = shift_point['Ewe/V'].mean()
#        intercept = shift_point
#        
#    else:
#        intercept = []
#        std = []
#    return np.array([intercept, std])
#
#def compute_CO_pot_shift(Ar_intercept, CO_intercept):
#    shift = (Ar_intercept[0]-CO_intercept[0])*1000                              #convert from V to mV
#    std = np.sqrt(np.power(CO_intercept[1],2))*1000
#    #std = np.sqrt(np.power(Ar_intercept[1],2)+np.power(CO_intercept[1],2))*1000
#    #print('Standard deviation: {} mV'.format(std))
#    
#    return np.array([shift,std])

