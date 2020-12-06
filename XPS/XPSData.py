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

def get_XPS_exps(exp_ID1, composition = '', XRD_phase = ''):
    XPS_exps = {}
    XPS_exps[exp_ID1]   = \
        {'Paths'            : {'Survey'     : {},                                                                     
                               'V'          : {},
                               'SE'         : {}},
         'Composition'      : '',
         'XRD phase'        : '',}    
    return XPS_exps

class XPSData:
    """ 
    Fill out description
    """
    
    # [static class variable] varibles inserted here will be shared by all instances
    # Could for instance be XPS instrument!
    # instrument = 'Thetaprobe'
    
    # [static class function] a function where "self" is left out of the
    # function ("function()" instead of "function(self)"
    
    def __init__(self, 
                 XPS_ID, 
                 XPS_exps, 
                 sample_description, 
                 C1s_CC_BE = 284.84):
        
        
        self.XPS_ID             = XPS_ID  
        self.XPS_exps           = XPS_exps
        self.XPS_info           = self.XPS_exps[XPS_ID]
        self.date               = XPS_ID.split(' ',1)[0]
        self.sample             = XPS_ID.split(' ',1)[1]
        self.sample_description = sample_description
        self.charge_shift       = 284.84-C1s_CC_BE
        self.paths              = self.XPS_info['Paths']
        self.composition        = self.XPS_info['Composition']
        self.XRD_phase          = self.XPS_info['XRD phase']
        self.angles_to_plot     = [28,37,47, 56, 65]#, 75]#[22, 34, 41, 49, 56, 64, 71, 79]
        #[22, 24 26 28 30 32, 34 35 37 39 41, 43 45 47 49 50, 52 54 56 58 60, 62 64 65 67 69, 71 73 75 77, 79]
        self.DPs_to_plot        = 1
        
        
        if bool(self.paths['Survey']):
            self.read_survey_spectrum()         #returns data_survey
        else:
            print('No paths for SURVEY found')
        if bool(self.paths['V']):
            self.read_valence_spectrum()        #returns data_valence
        else: 
            print('No paths for VALENCE found')
        if bool(self.paths['SE']):
            self.read_single_element_spectra()  #returns 
        else:
            print('No path for SE found')
        print('\n')            

        # print(self.data_SE.keys())
        # print(self.data_SE['Pd NI']['data'].head())
        # make a function that return the text file
        # for file in...
        # return what-comes-after "/" in path_d
        
                  
    def read_survey_spectrum(self):
        self._read_excel(spectrum_type = 'Survey')
        
    def read_valence_spectrum(self):
        self._read_excel(spectrum_type = 'V')
        
    def read_single_element_spectra(self):
        self._read_excel(spectrum_type = 'SE')
        
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
        
        if spectrum_type != 'SE':
            if self.paths[spectrum_type]['measurement type'] == 'std' and spectrum_type == 'Survey':
                " ____________________________________________________ survey "                
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
                dataframe['Binding Energy'] = dataframe['Binding Energy'].astype(float).add(self.charge_shift)
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
            
            elif self.paths[spectrum_type]['measurement type'] == 'ARXPS' and spectrum_type == 'V':
                " ____________________________________________________ valence "
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
                dataframe['Binding Energy'] = dataframe['Binding Energy'].astype(float).add(self.charge_shift)
               
                self.data_valence['data'] = dataframe
                self.data_valence['data_units'] = ['eV', 'Counts / s']
            elif self.paths[spectrum_type]['measurement type'] == 'DP' and spectrum_type == 'V':
                ''' valence band '''
                self.data_valence = {}
                file_path = self.paths[spectrum_type]['path']
                dataframe = pd.read_excel(file_path, 
                                               sheet_name = 'Valence', 
                                               header = [14],#[16],
                                               index_col=None)
                """
                Converts column to DP etching time. 
                DP etching time is converted from float to intergers.
                """
                # removes the row 'Etch Level (EtchLevel)\' and 'Binding Energy (E)'
                dataframe = dataframe.drop(dataframe.index[[0,1,2]])
                # converts columns from float to int 
                for i,col in enumerate(dataframe.columns.values):
                    if type(col) == float:
                        dataframe.columns.values[i] = int(col)
                # renames the frist column to xx
                dataframe.columns.values[0] = 'Binding Energy'
                
                " NB! Important to know. When doing depth profiling "
                " there is no need to charge shift. Charge shifting "
                " is due to the non-conductice carbon layer usually "
                " hence when depth profiling then shifting should   "
                " be necessary. "
                                    
                               
                self.data_valence['data'] = dataframe
                self.data_valence['data_units'] = ['eV', 'Counts / s']
            else:
                print('NB! Try again. Spectrum type recognized as: ', \
                      '\'{0}\'. Measurement type not recognized'.format(spectrum_type))
        
        elif spectrum_type == 'SE': 
            " ________________________________________________ single element "
        
            self.data_SE = {}
            for element, element_details in self.paths[spectrum_type].items():
                print('Getting {} data ...'.format(element))
                if self.paths[spectrum_type][element]['measurement type'] == 'DP'\
                    or self.paths[spectrum_type][element]['measurement type'] == 'ARXPS':
                    self.data_SE[element] = {}
                    file_path = element_details['path']
                    
                    dataframe = pd.read_excel(file_path, 
                                sheet_name = element_details['sheet_name'], 
                                header = [14],
                                index_col=None)                    
                    
                    for i,col in enumerate(dataframe.columns.values):
                        if type(col) == float:
                            dataframe.columns.values[i] = int(col)                  
                    dataframe.columns.values[0] = 'Binding Energy'                
                    
                    # removes rows
                    if element_details['measurement type'] == 'ARXPS':
                        dataframe = dataframe.drop(dataframe.index[[0,1]])                    
                    elif element_details['measurement type'] == 'DP':                  
                        dataframe = dataframe.drop(dataframe.index[[0,1,2]])                            
                    " NB! Important to know. When doing depth profiling "
                    " there is no need to charge shift. Charge shifting "
                    " is due to the non-conductice carbon layer usually "
                    " hence when depth profiling then shifting should   "
                    " be necessary. "
                    
                    # self.data_SE[element]['data'] =  dataframe
                    # self.data_SE[element]['data units'] =  ['eV', 'Counts / s'] 
                elif self.paths[spectrum_type][element]['measurement type'] == 'std':
                    self.data_SE[element] = {}
                    file_path = element_details['path']
                    
                    dataframe = pd.read_excel(file_path, 
                                sheet_name = element_details['sheet_name'], 
                                header = [15],
                                index_col=None)                    
                    dataframe.columns.values[0] = 'Binding Energy'
                    dataframe['Binding Energy'] = dataframe['Binding Energy'].astype(float).add(self.charge_shift)                    
                    
                    
                self.data_SE[element]['data'] =  dataframe
                self.data_SE[element]['data units'] =  ['eV', 'Counts / s']                    
            
                 
        else:
            print('Try again. Measurement type and spectrum type not recognized')

        '''
        When you have time, include other important information from
        the excel to the class, i.e "Acquisition Parameters"
        '''
             
    
    ''' ___________________________________________________ quick plotting '''
    
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
        
            
    def quick_plot_SE(self, 
                      element, 
                      save_plot = False, 
                      save_legend = True,
                      main_peak_only = False,
                      SE_type = 'SI'):
        print('Quick plotting {}... (main peak: {})'.format(element, main_peak_only))
        measurement_type = self.paths['SE'][element]['measurement type']
        # print(measurement_type)
        fig, ax = plt.subplots()
        color = pltF.color_maps(color_map = 'jkib')
        
        df = self.data_SE[element]['data']
        x = df['Binding Energy']        

        #print(y.columns.values)
        pltF.global_settings(ax)
        
        if measurement_type == 'ARXPS': 
            y = df.drop(df.columns[[0, 1]], axis = 1)
            y = y.filter(items = self.angles_to_plot, axis = 1)
            N = len(self.angles_to_plot) - 1
            for i, col in enumerate(y.columns):
                ax.plot(x,y[col], color = color(i/N), label = col, linewidth=3)
                         
            # pltF.XPS_global(ax, x, label = False, yticklabel = False,
            #                 measurement_type = 'SE ARXPS')#, measurement_type = 'XPS Survey')
        elif measurement_type == 'DP':   
            y = df.drop(df.columns[[0, 1]], axis = 1)
            y = y[y.columns[::self.DPs_to_plot]]
            N = len(y.columns)
            for i, col in enumerate(y.columns):
                if col == 0:
                    " NB! Important to know. When doing depth profiling "
                    " there is no need to charge shift. Charge shifting "
                    " is due to the non-conductice carbon layer usually "
                    " hence when depth profiling then shifting should   "
                    " be necessary. "
                    x0 = x.astype(float).add(self.charge_shift) 
                    print('NB! Only charge shifting for etching for: {}s'.format(col))
                    ax.plot(x0, y[col], color = color(i/(N-1)), label = str(col) + ' s', linewidth=3)
                else:
                    if 'NI' in element:
                        ax.plot(x, y[col].add(0.2*i), color = color(i/(N-1)), label = str(col) + ' s', linewidth=3)
                        # print(y[col])
                    else:
                        ax.plot(x, y[col], color = color(i/(N-1)), label = str(col) + ' s', linewidth=3)
            # pltF.XPS_global(ax, x, label = False, yticklabel = False,
            #                 measurement_type = 'SE ' + measurement_type)
        elif measurement_type == 'std':
            print('Plotting {}... ({})'.format(element, measurement_type))
            y = df.drop(df.columns[[0,1,3]], axis = 1)   
            # print(y)
            ax.plot(x, y, color = color(1), label = self.XPS_ID, linewidth=3)
            # pltF.XPS_global(ax, x, label = False, yticklabel = False,
            #         measurement_type = 'SE ' + measurement_type)  
        else:
            print('Measurement type not recognixed {}'.format(measurement_type))                         
        pltF.XPS_global(ax, 
                        x, 
                        label = False, 
                        yticklabel = False,
                        measurement_type = 'SE ' + measurement_type)                           
        pltF.XPS_custom_plot_SE_settings(ax, 
                                         element,
                                         main_peak_only,
                                         save_legend = save_legend)
    
        
        if save_plot:
            # adds SI to plot title. not necessary for NI
            if SE_type == 'SI':
                element += ' SI'
                
            if main_peak_only:
                element += ' main peak' 
                pltF.global_savefig(fig, 
                                    plt_title = str(date.today()) + ' ' + self.sample,
                                    subdirectory = 'main peak',
                                    addcomment = element + ' ' + self.sample_description)    
                
            else:
                print('Quick plotting {}...'.format(element))
                pltF.global_savefig(fig, 
                                    subdirectory = 'entire element scan',
                                    plt_title = str(date.today()) + ' ' + self.sample,
                                    addcomment = element + ' ' + self.sample_description)     
            plt.close()                
        else:
            plt.show()
        
    ''' _____________________________________________________ old functions '''    
   
    """
    Problems with counts
                if 'Counts / s  (Residuals × 0.5)' in self.dataframe.columns:
                self.dataframe = self.dataframe[['eV', 'Counts / s  (Residuals × 0.5)']]
            elif 'Counts / s  (Residuals × 1)' in self.dataframe.columns:
                self.dataframe = self.dataframe[['eV', 'Counts / s  (Residuals × 1)']]
            else:
                self.dataframe = self.dataframe[['eV', 'Counts / s']]                
    """
    def quick_plot_single_element_normalized(self, 
                                             element, 
                                             save_plot = False,
                                             main_peak_only = False):
        print('Does not exist anymore, change to quick_plot_SE')    
        
    def quick_plot_valence(self, save_plot = False):
        print('Does not exist anymore, change to quick_plot_SE') 
        
        # measurement_type = self.paths['V']['measurement type']
        # fig, ax = plt.subplots()
        # color = pltF.color_maps(color_map = 'jkib')
        
        # df = self.data_valence['data']
        # x = df['Binding Energy']
        # # remove the two first columns which contain x and an empty col       
        # y = df.drop(df.columns[[0, 1]], axis = 1)#, inplace = True)
        
        # pltF.global_settings(ax)
        
        # if measurement_type == 'ARXPS':
        #     y = y.filter(items = self.angles_to_plot, axis = 1)
        #     N = len(self.angles_to_plot) - 1
        #     for i, col in enumerate(y.columns):
        #         ax.plot(x,y[col], color = color(i/N), label = col, linewidth=2)
        
        #     pltF.XPS_global(ax, x, label = False, yticklabel = True,    
        #                     measurement_type = 'Valence ARXPS')
        # elif measurement_type == 'DP':
        #     # plots only every second
        #     y = y[y.columns[::2]]
        #     N = len(y.columns)
        #     # fig.set_size_inches(w=5,h=N*1)
        #     for i, col in enumerate(y.columns):
        #         if col == 0:
        #             " NB! Important to know. When doing depth profiling "
        #             " there is no need to charge shift. Charge shifting "
        #             " is due to the non-conductice carbon layer usually "
        #             " hence when depth profiling then shifting should   "
        #             " be necessary. "
        #             x = x.astype(float).add(self.charge_shift)
        #             print(self.charge_shift)
        #         if N == 1:
        #             ax.plot(x, y[col].add(i*0.1), color = color(i/(N)), label = str(col) + ' s', linewidth=2)
        #         else:
        #             ax.plot(x, y[col].add(i*0.1), color = color(i/(N-1)), label = str(col) + ' s', linewidth=2)
        #         # ax.plot(x, y[col], color = color(i/(N-1)), label = str(col) + ' s', linewidth=2)
            
        #     "Update Measurement type"
        #     pltF.XPS_global(ax, x, label = False, yticklabel = False,
        #                     measurement_type = 'V ' + measurement_type)    
        # else:
        #     print('Measurement type not recognixed {}'.format(measurement_type))
            
        # if save_plot:
        #     pltF.global_savefig(fig, 
        #                         plt_title = str(date.today()) + ' ' + self.sample,
        #                         addcomment = 'Valence' + ' ' + self.sample_description + \
        #                         '- NI')        
        
      

    
    