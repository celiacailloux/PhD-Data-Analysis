#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 23:02:35 2019

@author: celiacailloux
"""
import os

def create_directory(directory): #if the directory doesn't already exist!
    if not os.path.exists(directory):
        os.makedirs(directory)

''' Input: file name and the directory path of a directory, where you want to
seek for files in the SUBFOLDER. 
Output: file name path. '''
def find_files(file_name, directory_path):
    rootdir = directory_path
    for subdir, dirs, files in os.walk(rootdir):
        if file_name in files:
                return os.path.join(subdir, file_name)
        
            
''' Input: file name and the directory path of a directory, where you want to
seek for files in the SUBFOLDER. 
Output: file name path. '''

#root :	Prints out directories only from what you specified
#dirs :	Prints out sub-directories from root. 
#files:  Prints out all files from root and directories
def find_subsubd(dir_name, directory_path):
    rootdir = directory_path
    #print(directory_path)

    for root, dirs, files in os.walk(rootdir):
        if dir_name in root:
             dir_name_path = root
             #os.path.join(root, dir_name)
             #print(dir_name_path)
             return dir_name_path
        else:
             dir_name_path = ''
    if not dir_name_path:
        print('Error: didn\'t find subdirectory with the name: {}'.format(dir_name))


'''_______________ Instrument specific ____________________________________ '''

''' Input: file name and the directory path of a directory, where you want to
seek for files in the SUBFOLDER. 
Output: file name path. '''
def ECLab_find_txt_files(rootdir, exp_type):
    path_files = []
    for root, dirs, files in os.walk(rootdir):

        if not os.listdir(rootdir):
            print('!!!! Error !!!! \nNo files in: {}'.format(rootdir))
        else:
            for file in files:                
                if 'CP' in exp_type or 'OCV' in exp_type:                  
                    if file.endswith("CP_C01.txt") or file.endswith("OCV_C01.txt"):
                        #print(file)
                        
                        
                        path_file = os.path.join(root, file)
                        path_files.append(path_file)  
                elif 'CV' in exp_type:
                    if file.endswith("CVA_C01.txt"):
                        path_file = os.path.join(root, file)
                        #print('******* Returned subsub directory: \'{0}\' and path: \'{1}\' for experiment: \'{2}\''.format(subsub_d, path_file, choice_of_exp))
                        path_files.append(path_file)
#                if exp_type == 'CP':
#                    if file.endswith("CP_C01.txt"):
#                        print(file)
#                        path_file = os.path.join(root, file)
#                        path_files.append(path_file)  
#                elif exp_type == 'CV':
#                    if file.endswith("CVA_C01.txt"):
#                        path_file = os.path.join(root, file)
#                        #print('******* Returned subsub directory: \'{0}\' and path: \'{1}\' for experiment: \'{2}\''.format(subsub_d, path_file, choice_of_exp))
#                        path_files.append(path_file)
    if not path_files:
        print('!!!! Error !!!! \nCouldn\'t find experiment types {0} in folder {1}'.format(exp_type, rootdir))
    return path_files

            



            
            

    

