# -*- coding: utf-8 -*-
"""
Created         Wed May 23 14:40:38 2018

@author:        Celia Cailloux (ceshuca)

Updated         June 14 2020

This is a method for GC spectrum integration of PerkinElmer raw data, parsed by
the total_chrom parser created by Kenneth Nielsen. Orginally written by Patrick
Strøm-Hansen but heavily modified by Celia Cailloux.
"""

import numpy as np
import os
import matplotlib.pyplot as plt

from scipy.special import erf
from scipy.optimize import curve_fit
from scipy.integrate import simps


from PyExpLabSys.file_parsers.total_chrom import Raw

from ScipyFunctions import locateErrorFunctionCenter, get_maskedXY, \
    get_maskedXY_inverted, fit_GC_residual, errorfunc,  linfunc
from PlottingFunctions import GC_show_background_fitting
from OSfunctions import get_application_data_location, join_paths    

# import the information about the retention times
#import fit_info



def assign_dictkeys_to_new_dict(old_dict, split = None):
    new_dict = {}

    for dictkeys in old_dict:
        if split == 'end':
            new_dict[dictkeys.split('_',2)[2]] = {}
        else:
            new_dict[dictkeys] = {}
    return new_dict


def extract_data(raw_file):
    #Convinient function to get at the data
    raw_data = Raw(raw_file)
    creation_time = raw_data.raw_data_header['data_header']['time_and_date_created']
    retention_time = np.linspace(0,raw_data.ad_header['Number of Data Points'],raw_data.ad_header['Number of Data Points'])/12.5/60
    counts = np.array(raw_data.raw_data_points)
    return creation_time, retention_time, counts


def fit_erf_background(time_data, func_data, center):
        # Fit errorfunction background to the peaks
        def erf_background(time, size, height): #the errorfunction is re-defined for parsing it correctly into "curve_fit"
            step_speed = 10000 #making the erf-function a almost step-function
            return height + size * erf(step_speed*(time-center))
        best_fit = curve_fit(erf_background,time_data,func_data)
        return best_fit

def erf_bkg_fitting(data):
    erf_center = locateErrorFunctionCenter(data['retention_time_peak'], \
                                           data['spectrum_peak'])           # determines the center of the error function
              
    erf_fit_pars = fit_erf_background(data['retention_time_peak_bkg'], \
                                           data['spectrum_peak_bkg'], erf_center)
           
    retention_time_erf = data['retention_time_peak']
    spectrum_erf = errorfunc(retention_time_erf, erf_center, *erf_fit_pars[0])
    
    # integrating
    spectrum_bkg_subtraction = data['spectrum_peak']-spectrum_erf
    
    # three different ways of integrating the peak
    peak_area_man = round((spectrum_bkg_subtraction*\
                 np.mean(np.diff(data['retention_time_peak']))*60).sum(),0) #60 is for seconds
    peak_area_simps = round(simps(y = spectrum_bkg_subtraction, 
                                  x = data['retention_time_peak']*60), 0)
    peak_area_trapz = round(np.trapz(y = spectrum_bkg_subtraction, 
                                  x = data['retention_time_peak']*60), 0)
    # print(' ')
    # print(peak_area_man)
    # print(peak_area_simps)
    # print(peak_area_trapz)
    
        
    peak_int_erf = {'man'   : peak_area_man,
                    'simps' :peak_area_simps,
                    'trapz' : peak_area_trapz}
    
    return erf_center, retention_time_erf, spectrum_erf, peak_int_erf

def lin_bkg_fit(peak, data):
    lin_fit = fit_GC_residual(x = data['retention_time_peak_bkg'], \
                              y = data['spectrum_peak_bkg'], \
                          peak = peak, peak_center = data['peak_center'])
    
    # print(lin_fit.params['peak_center'].value)
    retention_time_lin_fit = data['retention_time_peak']    
    spectrum_lin_fit = linfunc(retention_time_lin_fit, lin_fit)
       
    # integrating
    spectrum_bkg_subtraction = data['spectrum_peak']-spectrum_lin_fit
    
    # three different ways of integrating the peak
    peak_area_man = round((spectrum_bkg_subtraction*\
                 np.mean(np.diff(data['retention_time_peak']))*60).sum(),0) #60 is for seconds
    peak_area_simps = round(simps(y = spectrum_bkg_subtraction, 
                                  x = data['retention_time_peak']*60), 0)
    peak_area_trapz = round(np.trapz(y = spectrum_bkg_subtraction, 
                                  x = data['retention_time_peak']*60), 0)
    # print(' ')
    # print(peak_area_man)
    # print(peak_area_simps)
    # print(peak_area_trapz)
    
        
    peak_int_lin = {'man'   : peak_area_man,
                    'simps' :peak_area_simps,
                    'trapz' : peak_area_trapz}

    return retention_time_lin_fit, spectrum_lin_fit, peak_int_lin
        
