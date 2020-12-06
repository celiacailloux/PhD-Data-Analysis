#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created         March 27 2020

Updated         June 24 2020

@author         celiacailloux/ceshuca

"""

import pandas as pd
import os
import numpy as np
# from XPS_SpectraPaths import XPS_exps
import PlottingFunctions as pltF
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, AutoLocator, MultipleLocator
from datetime import date
pd.set_option('display.max_columns', 4)

  

class XPSData:
    """ 
    Fill out description
    """
    
    # [static class variable] varibles inserted here will be shared by all instances
    # Could for instance be XPS instrument!
    # instrument = 'Thetaprobe'
    
    # [static class function] a function where "self" is left out of the
    # function ("function()" instead of "function(self)"
    
    def __init__(self, XPS_ID, XPS_exps, sample_description):
        
        
        self.XPS_ID             = XPS_ID  
        self.XPS_exps           = XPS_exps
        self.XPS_info           = self.XPS_exps[XPS_ID]
        self.date               = XPS_ID.split(' ',1)[0]
        self.sample             = XPS_ID.split(' ',1)[1]
        self.sample_description = sample_description
        self.paths              = self.XPS_info['Paths']
        self.composition        = self.XPS_info['Composition']
        self.XRD_phase          = self.XPS_info['XRD phase']
        self.angles_to_plot     = [28,37,47, 56, 65]#, 75]#[22, 34, 41, 49, 56, 64, 71, 79]
        #[22, 24 26 28 30 32, 34 35 37 39 41, 43 45 47 49 50, 52 54 56 58 60, 62 64 65 67 69, 71 73 75 77, 79]
        
        
        # from old script, changed 24-06-2020
        # if bool(self.paths['Survey']):
        #     self.read_survey_spectrum()         #returns data_survey
        # if bool(self.paths['Valence']):
        #     self.read_valence_spectrum()        #returns data_valence
        # if bool(self.paths['Single Element']):
        #     self.read_single_element_spectra()  #returns data_single_element
        if bool(self.paths['Survey']):
            self.read_survey_spectrum()         #returns data_survey
        if bool(self.paths['V']):
            self.read_valence_spectrum()        #returns data_valence
        if bool(self.paths['SE']):
            self.read_single_element_spectra()  #returns data_single_element
        print('\n')            


        # make a function that return the text file
        # for file in...
        # return what-comes-after "/" in path_d
        
                  
    """
    This function will read data from an excel file. The way it reads will 
    depend on which kind of scan it is (Survey, element, ARXPS etc.). This 
    will be defined in the function by the self.datatype (default = 'std").    
    """
    def _check_if_excel_sheet_exists(self, file_path, tab = 'Peak Table'):
        dataframe_as_dict = pd.read_excel(file_path, sheet_name = None) # entire excel spread sheet is read
        sheet_names = dataframe_as_dict.keys()
        if tab in sheet_names:
            return True
        else:
            print('No tab named \"{}\", thus no survey'\
                  ' peaks identification nor quantification.'\
                      ' Has to be included manually.'.format(tab))
        
    def _read_excel(self, spectrum_type = 'Survey'):
        
        if spectrum_type != 'Single Element':
            if self.paths[spectrum_type]['measurement type'] == 'std' and spectrum_type == 'Survey':
                self.data_survey = {}
                file_path = self.paths[spectrum_type]['path']
                dataframe = pd.read_excel(file_path, 
                                               sheet_name = spectrum_type, 
                                               header = [15],
                                               index_col=None)
                dataframe.name = self.XPS_ID + ' ' + spectrum_type
                
                dataframe = dataframe[['eV', 'Counts / s']]
                units = dataframe.columns.values
                dataframe.columns = ['Binding Energy', 'Intensity'] #rename columns
                #header = self.dataframe.columns.values
                self.data_survey['data'] = dataframe
                self.data_survey['data_units'] = units
                
                survey_tab = 'Peak Table'
                if self._check_if_excel_sheet_exists(file_path, tab = survey_tab):
                    data_survey_peaks = pd.read_excel(file_path, 
                                                sheet_name = survey_tab,
                                                skip_rows = 0,
                                                header = 1,
                                                index_col=None)
                    self.data_survey['survey peaks'] = data_survey_peaks
            elif self.paths[spectrum_type]['measurement type'] == 'ARXPS' and spectrum_type == 'Valence':
                self.data_valence = {}
                file_path = self.paths[spectrum_type]['path']
                dataframe = pd.read_excel(file_path, 
                                               sheet_name = spectrum_type, 
                                               header = [14],#[16], 
                                               index_col=None)
                """
                Converts column to ARXPS angles. ARXPS are firstly converted
                into integers.
                """
                dataframe = dataframe.drop(dataframe.index[[0,1]])
                for i,col in enumerate(dataframe.columns.values):
                    if type(col) == float:
                        dataframe.columns.values[i] = int(col)
                dataframe.columns.values[0] = 'Binding Energy'
                
               
                self.data_valence['data'] = dataframe
                self.data_valence['data_units'] = ['eV', 'Counts / s']
        elif spectrum_type == 'Single Element': 
            self.data_single_element = {}
            for element, element_details in self.paths[spectrum_type].items():
                print('Getting {} data ...'.format(element))
                
                self.data_single_element[element] = {}
                file_path = element_details['path']
                
                if element_details['measurement type'] == 'ARXPS':
                    dataframe = pd.read_excel(file_path, 
                                sheet_name = element_details['sheet_name'], 
                                header = [14],
                                index_col=None)                    
                    dataframe = dataframe.drop(dataframe.index[[0,1]])
                    for i,col in enumerate(dataframe.columns.values):
                        if type(col) == float:
                            dataframe.columns.values[i] = int(col)
                    dataframe.columns.values[0] = 'Binding Energy'
                    self.data_single_element[element]['data'] =  dataframe
                    self.data_single_element[element]['data units'] =  ['eV', 'Counts / s']
        else:
            print('Try again. Measurement type and spectrum type not recognized')

        '''
        When you have time, include other important information from
        the excel to the class, i.e "Acquisition Parameters"
        '''
    def _custom_plot_single_element_settings(self, ax, element, main_peak_only):
        if main_peak_only:
            if 'ZnLMM' in element:
                ax.set_xlabel('Kinetic Energy / eV ', fontsize = 16)  
                ax.set_xlim(982, 998)
            elif 'Pd' in element:
                ax.xaxis.set_minor_locator(AutoMinorLocator(5))
                ax.xaxis.set_major_locator(MultipleLocator(1))
                ax.set_xlim(339, 332)
                #pltF.global_mayor_xlocator(ax, x_locator = 2) 
            elif 'Zn'in element:
                ax.xaxis.set_minor_locator(AutoMinorLocator(4))
                ax.xaxis.set_major_locator(MultipleLocator(2)) 
                ax.set_xlim(1027, 1017)
            #element += ' main peak'
        else:
            if 'ZnLMM' in element:
                ax.set_xlabel('Kinetic Energy / eV ', fontsize = 16)
                ax.legend(loc='upper left', fontsize = 12)
                ax.set_xlim(982, 998)
            elif element == 'Pd N':
                ax.xaxis.set_minor_locator(AutoMinorLocator(4))
                ax.xaxis.set_major_locator(MultipleLocator(2))
                #pltF.global_mayor_xlocator(ax, x_locator = 2) 
            elif element == 'Zn N':
                ax.xaxis.set_minor_locator(AutoMinorLocator(5))
                ax.xaxis.set_major_locator(MultipleLocator(5))        
        
    def read_survey_spectrum(self):
        self._read_excel(spectrum_type = 'Survey')
        
    def read_valence_spectrum(self):
        self._read_excel(spectrum_type = 'Valence')
        
    def read_single_element_spectra(self):
        self._read_excel(spectrum_type = 'Single Element')
    
    def quick_plot_survey(self, identification_quantification = True, save_plot = False):
        """
        This function plot the survey spectrum. If identifaction_quantification 
        is enabled, it will also plot "Avantage's" search for peaks and insert
        a table with identified and quantified elements.
        
        Figures is saved in the auto-generated folder "Figures"
        """
        fig, ax = plt.subplots()
        fig.set_size_inches(w=10,h=6)
        x = self.data_survey['data']['Binding Energy']
        y = self.data_survey['data']['Intensity']
        
        #ax.semilogy(x,y)
        ax.plot(x, y, color = '#1f77b4')
        
        if identification_quantification:
            df_for_table = self.data_survey['survey peaks'][['Name ','Peak BE', 'Atomic %']].copy()
            # converts atomic % into integer
            df_for_table['Atomic %'] = df_for_table['Atomic %'].round(0).astype(int) 
        
            """ 
            Identification and quantification is inserted as a table in the survey
            spectrum in the upper right corner.
            """           
            for peak_BE in df_for_table['Peak BE']:
                row_idx = df_for_table['Peak BE'] == peak_BE
                peak = df_for_table['Name '][row_idx]
                
                ymax = y[x.between(peak_BE-0.5, peak_BE+0.5)]
                
                ax.vlines(x=peak_BE, ymin = 0, ymax = ymax, linestyles = '--', 
                          color = 'green', alpha = 0.5)
                ax.text(peak_BE, y = ymax, s = peak.to_string(index = False), color = '#1f77b4')
            pltF.global_plt_table(ax, df_for_table, config = 'XPS Survey')
            self.dat = df_for_table
        #if N
                
        pltF.global_settings(ax)
        pltF.XPS_global(ax, x, label = False, measurement_type = 'XPS Survey')
        ax.set_ylim(top = max(y*1.4))
        if save_plot:
            pltF.global_savefig(fig, 
                                plt_title = str(date.today()) + ' ' + self.sample,
                                addcomment = 'Survey' + ' ' + self.sample_description)
        
    def quick_plot_valence(self, save_plot = False):
        fig, ax = plt.subplots()
        color = pltF.color_maps(color_map = 'jkib')
        
        df = self.data_valence['data']
        x = df['Binding Energy']        
        y = df.drop(df.columns[[0, 1]], axis = 1)#, inplace = True)
        #angles_to_plot = [24, 35, 45, 54, 75]
        y = y.filter(items = self.angles_to_plot, axis = 1)
        N = len(self.angles_to_plot) - 1
        for i, col in enumerate(y.columns):
            ax.plot(x,y[col], color = color(i/N), label = col, linewidth=2)
            
        
        pltF.global_settings(ax)
        pltF.XPS_global(ax, x, label = False, yticklabel = True,
                        measurement_type = 'Valence ARXPS')
        if save_plot:
            pltF.global_savefig(fig, 
                                plt_title = str(date.today()) + ' ' + self.sample,
                                addcomment = 'Valence' + ' ' + self.sample_description)
            
            
    def quick_plot_single_element(self, element, save_plot = False,
                                  main_peak_only = False):
        print('quick plotting {} ({})'.format(element, self.sample_description))
        fig, ax = plt.subplots()
        color = pltF.color_maps(color_map = 'jkib')
        
        df = self.data_single_element[element]['data']
        x = df['Binding Energy']        
        y = df.drop(df.columns[[0, 1]], axis = 1)#, inplace = True)

        #angles_to_plot = [24, 35, 45, 54, 75]
        y = y.filter(items = self.angles_to_plot, axis = 1)
        N = len(self.angles_to_plot) - 1
        for i, col in enumerate(y.columns):
            ax.plot(x,y[col], color = color(i/N), label = col, linewidth=3)
                          
        pltF.global_settings(ax)
        pltF.XPS_global(ax, x, label = False, yticklabel = True,
                        measurement_type = 'Single Element ARXPS')#, measurement_type = 'XPS Survey')
        
        self._custom_plot_single_element_settings(ax, element, main_peak_only)
        
        if save_plot:
            if main_peak_only:
                element += ' main peak'
            pltF.global_savefig(fig, 
                                plt_title = str(date.today()) + ' ' + self.sample,
                                addcomment = element + ' ' + self.sample_description)
            
    
    def quick_plot_single_element_normalized(self, element, save_plot = False,
                                             main_peak_only = False):
        fig, ax = plt.subplots()
        color = pltF.color_maps(color_map = 'jkib')
        
        df = self.data_single_element[element]['data']
        x = df['Binding Energy']        
        y = df.drop(df.columns[[0, 1]], axis = 1)#, inplace = True)
        #print(y.columns.values)
        #angles_to_plot = [24, 35, 45, 54, 75]
        y = y.filter(items = self.angles_to_plot, axis = 1)
        N = len(self.angles_to_plot) - 1
        for i, col in enumerate(y.columns):
            ax.plot(x,y[col], color = color(i/N), label = col, linewidth=3)
         
                    
        pltF.global_settings(ax)
        pltF.XPS_global(ax, x, label = False, yticklabel = False,
                        measurement_type = 'Single Element ARXPS Normalized')#, measurement_type = 'XPS Survey')

        self._custom_plot_single_element_settings(ax, element, main_peak_only)

        
        if save_plot:
            if main_peak_only:
                element += ' main peak'            
            pltF.global_savefig(fig, 
                                plt_title = str(date.today()) + ' ' + self.sample,
                                addcomment = element + ' ' + self.sample_description)
        
        
   
    """
    Problems with counts
                if 'Counts / s  (Residuals × 0.5)' in self.dataframe.columns:
                self.dataframe = self.dataframe[['eV', 'Counts / s  (Residuals × 0.5)']]
            elif 'Counts / s  (Residuals × 1)' in self.dataframe.columns:
                self.dataframe = self.dataframe[['eV', 'Counts / s  (Residuals × 1)']]
            else:
                self.dataframe = self.dataframe[['eV', 'Counts / s']]
    """
    
    '''
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

    '''
        


    
    