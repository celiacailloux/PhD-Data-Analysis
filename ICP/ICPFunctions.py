#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 20:44:10 2019

@author: celiasullcacailloux
"""
import pandas as pd
from string import digits
import os

def get_elements(choice_of_elem):
    #print(os.listdir())
    #filename = '/Users/celiasullcacailloux/OneDrive - Danmarks Tekniske Universitet/Modules/ICP/Elements.xlsx' #MAC
    #filename = r'C:\Users\ceshuca\OneDrive - Danmarks Tekniske Universitet\Modules\ICP\Elements.xlsx' # Windows
    filename = 'Elements.xlsx' # Windows
    file_dir = os.path.dirname(os.path.realpath(__file__))                      # this function determines the directory path in which this script is in
    file_path = os.path.join(file_dir, filename)
    print(file_path)
    
    df = pd.read_excel(file_path, index_col=0)
    elem_dict = df.to_dict('records')[0]
    #corrected_dict = { k.replace(':', ''): v for k, v in ori_dict.items() }
    corrected_dict = { k.replace(' (KED)',''): v for k, v in elem_dict.items() }
    remove_digits = str.maketrans('', '', digits)
    corrected_dict = { k.translate(remove_digits): v for k, v in corrected_dict.items() }

    return {elem: corrected_dict[elem] for elem in choice_of_elem}
#
#elem = get_elements(choice_of_elem = ['Mg','Pb'])
#print(elem)