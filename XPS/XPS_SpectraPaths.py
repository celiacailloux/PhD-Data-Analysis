#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 17:43:22 2019

@author: celiacailloux
"""
#import os
import OSfunctions as osfunc
from OSfunctions import create_file_path,  get_user_path, join_paths
#______________________________________________________________________________
# Experimetnal spectra paths in a dictionary


""" 
Experimental files. Below are the file paths for the experimental files which
are the put into a dictionary (files_all) that contains the file path and label.
"""

user_path = osfunc.get_user_path()
XPS_data_dir    = 'OneDrive - Danmarks Tekniske Universitet/PhD/Data/XPS/'
XPS_data_path = join_paths(user_path, XPS_data_dir)


#SP14_single_elements    = join_paths(XPS_data_path, '20200204 Pd, ZnO and PdZn/SP30 Pd/SP30 Pd - Single Elements.xlsx')
SP14_single_elements_N  = join_paths(XPS_data_path, '20200204 Pd, ZnO and PdZn/SP14  ZnO/SP14 ZnO - Single Elements N.xlsx')
                                                    
SP30_single_elements    = join_paths(XPS_data_path, '20200204 Pd, ZnO and PdZn/SP30 Pd/SP30 Pd - Single Elements.xlsx')
SP30_single_elements_N  = join_paths(XPS_data_path, '20200204 Pd, ZnO and PdZn/SP30 Pd/SP30 Pd - Single Elements N.xlsx')

PdZn28_survey   = join_paths(XPS_data_path, '20200301 Impact of Ar-plasma-ion-etching/Impact of Ar plasma Ion etching/PdZn28 Pd1Zn1/PdZn28 Pd1Zn1 - Survey.xlsx')
PdZn28_valence  = join_paths(XPS_data_path, '20200301 Impact of Ar-plasma-ion-etching/Impact of Ar plasma Ion etching/PdZn28 Pd1Zn1/PdZn28 Pd1Zn1 - Valence.xlsx')
PdZn28_Pd       = join_paths(XPS_data_path, '20200301 Impact of Ar-plasma-ion-etching/Impact of Ar plasma Ion etching/PdZn28 Pd1Zn1/PdZn28 Pd1Zn1 - Pd3d.xlsx')
PdZn28_Pd_N     = join_paths(XPS_data_path, '20200301 Impact of Ar-plasma-ion-etching/Impact of Ar plasma Ion etching/PdZn28 Pd1Zn1/PdZn28 Pd1Zn1 - Pd3d Normalized.xlsx')
PdZn28_Zn_N     = join_paths(XPS_data_path, '20200301 Impact of Ar-plasma-ion-etching/Impact of Ar plasma Ion etching/PdZn28 Pd1Zn1/PdZn28 Pd1Zn1 - Zn2p Normalized.xlsx')
PdZn28_ZnLMM    = join_paths(XPS_data_path, '20200301 Impact of Ar-plasma-ion-etching/Impact of Ar plasma Ion etching/PdZn28 Pd1Zn1/PdZn28 Pd1Zn1 - ZnLMM.xlsx')
PdZn28_ZnLMM_N  = join_paths(XPS_data_path, '20200301 Impact of Ar-plasma-ion-etching/Impact of Ar plasma Ion etching/PdZn28 Pd1Zn1/PdZn28 Pd1Zn1 - ZnLMM Normalized.xlsx')

SP51_survey     = join_paths(XPS_data_path, '20200301 Impact of Ar-plasma-ion-etching/Impact of Ar plasma Ion etching/SP51 PdZn28 Ar plasma ion etched Pd1Zn1/SP51 Pd1Zn1 - Survey.xlsx')
SP51_valence    = join_paths(XPS_data_path, '20200301 Impact of Ar-plasma-ion-etching/Impact of Ar plasma Ion etching/SP51 PdZn28 Ar plasma ion etched Pd1Zn1/SP51 Pd1Zn1 - Valence.xlsx')
SP51_singe_elements     = join_paths(XPS_data_path, '20200301 Impact of Ar-plasma-ion-etching/Impact of Ar plasma Ion etching/SP51 PdZn28 Ar plasma ion etched Pd1Zn1/SP51 Pd1Zn1 - Single Elements.xlsx')
SP51_singe_elements_N   = join_paths(XPS_data_path, '20200301 Impact of Ar-plasma-ion-etching/Impact of Ar plasma Ion etching/SP51 PdZn28 Ar plasma ion etched Pd1Zn1/SP51 Pd1Zn1 - Single Elements N.xlsx') 

SP53_survey     = join_paths(XPS_data_path, '20200303 Al2O3 and H2-reduced ZnO/Al2O3 and H2-reduced ZnO/SP53 PdZn28 w Al2O3/SP53 - Pd1Zn1 - Survey.xlsx')
SP53_valence    = join_paths(XPS_data_path, '20200303 Al2O3 and H2-reduced ZnO/Al2O3 and H2-reduced ZnO/SP53 PdZn28 w Al2O3/SP53 - Pd1Zn1 - Single Elements.xlsx')#'20200303 Al2O3 and H2-reduced ZnO/Al2O3 and H2-reduced ZnO/SP53 PdZn28 w Al2O3/SP53 - Pd1Zn1 - Valence.xlsx')
SP53_singe_elements     = join_paths(XPS_data_path, '20200303 Al2O3 and H2-reduced ZnO/Al2O3 and H2-reduced ZnO/SP53 PdZn28 w Al2O3/SP53 - Pd1Zn1 - Single Elements.xlsx')
SP53_singe_elements_N   = join_paths(XPS_data_path, '20200303 Al2O3 and H2-reduced ZnO/Al2O3 and H2-reduced ZnO/SP53 PdZn28 w Al2O3/SP53 - Pd1Zn1 - Single Elements N.xlsx')



"""
Experiment description. Below a dictionary that contains the important information
about an XPS measurement.
"""
XPS_exps = {}



"""
SP14 (Pure ZnO) 
"""

XPS_exps['20200204 SP14']   = {'Paths'    : {'Survey'           : {},                                                                     
                                             'Valence'          : {},
                                             'Single Element'   : {}},
                               'Composition'    : 'ZnO',
                               'XRD phase'      : '',}

XPS_exps['20200204 SP14']['Paths']['Survey']['path']  = ''
XPS_exps['20200204 SP14']['Paths']['Survey']['measurement type'] = 'std' 
XPS_exps['20200204 SP14']['Paths']['Valence']['path'] = ''
XPS_exps['20200204 SP14']['Paths']['Valence']['measurement type'] = 'ARXPS' 
XPS_exps['20200204 SP14']['Paths']['Single Element']['Zn N'] = {}
XPS_exps['20200204 SP14']['Paths']['Single Element']['Zn N']['band'] = '2p'
XPS_exps['20200204 SP14']['Paths']['Single Element']['Zn N']['sheet_name'] = 'Zn2p Scan'
XPS_exps['20200204 SP14']['Paths']['Single Element']['Zn N']['path'] = SP14_single_elements_N
XPS_exps['20200204 SP14']['Paths']['Single Element']['Zn N']['measurement type'] = 'ARXPS'
# XPS_exps['20200204 SP14']['Paths']['Single Element']['ZnLMM'] = {}
# XPS_exps['20200204 SP14']['Paths']['Single Element']['ZnLMM']['band'] = 'LMM'
# XPS_exps['20200204 SP14']['Paths']['Single Element']['ZnLMM']['sheet_name'] = 'ZnLMM Scan'
# XPS_exps['20200204 SP14']['Paths']['Single Element']['ZnLMM']['path'] = SP14_single_elements_N
# XPS_exps['20200204 SP14']['Paths']['Single Element']['ZnLMM']['measurement type'] = 'ARXPS'
XPS_exps['20200204 SP14']['Paths']['Single Element']['ZnLMM N'] = {}
XPS_exps['20200204 SP14']['Paths']['Single Element']['ZnLMM N']['band'] = 'LMM'
XPS_exps['20200204 SP14']['Paths']['Single Element']['ZnLMM N']['sheet_name'] = 'ZnLMM Scan'
XPS_exps['20200204 SP14']['Paths']['Single Element']['ZnLMM N']['path'] = SP14_single_elements_N
XPS_exps['20200204 SP14']['Paths']['Single Element']['ZnLMM N']['measurement type'] = 'ARXPS'

"""
SP30 (Pure Pd) 
"""

XPS_exps['20200204 SP30'] = {'Paths'    : {'Survey'           : {},                                                                     
                                             'Valence'          : {},
                                             'Single Element'   : {}},
                               'Composition'    : 'Pd',
                               'XRD phase'      : '',}

XPS_exps['20200204 SP30']['Paths']['Survey']['path']  = ''
XPS_exps['20200204 SP30']['Paths']['Survey']['measurement type'] = 'std' 
XPS_exps['20200204 SP30']['Paths']['Valence']['path'] = ''
XPS_exps['20200204 SP30']['Paths']['Valence']['measurement type'] = 'ARXPS' 
XPS_exps['20200204 SP30']['Paths']['Single Element']['Pd'] = {}
XPS_exps['20200204 SP30']['Paths']['Single Element']['Pd']['band'] = '3d'
XPS_exps['20200204 SP30']['Paths']['Single Element']['Pd']['sheet_name'] = 'Pd3d Scan'
XPS_exps['20200204 SP30']['Paths']['Single Element']['Pd']['path'] = SP30_single_elements
XPS_exps['20200204 SP30']['Paths']['Single Element']['Pd']['measurement type'] = 'ARXPS'
XPS_exps['20200204 SP30']['Paths']['Single Element']['Pd N'] = {}
XPS_exps['20200204 SP30']['Paths']['Single Element']['Pd N']['band'] = '3d'
XPS_exps['20200204 SP30']['Paths']['Single Element']['Pd N']['sheet_name'] = 'Pd3d Scan'
XPS_exps['20200204 SP30']['Paths']['Single Element']['Pd N']['path'] = SP30_single_elements_N
XPS_exps['20200204 SP30']['Paths']['Single Element']['Pd N']['measurement type'] = 'ARXPS'


"""
PdZn28 
"""

XPS_exps['20200301 PdZn28'] = {'Paths'    : {'Survey'           : {},                                                                     
                                             'Valence'          : {},
                                             'Single Element'   : {}},
                               'Composition'    : 'PdZn(1:1)',
                               'XRD phase'      : 'PdZn',}
XPS_exps['20200301 PdZn28']['Paths']['Survey']['path']  = PdZn28_survey
XPS_exps['20200301 PdZn28']['Paths']['Survey']['measurement type'] = 'std' 
XPS_exps['20200301 PdZn28']['Paths']['Valence']['path'] = PdZn28_valence
XPS_exps['20200301 PdZn28']['Paths']['Valence']['measurement type'] = 'ARXPS' 
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Pd'] = {}
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Pd']['band'] = '3d'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Pd']['sheet_name'] = 'Pd3d Scan'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Pd']['path'] = PdZn28_Pd
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Pd']['measurement type'] = 'ARXPS'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Pd N'] = {}
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Pd N']['band'] = '3d'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Pd N']['sheet_name'] = 'Pd3d Scan'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Pd N']['path'] = PdZn28_Pd_N
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Pd N']['measurement type'] = 'ARXPS'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Zn N'] = {}
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Zn N']['band'] = '2p'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Zn N']['sheet_name'] = 'Zn2p Scan'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Zn N']['path'] = PdZn28_Zn_N
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['Zn N']['measurement type'] = 'ARXPS'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['ZnLMM'] = {}
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['ZnLMM']['band'] = 'LMM'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['ZnLMM']['sheet_name'] = 'ZnLMM Scan'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['ZnLMM']['path'] = PdZn28_ZnLMM
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['ZnLMM']['measurement type'] = 'ARXPS'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['ZnLMM N'] = {}
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['ZnLMM N']['band'] = 'LMM'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['ZnLMM N']['sheet_name'] = 'ZnLMM Scan'
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['ZnLMM N']['path'] = PdZn28_ZnLMM_N
XPS_exps['20200301 PdZn28']['Paths']['Single Element']['ZnLMM N']['measurement type'] = 'ARXPS'

XPS_exps['20200301 SP51']   = {'Paths'    : {'Survey'           : {},                                                                     
                                             'Valence'          : {},
                                             'Single Element'   : {}},
                               'Composition'    : 'PdZn(1:1)',
                               'XRD phase'      : 'PdZn',
                               }
XPS_exps['20200301 SP51']['Paths']['Survey']['path']  = SP51_survey
XPS_exps['20200301 SP51']['Paths']['Survey']['measurement type'] = 'std' 
XPS_exps['20200301 SP51']['Paths']['Valence']['path'] = SP51_valence
XPS_exps['20200301 SP51']['Paths']['Valence']['measurement type'] = 'ARXPS' 
XPS_exps['20200301 SP51']['Paths']['Single Element']['Pd'] = {}
XPS_exps['20200301 SP51']['Paths']['Single Element']['Pd']['band'] = '3d'
XPS_exps['20200301 SP51']['Paths']['Single Element']['Pd']['sheet_name'] = 'Pd3d Scan'
XPS_exps['20200301 SP51']['Paths']['Single Element']['Pd']['path'] = SP51_singe_elements
XPS_exps['20200301 SP51']['Paths']['Single Element']['Pd']['measurement type'] = 'ARXPS'
XPS_exps['20200301 SP51']['Paths']['Single Element']['Pd N'] = {}
XPS_exps['20200301 SP51']['Paths']['Single Element']['Pd N']['band'] = '3d'
XPS_exps['20200301 SP51']['Paths']['Single Element']['Pd N']['sheet_name'] = 'Pd3d Scan'
XPS_exps['20200301 SP51']['Paths']['Single Element']['Pd N']['path'] = SP51_singe_elements_N
XPS_exps['20200301 SP51']['Paths']['Single Element']['Pd N']['measurement type'] = 'ARXPS'
XPS_exps['20200301 SP51']['Paths']['Single Element']['Zn N'] = {}
XPS_exps['20200301 SP51']['Paths']['Single Element']['Zn N']['band'] = '2p'
XPS_exps['20200301 SP51']['Paths']['Single Element']['Zn N']['sheet_name'] = 'Zn2p Scan'
XPS_exps['20200301 SP51']['Paths']['Single Element']['Zn N']['path'] = SP51_singe_elements_N
XPS_exps['20200301 SP51']['Paths']['Single Element']['Zn N']['measurement type'] = 'ARXPS'
XPS_exps['20200301 SP51']['Paths']['Single Element']['ZnLMM'] = {}
XPS_exps['20200301 SP51']['Paths']['Single Element']['ZnLMM']['band'] = 'LMM'
XPS_exps['20200301 SP51']['Paths']['Single Element']['ZnLMM']['sheet_name'] = 'ZnLMM Scan'
XPS_exps['20200301 SP51']['Paths']['Single Element']['ZnLMM']['path'] = SP51_singe_elements
XPS_exps['20200301 SP51']['Paths']['Single Element']['ZnLMM']['measurement type'] = 'ARXPS'
XPS_exps['20200301 SP51']['Paths']['Single Element']['ZnLMM N'] = {}
XPS_exps['20200301 SP51']['Paths']['Single Element']['ZnLMM N']['band'] = 'LMM'
XPS_exps['20200301 SP51']['Paths']['Single Element']['ZnLMM N']['sheet_name'] = 'ZnLMM Scan'
XPS_exps['20200301 SP51']['Paths']['Single Element']['ZnLMM N']['path'] = SP51_singe_elements_N
XPS_exps['20200301 SP51']['Paths']['Single Element']['ZnLMM N']['measurement type'] = 'ARXPS'


XPS_exps['20200303 SP53'] = {'Paths'    : {'Survey'           : {},                                                                     
                                             'Valence'          : {},
                                             'Single Element'   : {}},
                               'Composition'    : 'PdZn(1:1)',
                               'XRD phase'      : 'PdZn',
                               }

XPS_exps['20200303 SP53']['Paths']['Survey']['path']  = SP53_survey
XPS_exps['20200303 SP53']['Paths']['Survey']['measurement type'] = 'std' 
XPS_exps['20200303 SP53']['Paths']['Valence']['path'] = SP53_valence
XPS_exps['20200303 SP53']['Paths']['Valence']['measurement type'] = 'ARXPS' 
XPS_exps['20200303 SP53']['Paths']['Single Element']['Pd'] = {}
XPS_exps['20200303 SP53']['Paths']['Single Element']['Pd']['band'] = '3d'
XPS_exps['20200303 SP53']['Paths']['Single Element']['Pd']['sheet_name'] = 'Pd3d Scan'
XPS_exps['20200303 SP53']['Paths']['Single Element']['Pd']['path'] = SP53_singe_elements
XPS_exps['20200303 SP53']['Paths']['Single Element']['Pd']['measurement type'] = 'ARXPS'
XPS_exps['20200303 SP53']['Paths']['Single Element']['Pd N'] = {}
XPS_exps['20200303 SP53']['Paths']['Single Element']['Pd N']['band'] = '3d'
XPS_exps['20200303 SP53']['Paths']['Single Element']['Pd N']['sheet_name'] = 'Pd3d Scan'
XPS_exps['20200303 SP53']['Paths']['Single Element']['Pd N']['path'] = SP53_singe_elements_N
XPS_exps['20200303 SP53']['Paths']['Single Element']['Pd N']['measurement type'] = 'ARXPS'
XPS_exps['20200303 SP53']['Paths']['Single Element']['Zn N'] = {}
XPS_exps['20200303 SP53']['Paths']['Single Element']['Zn N']['band'] = '2p'
XPS_exps['20200303 SP53']['Paths']['Single Element']['Zn N']['sheet_name'] = 'Zn2p Scan'
XPS_exps['20200303 SP53']['Paths']['Single Element']['Zn N']['path'] = SP53_singe_elements_N
XPS_exps['20200303 SP53']['Paths']['Single Element']['Zn N']['measurement type'] = 'ARXPS'
XPS_exps['20200303 SP53']['Paths']['Single Element']['ZnLMM'] = {}
XPS_exps['20200303 SP53']['Paths']['Single Element']['ZnLMM']['band'] = 'LMM'
XPS_exps['20200303 SP53']['Paths']['Single Element']['ZnLMM']['sheet_name'] = 'ZnLMM Scan'
XPS_exps['20200303 SP53']['Paths']['Single Element']['ZnLMM']['path'] = SP53_singe_elements
XPS_exps['20200303 SP53']['Paths']['Single Element']['ZnLMM']['measurement type'] = 'ARXPS'
XPS_exps['20200303 SP53']['Paths']['Single Element']['ZnLMM N'] = {}
XPS_exps['20200303 SP53']['Paths']['Single Element']['ZnLMM N']['band'] = 'LMM'
XPS_exps['20200303 SP53']['Paths']['Single Element']['ZnLMM N']['sheet_name'] = 'ZnLMM Scan'
XPS_exps['20200303 SP53']['Paths']['Single Element']['ZnLMM N']['path'] = SP53_singe_elements_N
XPS_exps['20200303 SP53']['Paths']['Single Element']['ZnLMM N']['measurement type'] = 'ARXPS'



