#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 09:11:27 2019

@author: celiacailloux
"""

exp_paths = {'20190321 Cu C anode Trial 1 KHCO3'    : '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC Lab/CO potential shift/20190321 Cu/20190321 Cu C anode Trial 1 KHCO3/Trial 1_03_CVA_C01.txt',
             '20190321 Cu C anode Trial 2 KHCO3'    : '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC Lab/CO potential shift/20190321 Cu/20190321 Cu C anode Trial 2 KHCO3/Trial 2_03_CVA_C01.txt',
             '20190607 Cu thin film CV 1'           : '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190607 Cu thin film/txts/CV 1_C01.mpt',
             '20190607 Cu thin film CV 2'           : '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190607 Cu thin film/txts/CV 2_C01.mpt',
             '20190607 Cu thin film CV 3'           : '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190607 Cu thin film/txts/CV 3_C01.mpt',
             '20190607 Cu thin film CV 4'           : '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190607 Cu thin film/txts/CV 4_C01.mpt',
             '20190607 Cu thin film CV 5 CO'        : '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190607 Cu thin film/txts/CO CV 1_C01.mpt',
             '20190607 Cu thin film CO CA 01'       : '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190607 Cu thin film/txts/CO CA 1_01_CA_C01.mpt',
             '20190607 Cu thin film CO CA 02'       : '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190607 Cu thin film/txts/CO CA 1_02_CA_C01.mpt',
             '20190607 Cu thin film CO OCV 03'       : '/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190607 Cu thin film/txts/CO CA 1_03_OCV_C01.mpt',
             '20190611 Cu:TiO2 CV 1':'/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190611 Cu:TiO2/txt/CV 1_C01.mpt',
             '20190611 Cu:TiO2 CV 2 CO':'/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190611 Cu:TiO2/txt/CO CV 1_C01.mpt',
             '20190611 Cu:TiO2 CV 3 CO':'/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190611 Cu:TiO2/txt/CO CV 2_C01.mpt',
             '20190613 TiO2 CV 1':'/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190613 TiO2/txt/Test CV_C01.mpt',
             '20190613 TiO2 CV 2 CO':'/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190613 TiO2/txt/CO CV_C01.mpt',
             '20190613 GaPd thin film  CV 1 He':'/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190619 GaPd thin film/txt/03 CV 7 He_02_CV_C01.mpt',
             '20190613 GaPd thin film  CV 2 CO':'/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190619 GaPd thin film/txt/06 CV 3 CO_CV_C01.mpt',
             '20190613 GaPd thin film  CO max pot 1':'/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190619 GaPd thin film/txt/09 CA CO max pot 2_01_CA_C01.mpt',
             '20190613 GaPd thin film  CO max pot 2':'/Users/celiacailloux/Dropbox/Studium/12_semester_ MasterThesis/EC-MS/20190619 GaPd thin film/txt/09 CA CO max pot 2_02_CA_C01.mpt'
             }







exp_details = {'20190607 Cu thin film'      : {'PEIS': 86},
               '20190611 Cu/TiO2'           : {'PEIS': 80},
               '20190613 TiO2'              : {'PEIS': 100},                    # PEIS was not conducted
               '20190619 GaPd thin film'    : {'PEIS': 119},
               }





