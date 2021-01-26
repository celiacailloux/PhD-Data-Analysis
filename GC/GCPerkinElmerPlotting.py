# -*- coding: utf-8 -*-
"""
Created on Mon May 18 20

@author: ceshuca

With inspiration from patri's (floor manager) scripts for GC analysis 
(original version can be found in O:\list-SurfCat\setups\307-059-largeCO2MEA).
This file contains the module/object used to do GC and EC analysis. Both 
calculations and plotting. 

It requires the "fit_info" to determine the GC peak fitting.
"""


from PyExpLabSys.file_parsers.total_chrom import Raw
from os import walk, path
import pickle
from cinfdata import Cinfdata
import numpy as np
from pylab import rcParams
import matplotlib.pyplot as plt
import PlottingFunctions as pltF
from ColorFunctions import view_colormap


#fit packages
#from gc_integrator_CO2 import GCIntegrator
from GCPerkinElmer_functions import GCIntegrator, assign_dictkeys_to_new_dict, \
    get_fitting_data, save_plot_in_raw_folder #, get_PerkinElmer_calibration
from PlottingFunctions import GC_show_background_fitting, GC_show_all_spectra, \
    global_savefig, color_maps, GC_show_peak_plotting
from OSfunctions import get_application_data_location, join_paths    

rcParams['figure.figsize'] = 10, 6
#sns.set()
#sns.set_context('paper')

""" object """