def get_fitting_data(raw_file, peaks_fit_info, bkg_range):#, background_spectrum, peak, bump=None,peak_rise=None):
        """
        get all data necesarry for peak fitting. 
        """
                
        raw_fitting_data = assign_dictkeys_to_new_dict(peaks_fit_info)    # data required to execute peak fitting and quantification
        creation_time, retention_time_all, spectrum_all = extract_data(raw_file)
        raw_fitting_data['retention_time_all'] = retention_time_all                
        raw_fitting_data['spectrum_all'] = spectrum_all
        # no idea
        i = raw_file.rfind('\\')    
        
        for peak, fit_constraint in peaks_fit_info.items():
            #raw_fitting_data[peak] = 'test'  

            " masked raw data to be plotted"
            # mask numpy array
            x_min = fit_constraint['start']
            x_max = fit_constraint['end'] 
            
            retention_time, spectrum = get_maskedXY(x_min-0.5, x_max+0.5, 
                                                    x = retention_time_all, 
                                                    y = spectrum_all)
            raw_fitting_data[peak]['retention_time'] = retention_time                 
            raw_fitting_data[peak]['spectrum'] = spectrum
            
            " masked raw data chosen in fit_info "
            # get masked retention_time and spectrum
            retention_time_peak, spectrum_peak = get_maskedXY(x_min = x_min, 
                                                              x_max = x_max,
                                                              x = retention_time,
                                                              y = spectrum)
           
            raw_fitting_data[peak]['retention_time_peak'] = retention_time_peak                 
            raw_fitting_data[peak]['spectrum_peak'] = spectrum_peak  
            
            " ends of masked raw data used to determine background values for \
                error function"
            retention_time_peak_bkg, spectrum_peak_bkg = \
                get_maskedXY_inverted(x_min = x_min+bkg_range, 
                                      x_max = x_max-bkg_range,
                                      x = retention_time_peak,
                                      y = spectrum_peak)            
         
            raw_fitting_data[peak]['retention_time_peak_bkg'] = retention_time_peak_bkg                 
            raw_fitting_data[peak]['spectrum_peak_bkg'] = spectrum_peak_bkg  
            
            " Error function background fit "   
            
            erf_center, retention_time_erf, spectrum_erf, peak_int_erf =\
                erf_bkg_fitting(raw_fitting_data[peak])
                
            raw_fitting_data[peak]['peak_center'] = erf_center
            raw_fitting_data[peak]['retention_time_bkg_erf'] = retention_time_erf
            raw_fitting_data[peak]['spectrum_bkg_erf'] = spectrum_erf  
            raw_fitting_data[peak]['peak_int_erf'] = peak_int_erf                
            
            " Linear function background fit"                
            retention_time_lin_fit, spectrum_lin_fit, peak_int_lin = \
                lin_bkg_fit(peak, raw_fitting_data[peak])
                
            raw_fitting_data[peak]['retention_time_bkg_lin'] = retention_time_lin_fit
            raw_fitting_data[peak]['spectrum_bkg_lin'] = spectrum_lin_fit  
            raw_fitting_data[peak]['peak_int_lin'] = peak_int_lin              
                   
        return raw_fitting_data

" ------------------------------------------------------------------ PLOTTING"

def save_plot_in_raw_folder(fig, save_plot, 
                            raw_file_path, 
                            detector, 
                            GC_plot_title = None, 
                            plot_type = 'entire chromatogram'):
    if plot_type == 'single peak':
        detector += '_' + 'single'
    
    if save_plot:
        if GC_plot_title:
            save_plot_title = GC_plot_title + '_' + detector + '.png'
            plt.savefig(join_paths(raw_file_path, save_plot_title), dpi=1200)
            print('plot of all {} chromatograms saved'.format(detector))
        else:
            save_plot_title = detector + '.png'                    
            plt.savefig(join_paths(raw_file_path, save_plot_title), dpi=1200)
            print('plot of all {} chromatograms saved'.format(detector))
        plt.close(fig)
    else:
        plt.show()
        print('successful plotting of all {} chromatograms'.format(detector))


