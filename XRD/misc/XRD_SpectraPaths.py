#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 17:43:22 2019

@author: celiacailloux
"""

''' Fig size '''
''' Angles range [10,120]
Three spectra: (6,3.5) '''
''' Angles range [10,120]: '''

#______________________________________________________________________________

''' Reference files '''
# Reference paths
refNP1 = 'Reference spectra/NP1_GaPa2/powderpattern_xy_collCode#107294.csv'
refNP2 = 'Reference spectra/NP2_GaPd/powderpattern_xy_collCode#108490.csv'
refNP3 = 'Reference spectra/NP3_Ga2Pd/powderpattern_xy_collCode#261111.csv'

refNP3cubic = 'Reference spectra/NP3_Ga2Pd/powderpattern_xy_collCode#635059_cubic.csv'
#refTiO2 = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/TiO2/powderpattern_xy_collCode#9852.csv'          # TiO2 support
refTiO2 = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/TiO2/powderpattern_xy_collCode#92363.csv'
refPdO = 'Reference spectra/PdO/powderpattern_xy_collCode#24692.csv'
refGaPd2 = 'Reference spectra/GaPd2/powderpattern_xy_collCode#107293.csv'
refSi = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/Si/powderpattern_xy_collCode#53783.csv'             # Silicon reference
refGa2O3_alpha = 'Reference spectra/Ga2O3/powderpattern_xy_collCode#34243.csv'
refGa2O3_beta = 'Reference spectra/Ga2O3/powderpattern_xy_collCode#635016.csv'

refGaPd2 = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/GaPd2/powderpattern_xy_collCode#107293.csv'
refGaPd = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/GaPd/powderpattern_xy_collCode#108490.csv'
refGa2Pd = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/Ga7Pd3/powderpattern_xy_collCode#174527.csv'

refGa3Pd5 = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/Ga3Pd5/powderpattern_xy_collCode#103906.csv'
refGa2Pd5 = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/Ga2Pd5/powderpattern_xy_collCode#103904.csv'
refGa5Pd13 = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/Ga5Pd13/powderpattern_xy_collCode#107572.csv'

refNi2FeGa = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/Ni2FeGa/powderpattern_xy_collCode#247174.csv'
refCo2FeGa = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/Co2FeGa/powderpattern_xy_collCode#102386.csv'
refCoGa = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/CoGa/powderpattern_xy_collCode#657494.csv'
refCo12Ga08 = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/Co1.2Ga0.8/powderpattern_xy_collCode#197568.csv'

refTi = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/Ti/powderpattern_xy_collCode#43733.csv' 
refPd = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/Pd/powderpattern_xy_collCode#64914.csv'
refGa = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/Reference spectra/Ga/powderpattern_xy_collCode#52271.csv'

refPd = 'powderpattern_xy_collCode%23171749.csv'
refZnO_NaCl = 'powderpattern_xy_collCode#38222.csv'
refZnO_Wurtzite = ''



# Reference paths in a dictionary
ref_files_all = {'NP1': refNP1 , 
                 'NP2': refNP2 , 
                 'NP3':refNP3, 
                 'GaPd2': refGaPd2,
                 'GaPd': refGaPd,
                 'Ga2Pd': refGa2Pd,
                 'Ga3Pd5': refGa3Pd5,
                 'Ga2Pd5': refGa2Pd5,
                 'Ga5Pd13': refGa5Pd13,
                 'TiO2':refTiO2, 
                 'PdO': refPdO, 
                 'GaPd2': refGaPd2, 
                 'NP3cubic': refNP3cubic, 
                 'Si1': refSi,
                 'Ga2O3_alpha': refGa2O3_alpha, 
                 'Ga2O3_beta': refGa2O3_beta, 
                 'Ni2FeGa': refNi2FeGa,
                 'Co2FeGa': refCo2FeGa,
                 'CoGa': refCoGa,
                 'Co12Ga08': refCo12Ga08,
                 'Ti': refTi,
                 'Pd': refPd,
                 'Ga': refGa,
                 'ZnO_NaCl': refZnO_NaCl,
                 'ZnO_Wurtzite': refZnO_Wurtzite,
                 'Pd': refPd} 

# Labels for the titles
ref_labels_all = {'NP1': 'ref Ga$_{0.9}$Pd$_{2.1}$' , 
                  'NP2' : 'ref Ga$_{0.15}$Pd$_{0.85}$', 
                  'NP3' :'ref GaPd', 
                  'GaPd2': 'GaPd$_2$ (ref)',
                  'GaPd': 'GaPd (ref)',
                  'Ga2Pd': 'Ga$_7$Pd$_3$ (ref)',
                  'Ga3Pd5': 'Ga$_3$Pd$_5$ (ref)',
                  'Ga2Pd5': 'Ga$_2$Pd$_5$ (ref)',
                  'Ga5Pd13': 'Ga$_5$Pd$_13$ (ref)',
                  'TiO2': 'TiO$_2$ (ref)',
                  'PdO':'ref PdO', 
                  'NP3cubic': 'ref GaPd cubic', 
                  'Si1' : 'Si (ref)',
                  'Ga2O3_alpha': r'ref $ \alpha$-Ga$_2$O$_3$ ', 
                  'Ga2O3_beta': r'ref $\beta$-Ga$_2$O$_3$',
                  'Ni2FeGa': r'Ni$_2$FeGa (ref)',
                  'Co2FeGa': r'Co$_2$FeGa (ref)',
                  'CoGa': r'CoGa (ref)',
                  'Co12Ga08' : r'Co$_1.2$Ga$_0.8$',
                  'Ti': 'Ti (ref)',
                  'Pd': 'Pd (ref)',
                  'Ga': 'Ga (ref)',
                  'ZnO_NaCl': 'ZnO [NaCl] (ref)',
                  'ZnO_Wurtzite': 'ZnO [Wurtzite] (ref)'} 

''' Experimental files '''
# Experimental spectra paths
# CSV files
                                                                               # 20190121
NP1 = '20190121/XRDML/spinner_default_2hrs_GaPd2_C1_I11_20190121.xrdml'
NP2 = '20190121/XRDML/spinner_default_2hrs_GaPd_C2_I9_20190121.xrdml'
NP3 = '20190121/XRDML/spinner_default_2hrs_Ga2Pd_C3_I10_20190121.xrdml'
TiO2 = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/20190121/spinner_default_2hrs_TiO2_nmPowder_I12_20190121.csv'
Si_20190121_1 = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/20190121/spinner_default_2hrs_Silicon_I1_20190121.csv' 
Si_20190121_2 = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/20190121/spinner_default_2hrs_Silicon_I15_20190121.csv'

GaPd2 = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/20190121/spinner_default_2hrs_GaPd2_C1_I11_20190121.csv'
GaPd = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/20190121/spinner_default_2hrs_GaPd_C2_I9_20190121.csv'
Ga2Pd = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/20190121/spinner_default_2hrs_Ga2Pd_C3_I10_20190121.csv'

GaPdthinfilm = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/20190622 GIXRD/20190622 GaPd Ass Thin Film Scan 35 to 85 deg Omega 2 deg 2 mmLONG SCAN_1.csv'
GaPdthinfilmAfter = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/20190622 GIXRD/20190622 GaPd Tested Ass Thin Film Scan 35 to 85 deg Omega 2 deg 2 mmLONG SCAN_1.csv'
                                                                               # 20190129
Ni2FeGa = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/20190129/spinner_default_2hrs_NP4_Ni2FeGa_I2_20190129.csv'
Co2FeGa = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/20190129/spinner_default_2hrs_NP5_Co2FeGa_I3_20190129.csv'
CoGa = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/20190129/spinner_default_2hrs_NP6_CoGa_I4_20190129.csv'
Si_20190129_1 = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/20190129/spinner_default_2hrs_Silicon_I1_20190129.csv'      # Si 
Si_20190129_2 = '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/XRD/20190129/spinner_default_2hrs_Silicon_I6_20190129.csv'      # Si 


#______________________________________________________________________________
# Experimetnal spectra paths in a dictionary

files_all = {'NP1': NP1 , 
             'NP2': NP2 , 
             'NP3':NP3,
             'GaPd2': GaPd2,
             'GaPd': GaPd,
             'Ga2Pd': Ga2Pd,
             'TiO2':TiO2, 
             'Si_20190121_1': Si_20190121_1, 
             'Si_20190121_2': Si_20190121_2, 
             'Si_20190129_1': Si_20190129_1, 
             'Si_20190129_2': Si_20190129_2,
             'Ni2FeGa': Ni2FeGa, 
             'Co2FeGa': Co2FeGa, 
             'CoGa': CoGa,
             'GaPdthinfilm' : GaPdthinfilm} 

labels_all = {'NP1': 'GaPd$_2$', 
              'NP2': 'GaPd' , 
              'NP3':'Ga$_2$Pd', 
              'GaPd2': 'GaPd$_2$ (exp)',
              'GaPd': 'GaPd (exp)',
              'Ga2Pd': 'Ga$_2$Pd (exp)',
              'TiO2':'TiO$_2$', 
              'Si_20190121_1': 'First Si (exp)', 
              'Si_20190121_2': 'Final Si (exp)',
              'Si_20190129_1': 'First Si (exp)', 
              'Si_20190129_2': 'Final Si (exp)',
              'Ni2FeGa':'Ni$_2$FeGa (exp)', 
              'Co2FeGa':'Co$_2$FeGa (exp)', 
              'CoGa':'CoGa (exp)',
              'GaPdthinfilm' : 'GaPd thin film (exp)'}


# Titles for the spectra
plt_title_all = {'NP1': 'NP1' , 'NP2': 'NP2' , 'NP3':'NP3', 'TiO2':'TiO2', 
                 'Si1' : 'Si', 'Si1_0121' : 'Si_0121',
                 'NP4':'NP4', 'NP5':'NP5', 'NP6':'NP6'} 
plt_title_reduced_all = {k : f'{v}reduced' for k, v in plt_title_all.items()}
#{'NP1': 'NP1reduced' , 'NP2': 'NP2reduced' , 'NP3':'NP3reduced', 
#                         'TiO2':'TiO2reduced'} 

    
