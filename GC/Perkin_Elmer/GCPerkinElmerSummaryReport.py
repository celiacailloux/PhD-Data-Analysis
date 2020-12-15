# -*- coding: utf-8 -*-
"""
Created on:             Thu Jun  4 06:54:38 2020

@author:                ceshuca

Updated:                June 19 2020
"""


import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator
from OSfunctions import find_all_csv_files_containing_str, \
    find_all_xlsx_files_containing_str
from datetime import datetime



# pd.set_option('display.max_rows', 15)
# pd.set_option('display.max_columns', 40)

class GCPESummaryData:
    def __init__(self, 
                 file_folder,
                 reaction_type = 'CO2R'):
        #attributes
        self.file_folder = file_folder
        self.data = {}
        self.injection_time = {}
        self.reaction_type = reaction_type
        #functions
        self.read_and_get_GC_summary_data()
        
        #attrubutes from functions
        self.get_PerkinElmer_calibration()        
        self.get_peaks_areas()
        
        # self.convert_to_RHE()
        # self.create_SHE_column()
        # self.convert_to_current_density()
        # self.create_timestamp_column()
        
        #self.convert_to_SHE()
    # ''' Read the txt file and save it in a pandas dataframe '''    
    # def read_txt(self):
    #     self.file_paths = find_all_xlsx_files_containing_str(rootdir = self.file_folder, 
    #                                                         _str = 'GC_summary')
    #     for file_path in self.file_paths:
    #         #self.dataframe = pd.read_csv(self.path_d,delimiter="\t", names = names, header = 1, index_col=None)#header = 0)
    #         file_name = os.path.basename(file_path)
    #         #df = pd.read_csv(ZIR_file_path, delimiter="\t", encoding = "ISO-8859-1",  index_col=None)
    #         #self.ZIR_data[file_name] = df.drop(df.index[[0]])
 
    #         df = pd.read_excel(file_path,
    #                            index_col=None)
    #         self.data[file_name] = df

            
        
    ''' Returns the current as a current density '''  
    def read_and_get_GC_summary_data(self):
        self.file_paths = find_all_csv_files_containing_str(rootdir = self.file_folder, 
                                                            _str = 'GC_summary')
        for file_path in self.file_paths:
            file_name = os.path.basename(file_path)
      
            df = pd.read_csv(file_path, 
                              delimiter=";", 
                              encoding = "ISO-8859-1", 
                              header = None,
                              skiprows = [0,1,2,3],
                              usecols = [*range(1, 13), *range(18, 26), *range(31, 35)],
                              names = ['File name',
                                       'Sample name',
                                       'Date of Injection',
                                       'Time of Injection',
                                       'H2 Time', 'H2 Area',
                                       'O2 Time', 'O2 Area',
                                       'N2 Time', 'N2 Area',
                                       'CH4 Time', 'CH4 Area',
                                       'CO Time', 'CO Area',
                                       'CO2 Time', 'CO2 Area',
                                       'C2H4 Time', 'C2H4 Area',
                                       'C2H6 Time', 'C2H6 Area',
                                       'C3H6 Time', 'C3H6 Area',
                                       'C3H8 Time', 'C3H8 Area'],
                              index_col=None)
            df = df.dropna() # remove all row containing NaN
            df['datetime'] = df['Date of Injection'].astype(str) + ' ' + df['Time of Injection'].astype(str)
            df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce') # it replaces non numeric to NaNs:
            df['timestamp'] = df['datetime'].astype('int64') // 10**9
            
            # n_rows = len(df['timestamp'])
            
            # df['timestamp'] = df['timestamp'].head(-int(n_rows/2))
            # df['timestamp'] = df['timestamp'].fillna(0)
            # df['timestamp'] = df['timestamp'].astype('int64')
        
            self.injection_time[file_name] = df
            self.data[file_name] = df
            
            
            # df = pd.read_excel(file_path,
            #                    header = 0,
            #                    skiprows = [0,1,3],
            #                    index_col=None)
            # print(list(df.columns))
            # column_names = list(df.columns)

            # #print(df.head(3))
            # #self.injection_time[file_name] = df 
            # # print(df[[column_names[0]],[column_names[1]]])
            # date = column_names[3]
            # time = column_names[4]
            # print(df[[date, time]])
            # df['datetime'] = df[date].astype(str) + df[time].astype(str)
            # print(df['datetime'])
            
    def get_PerkinElmer_calibration(self):
        " all calibration facetors are in uV*s/mol "
        

        if self.reaction_type == 'CO2R':
            self.calibration_CO2R = {'FID':  {}, 'TCD':  {}}
            # 50 sccm
            # self.calibration_CO2R['FID']['CO']    = {'slope' : 3306618,   'z': 2}
            # self.calibration_CO2R['TCD']['H2']    = {'slope' : 75668,     'z': 2}
            # self.calibration_CO2R['TCD']['O2']    = {'slope' : 7370,      'z': 10}
            # self.calibration_CO2R['TCD']['N2']    = {'slope' : 5756,      'z': 10}
            # self.calibration_CO2R['TCD']['CO']	= {'slope' : 5318,      'z': 2}
            # self.calibration_CO2R['TCD']['CO2']	= {'slope' : 5366,      'z': 0}
            # self.calibration_CO2R['FID']['C2H4']  = {'slope' : 6701790,   'z': 12}
            # self.calibration_CO2R['FID']['C3H6']  = {'slope' : 10252315,  'z': 18}
            # self.calibration_CO2R['FID']['CH4']   = {'slope' : 3359981,   'z': 8}
            # self.calibration_CO2R['FID']['C3H8']  = {'slope' : 10382908,  'z': 20}
            
            ' 10 scmm March 20 2020 '
            # CH4_FID	2785051.33
            # CO_FID	2736650.70
            # CO2_FID	2680599.09
            # C2H4_FID	5603906.80
            # C2H6_FID	5692391.95
            # C3H6_FID	8526507.60
            # C3H8_FID	8680642.65
            # H2_TCD	63541.43
            # O2_TCD	7369.83
            # N2_TCD	5755.54
            # CH4_TCD	15752.26903
            # CO_TCD	4992.095433
            # CO2_TCD	5296.766015
            
            # self.calibration_CO2R['FID']['CO']    = {'slope' : 2736650.70,    'z': 2}
            # # CO2 FID 2680599.09
            # self.calibration_CO2R['TCD']['H2']    = {'slope' : 63541.43,      'z': 2}
            # # self.calibration_CO2R['TCD']['O2']    = {'slope' : 7369.83,       'z': 0}
            # # self.calibration_CO2R['TCD']['N2']    = {'slope' : 5755.54,       'z': 0}
            # # self.calibration_CO2R['TCD']['CO']	= {'slope' : 4992.095433,   'z': 2}
            # # self.calibration_CO2R['TCD']['CO2']	= {'slope' : 5296.766015,   'z': 0}
            # # CH4 TCD 15752.26903
            # self.calibration_CO2R['FID']['C2H4']  = {'slope' : 5603906.80,    'z': 12}
            # self.calibration_CO2R['FID']['C2H6']  = {'slope' : 5692391.95,    'z': 14}
            # self.calibration_CO2R['FID']['C3H6']  = {'slope' : 8526507.60,    'z': 18}
            # self.calibration_CO2R['FID']['CH4']   = {'slope' : 2785051.33,    'z': 8}
            # self.calibration_CO2R['FID']['C3H8']  = {'slope' : 8680642.65,    'z': 20} 
            
            self.calibration_CO2R['FID']['CO']    = {'slope' : 2752241.03,    'z': 2}
            # CO2 FID 2654357.07
            self.calibration_CO2R['TCD']['H2']    = {'slope' : 84492.02,      'z': 2}
            # self.calibration_CO2R['TCD']['O2']    = {'slope' : None,       'z': 0}
            # self.calibration_CO2R['TCD']['N2']    = {'slope' : None,       'z': 0}
            # self.calibration_CO2R['TCD']['CO']	= {'slope' : 7025.40,   'z': 2}
            # self.calibration_CO2R['TCD']['CO2']	= {'slope' : 7449.13,   'z': 0}
            # CH4 TCD 22452.02
            self.calibration_CO2R['FID']['CH4']   = {'slope' : 2921101.39,    'z': 8}
            self.calibration_CO2R['FID']['C2H4']  = {'slope' : 5843969.22,    'z': 12}
            self.calibration_CO2R['FID']['C2H6']  = {'slope' : 5932381.85,    'z': 14}
            self.calibration_CO2R['FID']['C3H6']  = {'slope' : 8869813.78,    'z': 18}
            self.calibration_CO2R['FID']['C3H8']  = {'slope' : 9066898.89,    'z': 20} 
            
            ' 10 scmm October 20 2020 '
        else:
            print('no reaction type specified and no CALIBRATION DICT saved')        
    
            
    def get_peaks_areas(self):
        self.peaks_areas = {}
        for file_name, GC_data in self.data.items():
            # return the difference between each row. Since the first row will be Nan, it fills Nan to 0
            FID_GC_data = GC_data[GC_data['File name'].str.contains('fid')]
            FID_GC_data.rename(columns = {'H2 Area':'FID-H2',
                                          'O2 Area': 'FID-O2',
                                            'N2 Area': 'FID-N2',
                                            'CH4 Area':'FID-CH4',
                                            'CO Area': 'FID-CO',
                                            'CO2 Area': 'FID-CO2',
                                            'C2H4 Area': 'FID-C2H4',
                                            'C2H6 Area': 'FID-C2H6',
                                            'C3H6 Area': 'FID-C3H6',
                                            'C3H8 Area': 'FID-C3H8'}, inplace = True)
                               

            TCD_GC_data = GC_data[GC_data['File name'].str.contains('tcd')].reset_index()
            TCD_GC_data.rename(columns = {'H2 Area':'TCD-H2',
                                          'O2 Area': 'TCD-O2',
                                            'N2 Area': 'TCD-N2',
                                            'CH4 Area':'TCD-CH4',
                                            'CO Area': 'TCD-CO',
                                            'CO2 Area': 'TCD-CO2',
                                            'C2H4 Area': 'TCD-C2H4',
                                            'C2H6 Area': 'TCD-C2H6',
                                            'C3H6 Area': 'TCD-C3H6',
                                            'C3H8 Area': 'TCD-C2H8'}, inplace = True) 
            TCD_keys = ['TCD-H2','TCD-O2','TCD-N2','TCD-CH4','TCD-CO','TCD-CO2',
                        'TCD-C2H4', 'TCD-C2H6', 'TCD-C3H6','TCD-C2H8']
            self.peaks_areas[file_name] = {'FID': FID_GC_data,
                                      'TCD': TCD_GC_data}

            self.peaks_areas[file_name] = pd.concat([FID_GC_data, TCD_GC_data], axis = 1)
            # self.peaks_areas
            # print(FID_GC_data.columns)
            # print(TCD_GC_data.columns)
            # GC_data['File name/bool'] = \
            #     GC_data['File name'].ne(GC_data['File name'].shift().bfill())
            # print(GC_data['File name/bool'] )
            # print(GC_data['File name/bool'].iloc[0:50] )
            # # = Ru_diff != 0  
            
    def compute_j_avg_df(self, CA1):
        ' find average current between two injections '
        j_avg_df = pd.DataFrame(columns = ['File Name', 
                                           'Ns', 
                                           'j avg', 
                                           'j std', 
                                           'V avg', 
                                           'time/timestamp',
                                           'start time'])
        for filename, CA_data in CA1.CA_data.items():
            N_Ns = CA_data['Ns'].unique() # gets number of loops in this CA file (np array)
            
            
            'iterate over number of loops in CA file'        
            for Ns in N_Ns:   
                
                CA_data_Ns = CA_data.loc[CA_data['Ns'] == Ns]
                
                j       = CA_data_Ns['I/mAcm-2']
                Vref    = CA_data_Ns['Ewe/V']
                VSHE    = CA_data_Ns['Ewe/SHE']
                VRHE    = CA_data_Ns['Ewe/RHE']
                t       = CA_data_Ns['time/datetime'].dt.strftime('%H:%M')
                
                j_avg_df = j_avg_df.append({'File Name'     :filename, 
                                            'Ns'            : Ns,
                                            'j avg'         : round(j.mean(),2), 
                                            'j std'         : j.std(),
                                            'V avg/REF'     : round(Vref.mean(),2),
                                            'V avg/SHE'     : round(VSHE.mean(),2),
                                            'V avg/RHE'     : round(VRHE.mean(),2),
                                            'time/timestamp': t.iloc[-1],
                                            'start time'    : t.iloc[0]},
                                            ignore_index = True)
                j_avg_df.sort_values(by         = ['time/timestamp'], 
                                     inplace    = True, 
                                     ascending  = True)                
        return j_avg_df.reset_index()
    
    def update_peak_areas_with_FE(self, peak_areas, GC_file_name, 
                                  calibration_CO2R, F, molar_flow,
                                  j_avg_df):
        FE_calculator = {}    
        for detector, gases in calibration_CO2R.items():
            for gas, gas_items in gases.items():
                FE_calculator[detector + '-' + gas] = \
                    gas_items['z']*F/gas_items['slope']*molar_flow
                    
        for detector_gas, z_F_inv_slope_mflow in FE_calculator.items():
            temp = peak_areas[GC_file_name][detector_gas].astype(float).mul(z_F_inv_slope_mflow)
            FE = temp.div(j_avg_df['j avg'].mul(1e-3).abs())
            peak_areas[GC_file_name][detector_gas + ' FE'] = FE
            # print(j_avg_df['j avg'])
            
        # for col in list(peak_areas[GC_file_name].columns):
        #     if 'FE' in col:
        #         # print(col)
        #         FE = peak_areas[GC_file_name][col]
        #         print('gas: {} \FE: {}'.format( col, FE)              
            
        return peak_areas
                    
        
            
    
            



