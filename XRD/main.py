#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created         Jan 30 16:39:30 2019   
                                         
@author         celiacailloux              

Sample          PdZn28 PdZn(1:1)
"""

import auxiliary.functions as XRD
import submodules.plot_misc as pltF
# ##from xrd_spectra_paths import plt_title_all, plt_title_reduced_all, ref_files_all, files_all, ref_labels_all, labels_all

#from .PhD_Data_Analysis.submodules.plot.plot import plotting_functions as pltF

# from XRD_SpectraPaths_v2 import files_all, ref_files_all #ref_labels_all, files_all, labels_all

# import matplotlib.pyplot as plt
# import numpy as np
from datetime import date

def _ytext(y_min, XRD_plot_fig_shift_add):
    """
    This function determines the y-coordinate for the label text
    inserted in the XRD plots.
    """
    return y_min-XRD_plot_fig_shift_add*0.05 
    
def convert_x_range_to_str(x1_lim, x2_lim):
    
    " Converts XRD x1_lim and x2_lim into a nice string to attach to "
    " the file name of the plot. "

    return ', x_range.' + str(x1_lim) + '.' + str(x2_lim) + ','

def get_plot_title(wanted_exps, wanted_refs):
    
    date_str = str(date.today())
    wanted_exps_str = ' ' + ' '.join([str(exp.split('_', 1)[0]) for exp in wanted_exps])
    wanted_ref_str = ', ref. ' + ' '.join([str(exp) for exp in wanted_refs])
    #', Pd RT, ZnO(TiO2), Si100'
    print(wanted_exps_str)
    return date_str + wanted_exps_str + wanted_ref_str

# ##plt_title = plt_title_all[catalyst]
# ##plt_title_reduced = plt_title_reduced_all[catalyst]
# #''' Experimental files 
# #All experimental files are in XRD_SpectraPaths '''
# #exps = [files_all[catalyst]] 

# " change "
# savefigures = True
# entire_spectrum = True
# reduced_spectrum = False



# " Get samples & references by choosing. The actual measured and reference XRD "
# " patterns are collected from \"XRD_SpectraPaths_v2\"."
# #     * the desired MEASURED XRD patterns (wanted_exps). The list op possible
# #       spectra is listed below.
# #     * the desired REFERENCE from the ICSD database (wanted_refs)
    
# #     Measured "reference" spectra are:
# #         ZnO:    'ZnO_273K'
# #         Si100:  'Si100_273K'
# #         Pd:     'Pd_SP12_273K' 
    
# #     Database reference spectra are:
# #         PdZn:       'PdZn'
# #         Pd2_3Zn10:  'Pd2_3Zn10'
# #         Pd81Zn19:   'Pd81Zn19'
# #         ZnO_NaCl:   'ZnO_NaCl'
# #         Zn:         'Zn'
# #         PdZn:       'PdZn' 
# #         Pd2Zn:      'Pd2Zn' 

# " change "
# wanted_exps = ['PdZn28_long_scan', 
#                'Pd_SP12_273K', 
#                 # 'SP14_ZnO_273K']#, 
#                'Si100_273K']
               
# exps = XRD.dict_values_to_list(initial_dict = files_all, specified_keys = wanted_exps)
# wanted_refs = ['PdZn']
# refs = XRD.dict_values_to_list(initial_dict = ref_files_all, specified_keys = wanted_refs)

    
# " change "
# # "Insert a title for the file name of the plot (png) "
# title = get_plot_title(wanted_exps, wanted_refs)
# comment = ''


# " ______________________________________________________________ Plotting "

# N = (len(exps) + len(refs))
# color = pltF.color_maps(color_map = 'jkib')

# fig_shift = 0
# fig_shift_add = 0.5#0.3
# text_shift = 0.05
# angle_shift = 0 #-0.5867436830000017 #determined by Si
# scale_ref_spec = 1


    
# if entire_spectrum:
#     " Plotting entire spectrum x = [0:90] "

#     fig = plt.figure(figsize = (6,N))
#     ax = fig.add_subplot(1,1,1)
    
    
#     # ________ plot experimental spectra
#     for exp,n in zip(exps,range(0,len(exps))):
#             spectrum = XRD.read_exp_spectrum(exp[0])
#             y = np.subtract(spectrum[1],fig_shift)
#             ax.plot(spectrum[0].add(angle_shift), y, label=exp[1], color = color(n/N), linewidth = 2)
#             y_text = y.min()-text_shift
#             pltF.global_text(ax, text=exp[1], config = 'XRD', y = y_text, color =  color(n/N))
#             fig_shift += fig_shift_add

    
#     # ________plot reference spectra        
#     for ref,m in zip(refs,range(0,len(refs))):
#             spectrum = XRD.read_ref_spectrum(ref[0])
#             y = np.subtract(spectrum[1].mul(scale_ref_spec),fig_shift)
#             ax.plot(spectrum[0], y,label=ref[1], color = color((n+m+1)/N), linewidth = 2)
#             y_text = y.min()-text_shift
#             pltF.global_text(ax, text=ref[1], config = 'XRD', y = y_text, color =  color((n+m+1)/N))
           
#             #ax.plot(spectrum[0],np.subtract(spectrum[1].mul(0.2),fig_shift),label=ref[1], color = color(6/N))
#             fig_shift += fig_shift_add
    
#     " _____________________________________________________ Plotting Settings "
#     pltF.global_settings(ax)
#     pltF.global_minor_locator(ax, x_locator = 5, y_locator = 4)
#     ax.set_ylim(top = 1.5, bottom = -fig_shift+fig_shift_add/2)
#     ax.set_xlim(20,90)
    
#     " change "
#     ax.axvline(x = 41.3, linewidth=1, color='k', alpha = 0.5, linestyle = '--', zorder = 0)
#     ax.axvline(x = 44.3, linewidth=1, color='k', alpha = 0.5, linestyle = '--', zorder = 0)
    
#     pltF.XRD_global(ax, label = False)
#     if savefigures:
#         pltF.global_savefig(fig, plt_title = title, addcomment = comment)
#     #pltF.XRD_global(ax, label = True)
#     #if savefigures:
#     #    pltF.global_savefig(fig, plt_title = title + '_label', addcomment = comment)
#     plt.tight_layout()

# if reduced_spectrum:
    
#     "Plotting reduced spectrum "
    
#     x1_lim, x2_lim = 30, 80
#     width = (x2_lim-x1_lim)/10
#     height = N
  
#     fig = plt.figure(figsize = (width,height))
#     ax = fig.add_subplot(1,1,1)
    

    
#     # ________ plot experimental spectra
#     for exp,n in zip(exps,range(0,len(exps))):
#         spectrum = XRD.read_exp_spectrum(exp[0])
#         y = np.subtract(spectrum[1],fig_shift)
#         ax.plot(spectrum[0].add(angle_shift), y, label=exp[1], color = color(n/N), linewidth = 2)
#         y_text = _ytext(y.min(),fig_shift_add)
#         pltF.global_text(ax, text=exp[1], config = 'XRD_zoom', x = x2_lim, y = y_text, color =  color(n/N))
#         fig_shift += fig_shift_add

#     # ________plot reference spectra        
#     for ref,m in zip(refs,range(0,len(refs))):
#         spectrum = XRD.read_ref_spectrum(ref[0])
#         y = np.subtract(spectrum[1].mul(scale_ref_spec),fig_shift)
#         ax.plot(spectrum[0], y,label=ref[1], color = color((n+m+1)/N), linewidth = 2)
#         y_text = _ytext(y.min(),fig_shift_add)
#         pltF.global_text(ax, text=ref[1], config = 'XRD_zoom', x = x2_lim, y = y_text, color =  color((n+m+1)/N))
       
#         #ax.plot(spectrum[0],np.subtract(spectrum[1].mul(0.2),fig_shift),label=ref[1], color = color(6/N))
#         fig_shift += fig_shift_add

#     pltF.global_settings(ax)
#     pltF.global_minor_locator(ax, x_locator = 5, y_locator = 4)
#     pltF.XRD_global(ax, label = False)
#     ax.set_xlim(x1_lim,x2_lim)
#     ax.set_ylim(bottom = -0.9*N*fig_shift_add)
    
#     x_range_str = convert_x_range_to_str(x1_lim, x2_lim)
#     if savefigures:
#         pltF.global_savefig(fig, plt_title = title, 
#                             addcomment = comment + x_range_str)
        
        


