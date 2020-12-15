#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author         celiacailloux              

Main script to plot XRD patterns.

This script will read an csv file of an XRD pattern and plot it. In addition, 
reference pattern can be added to the plot. Finally, specific peak centers can
be inserted. 

"""

# custom-made modules
import auxiliary.functions as XRD
import submodules.plot_misc as pltF
from auxiliary.XRD_spectra_paths import *

# standard modules 
import matplotlib.pyplot as plt
import numpy as np
# from datetime import date

' Initialization ------------------------------------------------------------ '

# saves plotted plot WITHOUT showing showing it in the GUI
savefigures         = True
reduced_spectrum    = True     # mean reducing the x-range (i.e. 2theta range)
x1_lim, x2_lim      = 30, 80
x_min_loc, y_min_loc= 5,4 


' Choose data --------------------------------------------------------------- '



# choose which measureed XRD patterns to plot
# database can be found in auxiliary/XRD_spectra_paths.py in files_all
wanted_exps = ['example',
                # 'SP14_ZnO_273K']# 
                ]

# from all experiment extract chosen experiments              
exps = \
    XRD.dict_values_to_list(initial_dict = files_all, 
                            specified_keys = wanted_exps)
    
# choose which reference XRD patterns to plot
# database can be found in auxiliary/XRD_spectra_paths.py in ref_files_all
wanted_refs = ['PdZn']
refs = \
    XRD.dict_values_to_list(initial_dict = ref_files_all, 
                            specified_keys = wanted_refs)

    
# insert a title & comment. graph will be saved with this name
title = XRD.get_plot_title(wanted_exps, wanted_refs)
comment = ''

peak_centers = {'(111)'     : 41.3,
                '(211)'     : 44.3,
                }
print('\n')
print('Measured XRD pattern to be plotted: ')
for XRD_pattern in wanted_exps:
    print('\t', XRD_pattern)
print('Measured XRD pattern to be plotted: ')
for XRD_ref_pattern in wanted_refs:
    print('\t', XRD_ref_pattern)
    
' Plotting ------------------------------------------------------------------ '

N = (len(exps) + len(refs))
color = pltF.color_maps(color_map = 'jkib')

fig_shift = 0
fig_shift_add = 0.5#0.3
text_shift = 0.05
# should be determined by measuring on a well defined crystal
# with known crystal lattice, i.e. Si. If not measured use 0 as default value
angle_shift = 0 
# a number used to scaled the reference pattern smaller (<1) or larger (>1)
scale_ref_spec = 1 

if reduced_spectrum:    
    width   = (x2_lim-x1_lim)/10
    height  = N
    fig     = plt.figure(figsize = (width,height))
    config  = 'XRD_zoom' 
    x_text  = x2_lim
else:
    fig     = plt.figure(figsize = (6,N))
    config  = 'XRD'
    x_text  = None
    
ax = fig.add_subplot(1,1,1)

# ________ plot experimental patterns
for exp,n in zip(exps,range(0,len(exps))):
        spectrum    = XRD.read_exp_spectrum(exp[0])
        y           = np.subtract(spectrum[1],fig_shift)
        ax.plot(spectrum[0].add(angle_shift), 
                y, 
                label=exp[1], 
                color = color(n/N), 
                linewidth = 2)
        y_text = y.min()-text_shift
        pltF.global_text(ax, 
                          text=exp[1], 
                          config = config, 
                          x = x_text, 
                          y = y_text, 
                          color =  color(n/N))
        fig_shift += fig_shift_add

# ________plot reference patterns     
for ref,m in zip(refs,range(0,len(refs))):
        spectrum = XRD.read_ref_spectrum(ref[0])
        y = np.subtract(spectrum[1].mul(scale_ref_spec),fig_shift)
        ax.plot(spectrum[0], 
                y,
                label=ref[1], 
                color = color((n+m+1)/N), 
                linewidth = 2)
        y_text = y.min()-text_shift
        pltF.global_text(ax, 
                          text=ref[1], 
                          config = config, 
                          x = x_text, 
                          y = y_text, 
                          color =  color((n+m+1)/N))
        
        fig_shift += fig_shift_add

if bool(peak_centers):
    for hkl, peak_center in peak_centers.items():
        ax.axvline(x = peak_center, 
                    linewidth=1, 
                    color='k', 
                    alpha = 0.5, 
                    linestyle = '--', 
                    zorder = 0)
        print('Adding dotted line at peak center at: {} 2\u03F4'.format(peak_center))

' settings for plotting ----------------------------------------------------- '

pltF.global_settings(ax) 
pltF.global_minor_locator(ax, x_locator = x_min_loc, y_locator = y_min_loc)
pltF.XRD_global(ax, label = False)

if reduced_spectrum:
    ax.set_xlim(x1_lim, x2_lim)
    ax.set_ylim(bottom = -0.9*N*fig_shift_add)
    x_range_str = XRD.convert_x_range_to_str(x1_lim, x2_lim)
    if savefigures:
        pltF.global_savefig(fig, plt_title = title, 
                            addcomment = comment + x_range_str)
        plt.close('all')
    else:
        plt.show()
else:
    ax.set_xlim(20,90)
    ax.set_ylim(top = 1.5, bottom = -fig_shift+fig_shift_add/2)
    if savefigures:
        pltF.global_savefig(fig, plt_title = title, addcomment = comment)
        plt.close()
    else:
        plt.show('all')
         