class GC_EC_analyzer():
    
    def __init__(self, filepath, fit_info, raw_to_analyse, GC_plot_title,\
                 iv_average = int(5), \
                 bump = None, peak_rise = None):
        self.filepath = filepath
        self.raw_to_analyse = raw_to_analyse        
        self.GC_plot_title = GC_plot_title
        # Import the calibration file                                          # ?
        # self.calibration = get_PerkinElmer_calibration()#self.load_obj(name = 'calibrations_direct_CO_pressure_corrected_4')
        
        # Constants
        self.number_of_electrons = 2
        self.faraday_const = 96485.33289                                        # C/mol
        gas_constant = 0.08314472                                               # L bar mol^-1 K^-1
        self.molar_volume = 22.4*1e3                                           # cm3/mol, STP (273 K (or 0oC). 1 atm (760 torr))
        self.bump = bump                                                        # ?
        self.peak_rise = peak_rise                                              # ?
        
       
        self.fit_info = fit_info
        #self.peaks_fit_info = self.fit_info['TCD']                      # contains retention time start and end for peak fitting for all peaks (=gases)
        
        self.bkg_ends = fit_info['settings']['background_range']# define the number of datapoints to average over in the current, voltage
        # and flow calculations
        self.time_average_index = iv_average # seconds
        
        # functions

        self.fitting_data = self.obtain_GC_fitting_data()                       # data required to execute peak fitting and quantification
        self.raw_time_stamp = self.get_raw_time_stamp()
        # for key, val in self.fitting_data.items():
        #     print(val.keys())
        
    def load_obj(self,name):
        "Load files from folder obj. fx. calibration file"
        with open('obj/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)
        
    def get_raw_time_stamp(self):
        print('get_raw_time...\n')
        # Dict containing of time stamp of each chromatogram. E.g. 1537569193
        raw_time_stamp = assign_dictkeys_to_new_dict(self.fit_info) # gets TCD and FID as keys in dict
        
        for detector in raw_time_stamp.keys():
            if detector == 'FID' or detector == 'TCD':
                for n_raw, raw in enumerate(self.raw_files[detector]):
                    i = raw.rfind('\\')    
                    raw_file_name = path.splitext(raw[i:])[0]  
                    raw_data = Raw(raw)
                    raw_time_stamp[detector][raw_file_name] = \
                        raw_data.raw_data_header['data_header']['time_and_date_created']
            
        return raw_time_stamp
        
    def obtain_GC_fitting_data(self):
        fitting_data = assign_dictkeys_to_new_dict(self.fit_info) # gets TCD and FID as keys in dict
        self.raw_files =  {}

        # gets the chosen GC raw files
        self.raw_files['TCD'], self.raw_files['FID'] = self.raw_file_search(self.filepath, self.raw_to_analyse)

        " get fitting data (x,y, x_bkg, y_bkg) "  
        
        for detector in fitting_data.keys():
            if detector == 'FID' or detector == 'TCD':
                for n_raw, raw in enumerate(self.raw_files[detector]):
                    i = raw.rfind('\\')    
                    raw_file_name = path.splitext(raw[i:])[0]  
                    fitting_data[detector][raw_file_name] = \
                        get_fitting_data(raw, self.fit_info[detector], self.bkg_ends)     
           
        return fitting_data
        
    def uncertainty(self,*args):
        "Calculate the uncertainty on the value as root of squared fractional\
        uncertainties and return relative error"
        uncertainties = []
        for arg in args:
            #print(arg['value'], arg['error'])
            uncertainties.append((arg['error']/arg['value'])**2)
        
        error = np.sqrt(sum(uncertainties))
        #print(error)
        return error
            
    def raw_file_search(self, filepath, raw_to_analyse):
        "search for raw files in the specified folder"
        TCD_raw_files = []
        FID_raw_files = []
        
        print("Searching for raw files")
        for root, dirs, files in walk("{}".format(filepath)):
            for file_ in files:
                if path.splitext(file_)[1] == '.raw' and 'fid' in file_:
                    #print(path.join(root, file_))
                    FID_raw_files.append(path.join(root, file_))
                if path.splitext(file_)[1] == '.raw' and 'tcd' in file_:
                    #print(path.join(root, file_))
                    TCD_raw_files.append(path.join(root, file_))                
        if len(TCD_raw_files) == 0:
            print("Done! However, no TCD files were found in".format(filepath))
        else:
            print("Done! Found {} TCD files".format(len(TCD_raw_files)))            
        if len(TCD_raw_files) == 0:
            print("Done! However, no FID files were found in {}\n".format(filepath))            
        else:
            print("Done! Found {} FID files\n".format(len(FID_raw_files)))
            
        if raw_to_analyse is None:
            return TCD_raw_files, FID_raw_files
        else:
            return TCD_raw_files[raw_to_analyse], FID_raw_files[raw_to_analyse]
    
    """should be deleted - not used"""
    def get_area_from_raw(self, list_of_rawfiles):
        "get_area_from_raw(list_of_rawfiles)-> gc_time, TCD_res[fit_info.peak]"
        
        "TCD_res[peak] is a dictionary of area corresponding to define peaks in\
         fit info"
        # List of time stamp of each chromatogram. E.g. 1537569193

        # Dict which contains for all peaks(gases) the intensity
        TCD_res = {}
        for peak in self.peaks_fit_info:
            TCD_res[peak]=[]
            
        for raw in list_of_rawfiles:
            #print('Integrating spectrum in rawfile: {}'.format(raw))
            gc_integrator = GCIntegrator(raw,self.fit_info)
            raw_data = Raw(raw)

            peak_integration = gc_integrator.integrate_spectrum(self.bump,self.peak_rise)
            print(peak_integration)
                
            for peak in self.peaks_fit_info:
                TCD_res[peak].append(peak_integration['erf'][peak])
                
        print('Integration complete')
        #print(TCD_res)
        return TCD_res
    
    def show_peak_plotting(self, save_plot = False):
               
        """ plotting """
        n_FID = len(self.fit_info['FID'])
        n_TCD = len(self.fit_info['TCD'])
        num_of_raw = len(self.raw_files['TCD'])
        
        N = n_FID + n_TCD
        n_col = max(n_FID, n_TCD)
        n_row = len(self.raw_files.keys())
        fig, axs = plt.subplots(n_row,n_col, 
                                gridspec_kw={'wspace': 0.3, 'hspace': 0.3},
                                sharex=False, sharey = False, squeeze=True) 
        fig.set_size_inches(w=n_col*3+1,h=n_row*3)
        color = color_maps('jkib')  
        
        n_peak_plot = 0
        
        for n_detector, detector in enumerate(self.raw_files.keys()):
            
            for n_raw, raw in enumerate(self.raw_files[detector]):
                i = raw.rfind('\\')
                col = color(n_raw/(num_of_raw))
                if detector == 'TCD':
                    n_peak_plot = 0                       
                elif detector == 'FID':
                    n_peak_plot = n_TCD
                # print('subplot restart #:{}'.format(n_peak_plot))                    
                
                    
                for n_peak, peak in enumerate(self.fit_info[detector].keys()):
                    raw_file_name = path.splitext(raw[i:])[0] 
                    peak_data = self.fitting_data[detector][raw_file_name][peak]
                    
                    # print(n_detector, n_peak)
                    axs[n_detector, n_peak].plot(peak_data['retention_time_peak'],
                                            peak_data['spectrum_peak'],
                                            '-', linewidth = 1, #markersize=1.1,
                                            color = col, 
                                            label = raw_file_name)
        
                    "plotting parameters"    
                    GC_show_peak_plotting(ax = \
                                            axs[n_detector, n_peak], \
                                                x = peak_data['retention_time_peak'],
                                                y = peak_data['spectrum_peak'], 
                                                plt_title = peak + '-' + detector,
                                                detector = detector)
                    pltF.global_settings(axs[n_detector, n_peak])
        
        # plt.tight_layout()
        pltF.global_legendbox(axs[-1, -1],  
                              loc = 'GC peak plotting')        
        fig.subplots_adjust(wspace=0.5, hspace=0)
        if save_plot:    
            pltF.GCPE_savefig(fig, self.filepath, 
                         detector = 'FID and TCD', 
                         GC_plot_title = self.GC_plot_title, 
                         plot_type = 'single peak')
            view_colormap(cmap = color, raw_file_path = self.filepath)    
        else:
            plt.show()
            print('successful plotting of all {} chromatograms'.format(detector)) 
        # save_plot_in_raw_folder(fig, save_plot, self.filepath, detector, \
        #                         self.GC_plot_title, plot_type = 'single peak') 

    def show_fitting(self, save_plot = False):
        """
        From GC chromatograms, retention time and intensitiy is gathered for
        each peak (=gas). This information is saved in 
        Parameters
        """
         
        # for raw in self.fitting_data:
        #     print('\n', raw)
        #     print(self.fitting_data[raw].keys())
        #     for peak in self.fitting_data[raw]:
        #         print(self.fitting_data[raw][peak].keys())
                
        """ plotting """
        for detector in self.raw_files.keys():
        
            n_row = len(self.raw_files[detector])
            n_col = len(self.fit_info[detector])
            if n_col == 1:
                n_col = 2
     
            fig, axs = plt.subplots(n_row, n_col, figsize = (3*n_col,n_row), 
                                    sharex='col', sharey = False, squeeze=True) 
            for n_raw, raw in enumerate(self.raw_files[detector]):
                i = raw.rfind('\\')                         
                for n_peak, peak in enumerate(self.fit_info[detector].keys()):
                    raw_file_name = path.splitext(raw[i:])[0] 
                    peak_data = self.fitting_data[detector][raw_file_name][peak]
                    
                    
                    axs[n_raw, n_peak].plot(peak_data['retention_time'],
                                            peak_data['spectrum'],
                                            'o-',markersize=1.1)
                    # axs[n_raw, n_peak].plot(peak_data['retention_time_peak'], 
                    #                         peak_data['spectrum_peak'],
                    #                         'g--')
                    # axs[n_raw, n_peak].plot(peak_data['retention_time_peak_bkg'], 
                    #                         peak_data['spectrum_peak_bkg'],
                    #                         'k--')
                    axs[n_raw, n_peak].plot(peak_data['retention_time_bkg_lin'], 
                                            peak_data['spectrum_bkg_lin'],
                                            'r--')                
                    axs[n_raw, n_peak].plot(peak_data['retention_time_bkg_erf'], 
                                            peak_data['spectrum_bkg_erf'],
                                            'g-')#, color = 'orange')                
                                    
                    
                    "plotting parameters"    
                    GC_show_background_fitting(ax = \
                                                axs[n_raw, n_peak], \
                                                    x = peak_data['retention_time'],
                                                    y = peak_data['spectrum'], 
                                                    plt_title = raw_file_name)                
            plt.tight_layout()
            fig.subplots_adjust(wspace=0.5, hspace=0)
            
            save_plot_in_raw_folder(fig, save_plot, self.filepath, detector, \
                                    self.GC_plot_title, plot_type = 'single peak') 
        
        
    def show_fitting_all_figures(self, save_plot = False):
        """
        plots all entire chromatograms. it generates on figure pr. detector
        (FID or TCD). the figures are saved in the data folder. 
        """

        for detector in self.raw_files.keys():
            n_row = len(self.raw_files[detector])
                   
            fig, axs = plt.subplots(n_row, 1, figsize = (n_row,n_row), 
                                    sharex= True, sharey = False)#, squeeze=True) 
            for n_raw, raw in enumerate(self.raw_files[detector]):
                
                i = raw.rfind('\\')   
                raw_file_name = path.splitext(raw[i:])[0]      
                         
                retention_time = self.fitting_data[detector][raw_file_name]['retention_time_all']         
                spectrum = self.fitting_data[detector][raw_file_name]['spectrum_all']
                axs[n_raw].plot(retention_time, spectrum, 'o-',markersize=1.1)
                # axs[n_raw, n_peak].plot(peak_data['retention_time_peak'], 
                #                         peak_data['spectrum_peak'],
                #                         'g--')
                # axs[n_raw, n_peak].plot(peak_data['retention_time_peak_bkg'], 
                #                         peak_data['spectrum_peak_bkg'],
                #                         'k--')
                # axs[n_raw, n_peak].plot(peak_data['retention_time_bkg_lin'], 
                #                         peak_data['spectrum_bkg_lin'],
                #                         'r--')                
                # axs[n_raw, n_peak].plot(peak_data['retention_time_bkg_erf'], 
                #                         peak_data['spectrum_bkg_erf'],
                #                         'g-')#, color = 'orange')                
                                
                
                "plotting parameters"    
                GC_show_all_spectra(ax = axs[n_raw], 
                                    x = retention_time,
                                    y = spectrum,
                                    plt_title = raw_file_name)                
            plt.tight_layout()
            fig.subplots_adjust(wspace=0.5, hspace=0)
            # plt.close(fig)
            
            save_plot_in_raw_folder(fig, save_plot, self.filepath, detector, \
                                    self.GC_plot_title, plot_type = 'entire chromatogram') 
            
  