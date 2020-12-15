# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 22:28 2016

@author: scott

This module provides badass functions for coordinating between complex
objects and easily readable files. The compromise for so awesome a toolbox
is that the tools themselves aren't easily readible. Good luck!

"""

from __future__ import print_function, division
import re
import datetime


float_match = r'\s[-]?\d+[\.]?\d*(e[-]?\d+)?\s'     #matches floats like -3.57e4

def group_lines(lines, indent='\t', removecomments=True):
    '''
    Groups indentation blocks into list elements. The line before the
    indentation block is included.
    '''
    if removecomments:
        lines = remove_comments(lines)
    nest = 0 #to keep track of how deep we are in the indentation block
    grouped_lines = []
    whitespace = re.compile(r'\s+')
    for (i,line) in enumerate(lines):
        #print(line)
        if len(re.sub(whitespace, '', line)) == 0:
            #print('... skipped!')
                #fix 17C23 to protect against empty lines
            continue
        line = line[:-1] #to get rid of the '\n'
        while line[0:nest] != indent * nest:
            nest -= 1
        group = eval('grouped_lines' + '[-1]' * nest)       #actually works!
        if line[0 : (nest + 1)] == indent * (nest + 1):
            nest += 1
            group[-1] = [group[-1], line[nest:]]
        elif len(line)>nest: #to drop empty lines
            group += [line[nest:]]
    return grouped_lines

def remove_comments(lines):
    new_lines = []
    for line in lines:
        if '#' in line:
            line = re.search('^.*\#', line).group()[:-1]
            if re.search(r'\w', line): #to drop lines that only have comments
                new_lines += [line]
        else:
            new_lines += [line] #I don't want to get rid of empty lines here
    return new_lines

def structure_to_lines(structure, nest=0, indent='\t', toplevel=False,
                       preamble=None, title_key=None):
    '''
    Formats a dictionary or list, which can have nested dictionaries or lists,
    into a set of properly indented lines to write to file.
    '''
    lines = []
    intro = ''
    if preamble is not None:
        intro += preamble

    if type(structure) is dict:
        if title_key in structure.keys(): #changed 'intro' to 'title_key' 16L14
            intro += indent + '-' + indent + structure[title_key]
        if not toplevel:
            if len(intro) == 0:
                intro += '<Dictionary>'
            lines += [nest * indent + intro + '\n']
        if not toplevel:
            nest += 1
        for (key, value) in structure.items():
            if key == title_key:
                continue
            lines += structure_to_lines(value, nest, indent, preamble=key,
                                     title_key='title')
    elif type(structure) is list:
        if not toplevel:
            if len(intro) == 0:
                intro += '<List>'
            lines += [nest * indent + intro + ':\n']
        if not toplevel:
            nest += 1
        for value in structure:
            if type(value) is tuple and len(value) == 2:
                lines += structure_to_lines(value[1], nest, indent, preamble=value[0])
                #added 16L14 to enable writing of lists of (key, value)
            else:
                lines += structure_to_lines(value, nest, indent)

    elif type(structure) is str:
        if len(intro) > 0:
            intro += ': '
        lines += [nest * indent + intro + structure + '\n']

    else:
        if len(intro) > 0:
            intro += indent + '=' + indent
        lines += [nest * indent + intro + str(structure) + '\n']

    return lines


def dictionary_to_lines(dictionary, indent='\t'):
    return structure_to_lines(dictionary, toplevel=True)


def grouped_lines_to_structure(lines, indent='\t'):
    '''
    The exact inverse of write_lines, but works on grouped lines!
    # as of 16L14, '\n' is removed by group_lines and not here.
    '''
    if type(lines) is str:
        line = lines.strip()
        if ':' in line: #then we've got a key and string value separated by a ': '
            key = re.search(r'^.+:', line).group()[:-1] #don't want the ':'
            try:
                value = re.search(r':.+$', line).group()[2:] #don't want the ': '
                            #note: use of '$' means '\n' isn't in group()!
            except AttributeError:
                value = None
            structure = (key, value)
        elif '=' in line: #then we've got a key and numerical value separated by a '\t=\t'
            key = re.search(r'^.+=', line).group()[:-2] #don't want the '\t='
            try:
                value = re.search(r'=.+$', line).group()[2:] #don't want the '=\t'
            except AttributeError:
                value = None
            try:
                value = eval(value)
            except (SyntaxError, NameError):
                print('wasn''t able to evaluate \'' + value + '\'')
            structure = (key, value)
        else:   #then we've got just a string
            structure = line

    elif type(lines) is list:
        title_line = lines[0]
        if ':' in title_line:  #then we want to make it into a list
            key = re.search(r'^.+:', title_line).group()[:-1]
            value = []
            for line in lines[1:]:
                value += [grouped_lines_to_structure(line)]
        else:       #then we want to make it into a dictionary
            value = {}
            if (indent + '-' + indent) in title_line:
                key = re.search(r'^.+' + indent + '-', title_line).group()[:-2]
                                            #don't want the '\t-'
                title = re.search(r'-' + indent + '.+$', title_line).group()[2:]
                                            #don't want the '-\t'
                value['title'] = title
            else:
                key = title_line
            for line in lines[1:]:
                item = grouped_lines_to_structure(line)
                try:
                    value[item[0]] = item[1]
                except IndexError:
                    print('missing something. line = ' + str(line))
        if key is '<list>:' or key is '<dictionary>':
            structure = value
        else:
            structure = (key, value)

    return structure


def lines_to_structure(lines, indent='\t', removecomments=True):
    '''
    Have to group lines seperately to not mess up with recursion.
    This function includes both steps.
    '''
#    print('lines:\n ' + str(lines))
    grouped_lines = group_lines(lines, indent, removecomments=removecomments)
        #this is necessary for it to treat the file as a single structure
#    print('grouped lines:\n ' + str(grouped_lines))
    return grouped_lines_to_structure(grouped_lines, indent)


def lines_to_dictionary(lines, indent='\t', removecomments=True):
    lines = ['<dictionary>\n'] + lines
    structure = lines_to_structure(lines, removecomments=removecomments)
    dictionary = structure[1] #structure[0] being '<dictionary>'
        #this is necessary for it to treat the file as a single structure
#    print('grouped lines:\n ' + str(grouped_lines))
    return dictionary


def lines_to_attributes(lines, obj, verbose=1, indent='\t'):
    if verbose:
        print('function \'lines_to_attributes\' at your service!')
    lines = ['<dictionary>\n'] + lines
    #gets lines_to_structure to treat it as one big dictionary
    attributes = lines_to_structure(lines, indent)[1]
    for (key, value) in attributes.items():
        setattr(obj, key, value)
    if verbose:
        print('function \'lines_to_attributes\' finished!')
    #return obj #shouldn't be necessary


def file_to_attributes(f, obj, verbose=1, indent='\t'):
    lines = f.readlines()
    return lines_to_attributes(lines, obj, verbose, indent)


def attributes_to_file(f, obj, verbose=1, indent='\t'):
    if verbose:
        print('function \'attributes_to_file\' at your service!')
    attributes = obj.__dict__.copy()
    for unwanted_key in ['file_lines', 'attr_status', '__str__']:
        if unwanted_key in attributes.keys():
            del(attributes[unwanted_key]) #so I don't write the whole file in itself
    lines = structure_to_lines(attributes, indent=indent)
    lines = [line[1:] for line in lines[1:]] #dropping '<dictionary>\n' and an indentation
    for line in lines:
        f.write(line)
    if verbose:
        print('function \'attributes_to_file\' finished!')
    #return f #shouldn't be necessary


def advanced_update(dict1, dict2, newstuff=True, oldstuff=False,
                 newkeys=[], oldkeys=[], mask=None):
    '''
    updates dict1 with dict2, but with options about which keys to add/update.
    Default values give a normal update.
    '''

    keys2 = list(dict2.keys()) # so that I don't have a dictionary changed size during iteration error
    if not newstuff:
        #then don't add new keys
        for key in keys2:
            if key not in dict1.keys() and key not in newkeys:
                dict2.pop(key, None)
    if oldstuff or len(oldkeys)>0:
        #then don't replace values of (evt. select) existing keys
        for key in keys2:
            if (oldstuff and key in dict1.keys()) or key in oldkeys:
                dict2.pop(key, None)
    if mask is not None:
        #then mask is a function evaluating to True if
        #a key shouldn't be added or updated.
        for key in keys2:
            if mask(key):
                dict2.pop(key)

    #print(type(dict2))

    dict1.update(dict2)
    return dict1

def update_lines(lines, dictionary, **kwargs):
    '''
    Does exactly what you'd think.
    '''
    dict1 = lines_to_dictionary(lines)
    newdict = advanced_update(dict1, dictionary, **kwargs)
    newlines = dictionary_to_lines(newdict)

    return newlines


def date_scott(date='today')  :
    '''
    Returns the date, default is today's, as Scott writes it.
    '''
    if date == 'today':
        a = datetime.date.today()
        year = a.year
        month = a.month
        day = a.day

    elif type(date) is str:
        if len(date) == 6: # 6-digit-integer dates format
            year = date[0:2]
            month = date[2:4]
            year = date[4:6]
        else: #if you insist
            return str(date)

    else:
        return str(date)
    date_string = '{0:2d}{1:1s}{2:2d}'.format(year%100, chr(ord('A') + month - 1), day)
    date_string = date_string.replace(' ', '0')

    return date_string



if __name__ == '__main__':
    from Molecules import Molecule
    #make an 'H2' molecule from the data file
    a = Molecule('H2')
    a.birthday = date_scott() #today is it's birthday!
    a.mood = 'Happy'    #make it happy
    #write everything about the happy H2 molecule to a file
    f = open('data/test.txt', 'w')
    attributes_to_file(f, a)
    f.close()
    #make a CO2 molecule from the data file...
    b = Molecule('CO2')
    print(b.name)
    #... and confuse the shit out it!
    f = open('data/test.txt', 'r')
    file_to_attributes(f, b) #its attributes are reset with the H2 data
    f.close()
    print(b.name) #now it thinks it's H2.
    print(b.__str__) #but deep down it's not
    print(b.mood) #At least it's happy!
    b.reset()
    print(b.name) #and now it's back to normal.






