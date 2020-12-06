#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 12:43:58 2019

@author: celiacailloux
"""
import OSfunctions as OSfunc
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import trapz
from matplotlib.ticker import AutoMinorLocator, AutoLocator, MultipleLocator

'''________________________GLOBAL SETTINGS__________________________________'''

def color_maps(color_map = None):
    if color_map == 'greenblue':
        color = plt.get_cmap('ocean') 
    elif color_map == 'ocean':
        color = plt.get_cmap('ocean')
    elif color_map == 'blackbluegreen':
        color = plt.get_cmap('gist_earth')    
    elif color_map == 'terrain':
        color = plt.get_cmap('terrain') 
    elif color_map == 'pastel1':
        color = plt.get_cmap('pastel1') 
    elif color_map == 'cubehelix':
        color = plt.get_cmap('cubehelix') 
    elif color_map == 'color_coded':
        color = plt.get_cmap('tab20c')
    else:
        color = ['b', 'g','r','c','m','y','k']
    return color

def markers():
    return ['o', '^','D', 'X']

def global_settings(ax):
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
        
    ax.tick_params(which = 'major',direction='inout', length=12, width=2, labelsize = 14)
    ax.tick_params(which = 'minor',direction='in', length=4, width = 1.2, labelsize = 14)
    
def global_minor_locator(ax, x_locator, y_locator):
    #if x_locator != 0 or y_locator = 0:
        
    ax.xaxis.set_minor_locator(AutoMinorLocator(x_locator))
    ax.yaxis.set_minor_locator(AutoMinorLocator(y_locator))  
    
def global_mayor_xlocator(ax, x_locator):
    ax.xaxis.set_major_locator(MultipleLocator(x_locator))

def global_mayor_ylocator(ax, y_locator):
    ax.yaxis.set_major_locator(MultipleLocator(y_locator))
        
def global_mayor_locator_auto(ax):
    ax.xaxis.set_major_locator(plt.AutoLocator())
    ax.yaxis.set_major_locator(plt.AutoLocator())

def global_lim(ax, x_lim, y_lim):
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    
def global_savefig(fig, plt_title, addcomment = ''):
    directory = 'results'
    OSfunc.create_directory(directory)
    #save_title = directory + '/' + plt_title + '_' + addcomment
    save_title = directory + '/' + plt_title + addcomment
    #fig.savefig(save_title + '.png',bbox_inches='tight', dpi=200)
    #fig.set_size_inches(6, 4)
    fig.savefig(save_title + '.png',bbox_inches='tight', dpi=200)

def global_legendbox(ax, location = 'upper left', loc = 'to right' ):
    if loc == 'bottom':
        ax.legend(loc=location, fontsize = 14, bbox_to_anchor=(0, -0.15))
    elif loc == 'right':
        ax.legend(loc='upper left', fontsize = 16, bbox_to_anchor=(1.2, 1))
    #ax.legend(loc=location, fontsize = 14, bbox_to_anchor=(xbox, ybox))
    
def global_exp_details(ax, exp_details_box, title = None, details_type = None):
    #trans = ax.get_xaxis_transform()
    if details_type is None:
        if title:
            details = title
            print('NOT NONE')
        else:
            details = ''
        
        for detail in exp_details_box:
            details += '\n' + str(detail)
    elif details_type == 'dict':
        for exp, exp_details in exp_details_box.items():
            details = exp + '\n' + str(exp_details)
        details + '** new exp'

    
    ax.annotate(details,xy=(0,-.15), xytext = (0,-.3), 
                    bbox=dict(boxstyle="square", fc="w"), 
                    horizontalalignment='left',verticalalignment='top', 
                    xycoords='axes fraction')   
    
def area_under_curve(x,y, stepsize,baseline = None):
    area_all = trapz(y, x=x, dx=stepsize)
    if baseline is None:
        AUC = np.abs(area_all) #area under curve 
    else:
        ytrapz = np.full_like(y, baseline)
        area_baseline = trapz(ytrapz,x=x, dx=stepsize)
        AUC = np.abs(area_all)-np.abs(area_baseline) #area under curve
    return round(AUC,0)

def global_annotation(ax, text_title, text_list = '', pos = 1):
    if pos == 1:
        xy = (0,-0.2)
        text = text_title #+ '\n' + str(text_list)
        ax.annotate(text,xy, xytext = xy, 
                            bbox=dict(boxstyle="square", fc="w"), 
                            horizontalalignment='left',verticalalignment='top', 
                            xycoords='axes fraction', size = 14)
    if pos == 'EDS/XPS':
        xy = (0.05,0.96)
        text = text_title #+ '\n' + str(text_list)
        ax.annotate(text,xy, xytext = xy, 
                            bbox=dict(boxstyle="square", fc="w"), 
                            horizontalalignment='left',verticalalignment='top', 
                            xycoords='axes fraction', size = 14)
    
def detail_annotation(ax, text, pos = 1):
    if pos == 1:
        xy = (0.05,0.9)
    ax.annotate(text,xy, xytext = xy, 
                        bbox=dict(boxstyle="square", fc="w"), 
                        horizontalalignment='left',verticalalignment='top', 
                        xycoords='axes fraction', size = 16)
        
''' __________________INSTRUMENT SPECIFIC___________________________________'''

''' ICP settings '''

def ICP_global(ax):
    #ax.set_xlabel('Time / min ', fontsize=16)
    ax.set_ylabel('Concentration / ppb', fontsize=16) 
    ax.legend(loc='upper left', fontsize = 12)#, bbox_to_anchor=(1.3, 0.5))
    ax.grid(True, linestyle = '--', which='major', axis ='both', alpha = 0.5)
    
  
    ax.axhline(y = 0, linewidth=2, color='k', alpha = 0.5, linestyle = '--')
    #ax.set_xlim(left = 0)
    ax.set_ylim([-5,15])

''' EDS settings '''

def EDS_global(ax, element, x, x_tick_labels, legend = False, grid = False):
    #line = np.linspace(0, 100, 1000)
    #ax.plot(line,line, color = 'k', alpha = 0.4)
    #ax.set_xlabel('Intended Composition / %', fontsize = 16)
    ax.set_ylabel('at%', fontsize = 16)
    if legend:
        ax.legend(fontsize = 12, loc = 'lower right')
    ax.set_ylim(0,100)
    
    ax.set_xticks(x*100)
    ax.set_xticklabels(x_tick_labels, rotation = 45, fontsize = 14, ha='right')
    #ax.set_aspect('equal', adjustable='box')
    if grid:
        ax.grid(which='major', axis = 'both', color = 'grey', alpha=0.2, linewidth =1 )


''' XRD settings'''

def XRD_global(ax, label = True, yticklabel = False):#

    ax.set_xlabel(r'2$\theta$ / $^\circ$', fontsize = 16)
    ax.set_ylabel('Intensity / arb. unit.', fontsize = 16)
    if yticklabel:
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    else:
        ax.get_yaxis().set_ticks([])     
    
    if label:        
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#        handles, labels = ax.get_legend_handles_labels()
#        ax.legend(handles[::-1], labels[::-1], loc='upper left', fontsize = 16, bbox_to_anchor=(1.3, 0.5))
#    # Shrink current axis by 20%
#    w = 0.8
#    box = ax.get_position()
#    ax.set_position([box.x0, box.y0, box.width * w, box.height])                                           # removes y ticks
#    if label:        
#        #ax.legend(loc='upper left', fontsize = 16, bbox_to_anchor=(1.3, 0.5))
#        handles, labels = ax.get_legend_handles_labels()
#        ax.legend(handles[::-1], labels[::-1], loc='upper left', fontsize = 16, bbox_to_anchor=(1.3, 0.5))
#    if yticklabel:
#        ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
#    else:
#        ax.yaxis.set_major_locator(plt.NullLocator())

''' XPS settings'''

def XPS_global(ax, x, label = True, yticklabel = True):
    #ax.set_xlim([max(x),min(x)])

    if not ax.xaxis_inverted():
        ax.invert_xaxis()

    ax.set_xlabel('Binding Energy / eV ', fontsize = 16)
    ax.set_ylabel('Counts / arb. unit', fontsize = 16)
    if label:        
        #ax.legend(loc='upper left', fontsize = 16, bbox_to_anchor=(1.3, 0.5))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], loc='upper left', fontsize = 16, bbox_to_anchor=(1.3, 0.5))
    if yticklabel:
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    else:
        ax.yaxis.set_major_locator(plt.NullLocator())
        
''' CA (chronoamperomtry settings) '''
def CA_global(ax, V, yaxis,label = True, grid = True):
    if V == 'Ewe/V':
        ax.set_ylabel('V / V vs. RHE ', fontsize=16)
    elif V == 'Ewe/SHE':
        ax.set_ylabel('V / V vs. SHE ', fontsize=16)
    if yaxis == 'Vvstime':
        ax.set_ylabel('V / V vs. RHE', fontsize=16)
    elif yaxis == 'Ivstime':
        ax.set_ylabel('j / mA cm$^{-2}$', fontsize=16) 
    ax.set_xlabel('Time / min', fontsize = 16)
    if grid:
        ax.grid(which='major', axis = 'both', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )
    if label:        
        leg = ax.legend(loc='lower right', fontsize = 14) #bbox_to_anchor=(1.3, 0.5)   
        for line in leg.get_lines():
            line.set_linewidth(4.0)

        
''' CP (chronopotentiometry) settings'''

def CP_global(ax, V, t, label = False, grid = True):

    ax.set_xlabel('Time / min', fontsize=16)#ax.set_xlabel('Time / s', fontsize=16)
    y_range = 3
    if V == 'Ewe/V':
        ax.set_ylabel('V / V vs. RHE ', fontsize=16)        
        ax.set_ylim(-1.5,-1.5+y_range)
    elif V == 'Ewe/SHE':
        ax.set_ylabel('V / V vs. SHE ', fontsize=16)
        ax.set_ylim(-2.5,0.5)#-2+y_range)
        
    if t == 'time/min':
        ax.set_xlabel('Time / min', fontsize=16)
    elif t == 'time/s':
        ax.set_xlabel('Time / s', fontsize=16)
    
    if grid:
        ax.grid(which='major', axis = 'both', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )
        #ax.grid(True, linestyle = '--', which='both', axis ='both', alpha = 0.5)
    if label:        
        leg = ax.legend(loc='lower right', fontsize = 14) #bbox_to_anchor=(1.3, 0.5)   
        for line in leg.get_lines():
            line.set_linewidth(4.0)
''' CV (cyclic voltammetry) settings'''

def CV_global(ax, V, label = True, hline = True, grid = True):
    ax.yaxis.tick_right()
    ax.xaxis.tick_top()
    ax.yaxis.set_label_position('right')
    ax.xaxis.set_label_position('top')
    if V == 'Ewe/V':
        ax.set_xlabel('V / V vs. RHE ', fontsize=16)
    elif V == 'Ewe/SHE':
        ax.set_xlabel('V / V vs. SHE ', fontsize=16)

    ax.set_ylabel('j / mA cm$^{-2}$', fontsize=16) 
    if hline:
        ax.axhline(y = -5.00, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder=1)
    if grid:
        ax.grid(which='major', axis = 'both', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )
    if label:        
        leg = ax.legend(loc='lower right', fontsize = 14) #bbox_to_anchor=(1.3, 0.5)   
        for line in leg.get_lines():
            line.set_linewidth(4.0)