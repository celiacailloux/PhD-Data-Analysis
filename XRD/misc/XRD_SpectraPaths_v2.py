#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 17:43:22 2019

@author: celiacailloux
"""
#import os
import OSfunctions as osfunc
from OSfunctions import create_file_path,  get_user_path
#______________________________________________________________________________
# Experimetnal spectra paths in a dictionary


# Experimental spectra paths
# CSV files

''' ____________________________________________________________ File paths ''' 
user_path = osfunc.get_user_path()
XRD_data_dir    = 'OneDrive - Danmarks Tekniske Universitet/PhD/Data/XRD/'
XRD_ref_dir     = 'OneDrive - Danmarks Tekniske Universitet/Modules/XRD/XRD Reference Spectra/'

" add exp "
# "Experimental files. Below are the file paths for the experimental files which"
# "are the put into a dictionary (files_all) that contains the file path and label."
Pd              = osfunc.create_file_path(user_path, XRD_data_dir,'20191010 GIXRD Pd wobbled\Pd thin film GIXRD 20to90deg Omega0,5deg 10HrScan.csv')
PdZn_873K       = osfunc.create_file_path(user_path, XRD_data_dir,'20191016 Pdzn 873K/GIXRD 20to90deg Omega0,5deg 10HrScan_1.csv')
PdZn_523K       = osfunc.create_file_path(user_path, XRD_data_dir, '20191024 PdZn 523K/PdZn 523K GIXRD 20to90deg Omega0,5deg 10HrScan_1.csv')
PdZn_623K       = osfunc.create_file_path(user_path, XRD_data_dir, '20191028 PdZn 623K/PdZn 623 K GIXRD 20to90deg Omega0,5deg 10HrScan_1_20191028.csv')
PdZn_623K_NF    = osfunc.create_file_path(user_path, XRD_data_dir, '20191031 PdZn 623K no flow dep/PdZn 623 K no flow dep GIXRD 20to90deg Omega0,5deg 10HrScan_1_20191031.csv')
PdZn_623K_NF_SD = osfunc.create_file_path(user_path, XRD_data_dir, '20191101 Pd Zn 623K no flow new small ceramic boat/PdZn 623 K no flow dep small cer boat GIXRD 20to90deg Omega0,5deg 10HrScan_1_20191101.csv')
PdZn_723K_NF_SD = osfunc.create_file_path(user_path, XRD_data_dir, '20191104 PdZn 723K NF SB/PdZn 723K NF SB 20191104 GIXRD 20to90deg Omega0,5deg 10HrPrScan_1.csv')
PdZn_673K_NF    = osfunc.create_file_path(user_path, XRD_data_dir, '20191107 PdZn 673K NF LD/PdZn 673K NF LD 20191107 GIXRD 20to90deg Omega0,5deg 5HrPrScan_1.csv')
PdZn_648K_NF    = osfunc.create_file_path(user_path, XRD_data_dir, '20191107 PdZn 648K NF LD/PdZn 648K NF LD 20191107 GIXRD 20to90deg Omega0,5deg 5HrPrScan_1.csv')
Pd_noZn_623K_NF = osfunc.create_file_path(user_path, XRD_data_dir, '20191119 Pd(Si) 623K/Pd(Si) pos3 20191119 GIXRD 20to90deg Omega0,5deg 5HrScan_1.csv')
Si100_273K      = osfunc.create_file_path(user_path, XRD_data_dir, '20191119 Si(100)/Si(100) 20191119 GIXRD 20to90deg Omega0,5deg 5HrScan_1.csv')
Pd_SP12_273K    = osfunc.create_file_path(user_path, XRD_data_dir, '20191122 Pd(TiO2Ti)/20191122 Pd (TiO2Ti) GIXRD 20to90deg Omega0,6deg 5HrScan_1.csv')
PdZn13_623K     = osfunc.create_file_path(user_path, XRD_data_dir, '20191128 PdZn 623K #13/20191128 PdZn #13 GIXRD 20to90deg Omega0,45deg 10HrScan_1.csv')
SP14_ZnO_273K   = osfunc.create_file_path(user_path, XRD_data_dir, '20191202 ZnO (44nm) SP#14/20191202 ZnO (44nm) SP#14  GIXRD 20to90deg Omega0,35deg 10HrScan_1.csv')                                       
PdZnO_273K      = osfunc.create_file_path(user_path, XRD_data_dir, '20191203 PdZnO SP#15/20191203 PdZnO SP#15 GIXRD 20to90deg Omega0,4deg 5HrScan_1.csv')                                      
PdZn14_623K     = osfunc.create_file_path(user_path, XRD_data_dir, '20191203 PdZn#14 623K/20191203 PdZn#14 623K  GIXRD 20to90deg Omega0,4deg 5HrScan_1.csv')
PdZn15_723K     = osfunc.create_file_path(user_path, XRD_data_dir, '20191206 PdZnO (PdZn15, SP15)/20191206 PdZn15 GIXRD 20to90deg Omega0,4deg 1,5HrScan_1.csv')
PdZn16_773K     = osfunc.create_file_path(user_path, XRD_data_dir, '20191216 ZnOPd (PdZn16, SP17)/20191216 PdZn16 GIXRD 20to90deg Omega0,4deg 10HrScan_1.csv')                                          
PdZn17_623K     = osfunc.create_file_path(user_path, XRD_data_dir, '20191217 ZnOPd (PdZn17, SP17)/20191217 PdZn17 GIXRD 20to90deg Omega0,5deg 5HrScan_1.csv')
ZnO_SP20_RT     = osfunc.create_file_path(user_path, XRD_data_dir, '20191217 ZnOPd (SP20)/20191217 SP20 GIXRD 20to90deg Omega0,4deg 2,5HrScan_1.csv')
PdZn18_623K     = osfunc.create_file_path(user_path, XRD_data_dir, '20191217 PdZn18 (SP19)/20191217 PdZn18 GIXRD 20to90deg Omega0,45deg 2,5HrScan_1.csv')
PdZn22_450C     = osfunc.create_file_path(user_path, XRD_data_dir, '20200116 PdZnO (PdZn22, SP29)/20200116 PdZnO (PdZn22) GIXRD 20to90deg Omega0,4deg 3HrScan_1.csv')
PdZn23_450C     = osfunc.create_file_path(user_path, XRD_data_dir, '20200116 PdZnO (PdZn23, SP31)/20200116 PdZnO (PdZn23) GIXRD 20to90deg Omega0,4deg 3HrScan_1.csv')
PdZn25_2x450C   = osfunc.create_file_path(user_path, XRD_data_dir, '20200210/PdZn25 Pd1Zn2/20200210 PdZn25 Pd1Zn2 GIXRD 20to90deg Omega0,4deg 3HrScan_1.csv')
PdZn26_450C     = osfunc.create_file_path(user_path, XRD_data_dir, '20200210/PdZn26 Pd1Zn1/20200210 PdZn26 Pd1Zn1 GIXRD 20to90deg Omega0,5deg 2,5HrScan_1.csv')
PdZn20_Al2O3    = osfunc.create_file_path(user_path, XRD_data_dir, '20200210/SP32 Al2O3 on Pd1Zn2/20200210 SP32 Al2O3 on Pd1Zn2 GIXRD 20to90deg Omega0,4deg 2,5HrScan_1.csv')
PdZn28_450C     = create_file_path(user_path, XRD_data_dir, '20200304 PdZn28 Pd1Zn1/20200304 PdZn28 Pd1Zn1 GIXRD 30to90deg Omega0,5deg 2,0HrScan_1.csv')
PdZn28_long_scan= create_file_path(user_path, XRD_data_dir, r'20200609 PdZn28 Pd1Zn1/SP#49(Celia) PdZn#48(11) GIXRD 20to90deg Omega0,60deg 16HrScan_1.csv')
# = create_file_path(user_path, XRD_data_dir,r'')

" add exp "
# Contains key, file_path, label
files_all = {'Pd': [Pd, 'Pd/Si (100 nm)'],
                    'PdZn_873K'         : [PdZn_873K,       'PdZn (873 K)'],
                    'PdZn_523K'         : [PdZn_523K,       'PdZn (523 K)'],
                    'PdZn_623K'         : [PdZn_623K,       'PdZn (623 K)'],
                    'PdZn_623K_NF'      : [PdZn_623K_NF,    'PdZn (623 K, NF)'],
                    'PdZn_623K_NF_SD'   : [PdZn_623K_NF_SD, 'PdZn (623 K, NF, SD)'],
                    'PdZn_723K_NF_SD'   : [PdZn_723K_NF_SD, 'PdZn (723 K, NF, SD)'],
                    'PdZn_673K_NF'      : [PdZn_673K_NF,    'PdZn (673 K, NF)'],
                    'PdZn_648K_NF'      : [PdZn_648K_NF,    'PdZn (648 K, NF)'],
                    'Pd_noZn_623K_NF'   : [Pd_noZn_623K_NF, 'Pd/Si(100) (623K)'],
                    'Si100_273K'        : [Si100_273K,      'Si(100)'],
                    'PdZn13_623K'       : [PdZn13_623K,     'PdZn/TiO$_2$ (623 K)'],
                    'Pd_SP12_273K'      : [Pd_SP12_273K,    'Pd thin film'],#'Pd/TiO2/Ti RT (SP12)'],#'Pd/TiO2/Ti (273 K)'],
                    'SP14_ZnO_273K'     : [SP14_ZnO_273K,        'ZnO/TiO2 RT (SP14)'],#'ZnO/TiO2 (273 K)'],
                    'PdZnO_273K'        : [PdZnO_273K,      'Pd/ZnO/TiO2 RT (SP15)'],#'PdZnO (273 K)'],
                    'PdZn14_623K'       : [PdZn14_623K,     'Pd/ZnO/TiO2 350C (PdZn14)'],#'PdZnO (623 K)']}
                    'PdZn15_723K'       : [PdZn15_723K,     'Pd/ZnO/TiO2 450C (PdZn15)'],
                    'PdZn16_773K'       : [PdZn16_773K,     'ZnO/Pd/TiO2/Ti (PdZn16)'],
                    'PdZn17_623K'       : [PdZn17_623K,     'ZnO/Pd/TiO2/Ti (PdZn17)'],
                    'ZnO_SP20_RT'       : [ZnO_SP20_RT,     'ZnO/Pd/TiO2/Ti RT (SP20)'],
                    'PdZn18_623K'       : [PdZn18_623K,     'PdZn CVD 350 (PdZn18)'],
                    'PdZn22_450C'       : [PdZn22_450C,     'PdZn(1:2) (PdZn22)'],
                    'PdZn23_450C'       : [PdZn23_450C,     'PdZn(2:1) (PdZn23)'],
                    'PdZn25_2x450C'     : [PdZn25_2x450C,   'PdZn(1:2) (PdZn25)'],
                    'PdZn26_450C'       : [PdZn26_450C,     'PdZn(1:1) (PdZn26)'],
                    'PdZn20_Al2O3'      : [PdZn20_Al2O3,    'PdZn(1:2) (SP32,PdZn20)'],
                    'PdZn28_450C'       : [PdZn28_450C,     'PdZn(1:1) (PdZn28)'],
                    'PdZn28_long_scan'  : [PdZn28_long_scan,'PdZn(1:1)']}#'PdZn(1:1) (PdZn28)']}


''' ____________ Reference files ___________________________________________''' 

refPd           = osfunc.create_file_path(user_path, XRD_ref_dir,'Pd/powderpattern_xy_collCode#64922.csv')
refPd2_3Zn10    = osfunc.create_file_path(user_path, XRD_ref_dir,'Pd2.352Zn10.648/powderpattern_xy_collCode#171749.csv')                                          
refZnO_NaCl     = osfunc.create_file_path(user_path, XRD_ref_dir,'ZnO NaCl/powderpattern_xy_collCode#38222.csv')
refZnO_Wurtzite = osfunc.create_file_path(user_path, XRD_ref_dir,'ZnO Wurtzite/powderpattern_xy_collCode#41488.csv')
refPd2Si        = osfunc.create_file_path(user_path, XRD_ref_dir,'Pd2Si/powderpattern_xy_collCode#648847.csv')
refSiO2         = osfunc.create_file_path(user_path, XRD_ref_dir, 'SiO2/powderpattern_xy_collCode#181309.csv')
refPdZn         = osfunc.create_file_path(user_path, XRD_ref_dir, 'PdZn/powderpattern_xy_collCode#180143.csv')
refPd81Zn19     = osfunc.create_file_path(user_path, XRD_ref_dir, 'Pd81Zn19/powderpattern_xy_collCode#105757.csv')                                         
refZn           = osfunc.create_file_path(user_path, XRD_ref_dir, 'Zn/powderpattern_xy_collCode#52543.csv')
refPdZn2        = osfunc.create_file_path(user_path, XRD_ref_dir, 'PdZn2/powderpattern_xy_collCode#105753.csv')
refPd2Zn        = osfunc.create_file_path(user_path, XRD_ref_dir, 'Pd2Zn/powderpattern_xy_collCode#649139.csv')                                          

ref_files_all = {'Pd': [refPd, 'Pd (ref)'] , 
                        'Pd2_3Zn10': [refPd2_3Zn10, 'Pd$_{2.352}$Zn$_{10.648}$ (ref)'],
                        'ZnO_NaCl': [refZnO_NaCl, 'ZnO [NaCl] (ref)'], 
                        'ZnO_Wurtzite'  : [refZnO_Wurtzite, 'ZnO [Wurtzite] (ref)'],
                        'Pd2Si'         : [refPd2Si, 'Pd$_2$Si (ref)'],
                        'SiO2'          : [refSiO2, 'SiO$_2$ (ref)'],
                        'PdZn'          : [refPdZn, 'PdZn (ref)'],
                        'Pd81Zn19'      : [refPd81Zn19, 'Pd$_{0.81}$Zn$_{0.19}$ (ref)'],
                        'Zn'            : [refZn,       'Zn (ref)'], 
                        'PdZn2'         : [refPdZn2,   'PdZn$_2$ (ref)'],
                        'Pd2Zn'        : [refPd2Zn,   'Pd$_2$Zn (ref)']}
    

