#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 20:44:10 2019

@author: celiasullcacailloux
"""
import pandas as pd
from string import digits
import os

def get_elements():
    #print(os.listdir())
    filename = '/Users/celiasullcacailloux/Library/Mobile Documents/com~apple~CloudDocs/Documents/Modules/ICP/Elements.xlsx'
    df = pd.read_excel(filename, index_col=0)
    elem_dict = df.to_dict('records')[0]
    #corrected_dict = { k.replace(':', ''): v for k, v in ori_dict.items() }
    corrected_dict = { k.replace(' (KED)',''): v for k, v in elem_dict.items() }
    remove_digits = str.maketrans('', '', digits)
    corrected_dict = { k.translate(remove_digits): v for k, v in corrected_dict.items() }
    return corrected_dict
    

elem = get_elements()
print(elem)