""" ---------------------------------------------------------------------- """

class GCIntegrator(object):
    
    def __init__(self,raw_file,fit_info):
        # Initialize info about the fitting
        self.info = fit_info
        self.detector = 'TCD'
        self.raw_file = raw_file
        self.peak_integration = {'erf': {}, 'linear' : {}}
        self.background = {}
        for peak in self.info[self.detector]:
            self.background[peak] = {}
        
    def extract_data(self):
        #Convinient function to get at the data
        raw_data = Raw(self.raw_file)
        creation_time = raw_data.raw_data_header['data_header']['time_and_date_created']
        retention_time = np.linspace(0,raw_data.ad_header['Number of Data Points'],raw_data.ad_header['Number of Data Points'])/12.5/60
        counts = np.array(raw_data.raw_data_points)
        return creation_time, retention_time, counts
    
    def find_CO2_background(self,peak,retention_time,spectrum,bump = 5.6E5,peak_rise=1E6):
        initial_peak_mask = np.logical_and(retention_time>self.info[self.detector][peak]['start'],\
                               retention_time<self.info[self.detector][peak]['end'])
        
        background_bump = np.argmax(spectrum[initial_peak_mask]>bump)
        #print(background_bump)
        peak_start = np.argmax(spectrum[initial_peak_mask]>peak_rise)
        #print('background bump at: {}, and peak start at {}'.format(background_bump,peak_start))
        background_start_index = int(min(range(len(retention_time)),\
                                     key=lambda i: abs(retention_time[i]-self.info[self.detector][peak]['start']))\
                                     +peak_start-(peak_start-background_bump)/2)
        #print(background_start_index)
        new_start = retention_time[background_start_index]
        #print('new start point {}'.format(new_start))
        peak_mask = np.logical_and(retention_time>new_start,\
                               retention_time<self.info[self.detector][peak]['end'])
        peak_time = retention_time[peak_mask]
        self.background[peak]['peak_time']=peak_time
        peak_count = spectrum[peak_mask]
        background_mask_start = np.logical_and(peak_time>new_start,\
                                               peak_time<new_start\
                                               +self.info['settings']['background_range'])
        background_mask_end = np.logical_and(peak_time>self.info[self.detector][peak]['end']\
                                               -self.info['settings']['background_range'],\
                                               peak_time<self.info[self.detector][peak]['end'])
        return peak_time, peak_count, background_mask_start, background_mask_end
    
    def find_normal_background(self,peak,retention_time,spectrum):
        "masks retention time and spectrum"
        # mask consisting of logical (True/False)
        peak_mask = np.logical_and(retention_time>self.info[self.detector][peak]['start'],\
                                   retention_time<self.info[self.detector][peak]['end'])
        # masking the retention_time
        peak_time = retention_time[peak_mask]
        # save the masked retention time in a dictionary
        self.background[peak]['retention_time_peak'] = peak_time

        peak_count = spectrum[peak_mask]
        "further masking off the retention time??"
        background_mask_start = np.logical_and(peak_time>self.info[self.detector][peak]['start'],\
                                               peak_time<self.info[self.detector][peak]['start']\
                                               +self.info['settings']['background_range'])
        background_mask_end = np.logical_and(peak_time>self.info[self.detector][peak]['end']\
                                               -self.info['settings']['background_range'],\
                                               peak_time<self.info[self.detector][peak]['end'])
        return peak_time, peak_count, background_mask_start, background_mask_end
    
    #fit background and integrate spectrum
    def integrate_spectrum(self, bump= None, peak_rise = None):
        creation_time, retention_time, spectrum = self.extract_data()
        # search through fit_info for the peaks and create a mask of the 
        # retention times where they appear
        for peak in self.info[self.detector]:
            
            x_min = self.info[self.detector][peak]['start']
            x_max = self.info[self.detector][peak]['end']      
            
            " masked raw data chosen in fit_info "
            # get masked retention_time and spectrum
            retention_time_peak, spectrum_peak = get_maskedXY(x_min = x_min, 
                                                              x_max = x_max,
                                                              x = retention_time,
                                                              y = spectrum)        
            
            # if peak == 'CO2':
            #     if bump is None and peak_rise is None:
            #         peak_time,peak_count, background_mask_start, background_mask_end = \
            #         self.find_CO2_background(peak,retention_time,spectrum)
            #     else:
            #         peak_time,peak_count, background_mask_start, background_mask_end = \
            #         self.find_CO2_background(peak,retention_time,spectrum,bump,peak_rise)
            # else:                
            #     peak_time, peak_count, background_mask_start, background_mask_end = \
            #     self.find_normal_background(peak,retention_time,spectrum)
            
            
            " Ends of masked raw data used to determine background values for error function"
            retention_time_peak_bkg, spectrum_peak_bkg = \
                get_maskedXY_inverted(x_min = x_min+self.info['settings']['background_range'],
                                                         x_max = x_max-self.info['settings']['background_range'],
                                                         x = retention_time_peak,
                                                         y = spectrum_peak)
                
            erf_center = [i for i, j in enumerate(spectrum_peak) if j == np.amax(spectrum_peak)] #the step of the error-function is placed at peak-maximum
            erf_center = retention_time_peak[erf_center[0]] #value instead of a vector
            #self.background[peak]['erf_center']=erf_center
            
            background_fit = self.fit_erf_background(retention_time_peak_bkg, spectrum_peak_bkg, erf_center)
            #self.background[peak]['background_fit'] = background_fit
            
            renorm_peak_count = spectrum_peak-self.errorfunc(retention_time_peak,erf_center,*background_fit[0])     
            area = (renorm_peak_count*np.mean(np.diff(retention_time_peak))*60).sum() #60 is for seconds
            
            self.peak_integration['erf'][peak] = abs(area)
            self.peak_integration['erf'][peak] = abs(area)
        return self.peak_integration
    
       
    def plot_background(self,bump=None,peak_rise=None):
        creation_time, retention_time, spectrum = self.extract_data()
        


    
        fig, background_spectrum = plt.subplots()
        background_spectrum.plot(retention_time,spectrum,'o',markersize=1.1)
        i = self.raw_file.rfind('\\')
        for peak in self.info[self.detector]:
            
