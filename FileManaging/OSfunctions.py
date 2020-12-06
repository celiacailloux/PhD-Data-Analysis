#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 23:02:35 2019

@author: celiacailloux
"""
import os

def join_paths(path_part_one, path_part_two, path_part_three = '', path_part_four = ''):
    """
    This functions will join two paths and make sure that forward and backslash
    are indiferent. This is important when switching between OSx and Windows.
    Input: First part of the path and second part of the path
    Ouput: Joined path
    """
    return os.path.abspath(os.path.join(path_part_one, path_part_two, 
                                        path_part_three, path_part_four))
    

def create_directory(directory): 
    """
    This functions creates a DIRECTORY in the current path IF no directory 
    with such names already exists.
    Input: directory name
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        
"""
root :	= directory path, Prints out directories only from what you specified
dirs :	Prints out sub-directories from root. 
files:  Prints out all files from root and directories
"""

def find_files(file_name, directory_path):
    """
    Input: file name and the directory path of a directory, where you want to
    seek for files in the SUBFOLDER. 
    Output: file name path. 
    """
    rootdir = directory_path
    for subdir, dirs, files in os.walk(rootdir):
        if file_name in files:
                return os.path.join(subdir, file_name)
        
def find_subsubd(_dir, rootdir):
    """
    This function iterates over all DIRECTORIES (also sub) from a given PATH 
    (rootdir) and searches for a SPECIFIC directory (dir_name) and returns the 
    directory path (dir_name).
    Input: directory name and root directory path
    Output: directory path
    """
    for root, dirs, files in os.walk(rootdir):
        if _dir in root:
             dir_path = root
             return dir_path
        else:
             dir_path = ''
    if not dir_path:
        print('Error: didn\'t find the subdirectory \'{}\''.format(_dir))
        
def find_dir_containing_str(rootdir, _str):
    """
    This function iterates over DIRECTORIES from a given PATH (ROOTDIR) 
    and searches for a directory that CONTAINS a string given as input (_STR)
    """
    for root_dir in os.listdir(rootdir):
        if _str in root_dir:
            return os.path.join(rootdir,root_dir)
    print('No directory containing \'{}\' was found'.format(_str))
    
def find_all_txt_files_containing_str(rootdir, _str):
    """
    This function iterates over FILES in a DIRECTORY from a given PATH (ROOTDIR) 
    and searches and SAVES all files CONTAINING a string given as input (_STR)
    """
    file_names_containing_str = []

    print('\'.txt\' files containing {0} in \'{1}\'.....'.format(_str, os.path.basename(rootdir)))
    for subdir, dirs, files in os.walk(rootdir):     
        for file_name in files:
            if file_name.endswith('.txt'):
                if _str in file_name:
                    file_name_containing_str = os.path.join(subdir, file_name)
                    file_names_containing_str.append(file_name_containing_str)
                    print(os.path.basename(file_name_containing_str))
    if not file_names_containing_str:
        print('No txt files containing \'{}\' was found'.format(_str))
    print('\n')

    return file_names_containing_str

def find_all_csv_files_containing_str(rootdir, _str):
    """
    This function iterates over FILES in a DIRECTORY from a given PATH (ROOTDIR) 
    and searches and SAVES all files CONTAINING a string given as input (_STR)
    """
    file_names_containing_str = []

    print('\'.csv\' files containing {0} in \'{1}\'.....'.format(_str, os.path.basename(rootdir)))
    for subdir, dirs, files in os.walk(rootdir):     
        for file_name in files:
            if file_name.endswith('.csv'):
                if _str in file_name:
                    file_name_containing_str = os.path.join(subdir, file_name)
                    file_names_containing_str.append(file_name_containing_str)
                    print(os.path.basename(file_name_containing_str))
    if not file_names_containing_str:
        print('No txt files containing \'{}\' was found'.format(_str))
    print('\n')

    return file_names_containing_str

def find_all_xlsx_files_containing_str(rootdir, _str):
    """
    This function iterates over FILES in a DIRECTORY from a given PATH (ROOTDIR) 
    and searches and SAVES all files CONTAINING a string given as input (_STR)
    """
    file_names_containing_str = []

    print('\'.xlsx\' files containing \'{0}\' in {1}.....'.format(_str, os.path.basename(rootdir)))
    for subdir, dirs, files in os.walk(rootdir):     
        for file_name in files:            
            if file_name.endswith('.xlsx'):
                if _str in file_name:
                    file_name_containing_str = os.path.join(subdir, file_name)
                    file_names_containing_str.append(file_name_containing_str)
                    print(os.path.basename(file_name_containing_str))
    if not file_names_containing_str:
        print('No xlsx files containing \'{}\' was found'.format(_str))
    print('\n')

    return file_names_containing_str
    
        
def get_user_path():
    """ 
    This function return the user path, i.e. USER/CELIACAILLOUX or 
    USER/CESHUCA from where applications and files can be reached.
    """
    user_path = os.path.expanduser('~')
    return user_path

def create_file_path(user_path, XRD_data_dir, dir_path):
    file_path = os.path.join(user_path, XRD_data_dir, dir_path)
    return os.path.normpath(file_path)

def get_application_data_location(application):
    """
    This function returns a PATH containing a directory that is present in the
    user-application-path. Thus, Can be used for folders like Dropbox, Onedrive, 
    Google Drive, Mendelay, Sharelatex, ... etc.
    """
    path = os.path.expanduser(os.path.join('~',application))
    """
    NOTE os.path.expanduser() On Unix and Windows, return the argument with an 
    initial component of ~ or ~user replaced by that user’s home directory. 
    """
    if os.path.exists(path):
        return path
    path = find_dir_containing_str(os.path.expanduser('~'), application)
    if path:
        return path
'''_______________ Additional functions ___________________________________ '''
#file_dir = os.path.dirname(os.path.realpath(__file__))                      # this function determines the directory path in which this script is in


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


            
"""
Testing the different function
"""
#print(get_application_data_location('Test'))




            
            

    

