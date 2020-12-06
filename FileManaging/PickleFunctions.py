# -*- coding: utf-8 -*-
"""
Created on Thu May 14 09:32:17 2020

@author: ceshuca

More on python pickles https://wiki.python.org/moin/UsingPickle
"""

import pickle
from datetime import date


def save_as_pickle(pkl_data, pkl_name):    
    pkl_filename = str(date.today())+ '_' + pkl_name + '.pickle'
    with open(pkl_filename, 'wb') as f:
        pickle.dump(pkl_data, f)
        
def get_saved_pickle(pkl_name):
    pkl_filename = str(date.today())+ '_' + pkl_name + '.pickle'
    with open(pkl_filename, 'rb') as f:
        pkl_data = pickle.load(f)
    
    return pkl_data