#            if peak == 'CO2':
#                if bump is None and peak_rise is None:
#                    peak_time,peak_count, background_mask_start, background_mask_end = \
#                    self.find_CO2_background(peak,retention_time,spectrum)
#                else:
#                    peak_time,peak_count, background_mask_start, background_mask_end = \
#                    self.find_CO2_background(peak,retention_time,spectrum,bump,peak_rise)
#            else:
                
            peak_time, peak_count, background_mask_start, background_mask_end = \
            self.find_normal_background(peak,retention_time,spectrum)
            
            
            retention_time_peak_bkg = np.append(peak_time[background_mask_start],\
                                             peak_time[background_mask_end])
            spectrum_peak_bkg = np.append(peak_count[background_mask_start],\
                                                  peak_count[background_mask_end])
                
            erf_center = [i for i, j in enumerate(peak_count) if j == np.amax(peak_count)] #the step of the error-function is placed at peak-maximum
            erf_center = peak_time[erf_center[0]] #value instead of a vector
            self.background[peak]['erf_center']=erf_center
            
            background_fit = self.fit_erf_background(retention_time_peak_bkg, spectrum_peak_bkg, erf_center)
                   
            background_spectrum.plot(self.background[peak]['peak_time'],self.errorfunc(self.background[peak]['peak_time'],\
                                     self.background[peak]['erf_center'],*background_fit[0]))
            
            background_spectrum.set_xlabel('time [min]')
            background_spectrum.set_ylabel('a.u.')
            background_spectrum.tick_params('y')
            background_spectrum.axes.set_title(self.raw_file[i:])
            background_spectrum.set_ylim([5E5,2.8E6])
        plt.tight_layout()
        plt.draw()
        
    def plot_background_fitting(self,background_spectrum, peak, bump=None,peak_rise=None):
        """
        Parameters
        ----------
        background_spectrum : TYPE
            DESCRIPTION.
        peak : TYPE
            DESCRIPTION.
        bump : TYPE, optional
            DESCRIPTION. The default is None.
        peak_rise : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        creation_time, retention_time_all, spectrum_all = self.extract_data()
        # no idea
        i = self.raw_file.rfind('\\')                                           
        
        " masked raw data to be plotted"
        # mask numpy array
        x_min = self.info[self.detector][peak]['start']
        x_max = self.info[self.detector][peak]['end']
        retention_time, spectrum = get_maskedXY(x_min-0.5, x_max+0.5, 
                                                x = retention_time_all, 
                                                y = spectrum_all)
        background_spectrum.plot(retention_time,spectrum,'o',markersize=1.1)

                    
        # if peak == 'CO2':
        #     if bump is None and peak_rise is None:
        #         peak_time,peak_count, background_mask_start, background_mask_end = \
        #         self.find_CO2_background(peak,retention_time,spectrum)
        #     else:
        #         peak_time,peak_count, background_mask_start, background_mask_end = \
        #         self.find_CO2_background(peak,retention_time,spectrum,bump,peak_rise)
        # else:
        
        " masked raw data chosen in fit_info "
        # get masked retention_time and spectrum
        retention_time_peak, spectrum_peak = get_maskedXY(x_min = x_min, 
                                                          x_max = x_max,
                                                          x = retention_time,
                                                          y = spectrum)
        self.background[peak]['retention_time_peak'] = retention_time_peak
        
        #background_spectrum.plot(retention_time_peak, spectrum_peak)
        
        " Ends of masked raw data used to determine background values for error function"
        retention_time_peak_bkg, spectrum_peak_bkg = \
            get_maskedXY_inverted(x_min = x_min+self.info['settings']['background_range'],
                                                     x_max = x_max-self.info['settings']['background_range'],
                                                     x = retention_time_peak,
                                                     y = spectrum_peak)

        
        background_spectrum.plot(retention_time_peak_bkg, spectrum_peak_bkg, 'r')
        #background_spectrum.plot(retention_time_peak, spectrum_peak)
        
        " Error function background fit "
        erf_center = locateErrorFunctionCenter(retention_time_peak, spectrum_peak)           # determines the center of the error function
        self.background[peak]['erf_center'] = erf_center       
              
        background_fit = self.fit_erf_background(retention_time_peak_bkg, spectrum_peak_bkg, erf_center)
        renorm_peak_count = spectrum_peak-self.errorfunc(retention_time_peak,erf_center,*background_fit[0])     
        area = (renorm_peak_count*np.mean(np.diff(retention_time_peak))*60).sum() #60 is for seconds
        
        self.peak_integration['erf'][peak] = abs(area)

        # print(background_fit)
        # print(background_fit[0])
        print(' ')
        x = self.background[peak]['retention_time_peak']
        y = self.errorfunc(self.background[peak]['retention_time_peak'],\
                                     self.background[peak]['erf_center'],\
                                         *background_fit[0])
        background_spectrum.plot(x,y, color = 'r')
        background_spectrum.plot(x,renorm_peak_count, color = 'g')
        
        " Linear function background fit"
        lin_fit = fit_GC_residual(x = retention_time_peak_bkg, y = spectrum_peak_bkg, \
                              peak = peak, peak_center = erf_center)
        
        #out = fit_GC_residual(x = retention_time, y = spectrum, peak = peak, peak_center = erf_center)
        background_spectrum.plot(retention_time_peak_bkg, lin_fit.best_fit, 'k-')
        # print(lin_fit.params['peak_center'].value)
        self.background[peak]['lin_bkg_fit'] = lin_fit
                
        "plotting parameters"    
        GC_show_background_fitting(ax = background_spectrum, x = retention_time, 
                                   y = spectrum, plt_title = self.raw_file[i:])


    def fit_erf_background(self,time_data, func_data, center):
        # Fit errorfunction background to the peaks
        def erf_background(time, size, height): #the errorfunction is re-defined for parsing it correctly into "curve_fit"
            step_speed = 10000 #making the erf-function a almost step-function
            return height + size * erf(step_speed*(time-center))
        best_fit = curve_fit(erf_background,time_data,func_data)
        return best_fit
    
    def errorfunc(self, time, center, size, height):
        step_speed = 10000 #making the erf-function a almost step-function
        return height+size*erf(step_speed*(time-center))