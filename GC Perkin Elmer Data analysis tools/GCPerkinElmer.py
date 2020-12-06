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


#fit packages
#from gc_integrator_CO2 import GCIntegrator
from GCPerkinElmer_functions import GCIntegrator, assign_dictkeys_to_new_dict, \
    get_fitting_data, save_plot_in_raw_folder, get_PerkinElmer_calibration
from PlottingFunctions import GC_show_background_fitting, GC_show_all_spectra, \
    global_savefig, GCPE_savefig
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
        self.calibration = get_PerkinElmer_calibration()#self.load_obj(name = 'calibrations_direct_CO_pressure_corrected_4')
        
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
            
    def FE_calculation(self,filename,measurement_id, time_correction=0):
        """Do Faradaic efficiency calculation
        
        time_correction: "correction to get the right current value"
        raw_to_analyse: "slice of raw files"
        
        """
        " peak integration etc"
        # gc_measurement_time is now raw_time_stamp
        # TCD_res is now fitting_data[detector][raw][peak][bkg_type][int_type]
        # Ex fitting_data['TCD']['\\datb_tcd_021']['H2']['peak_int_lin']['simps']
        
        " iv_data in progress "
        # see how Patrik and co calculated the inlet flow in iv_gc_comparison
        iv_data = None
        cathode_size = 1 # cm2   
        
        # gc_inlet_flow, gc_current, gc_voltage = \
        #     self.iv_gc_comparison(gc_measurement_time,iv_data,time_correction)
        # gc_inlet_flow is changed to molar flow rate
        
        gc_current = assign_dictkeys_to_new_dict(self.raw_time_stamp['FID'].keys(), 
                                                 split = 'end')
      
        gc_voltage = assign_dictkeys_to_new_dict(self.raw_time_stamp['FID'].keys(),
                                                 split = 'end')
        
        gc_current = dict.fromkeys(gc_current, -2.2)                            # mA
        gc_voltage = dict.fromkeys(gc_voltage, -1.7)                            # V
        
        # Find the amount of moles of each component from the calibration
        # normalized_res = {} is now moles[peak] but does not contain any col_std nor err
        
        FE = {}
        molar_flow_rate = \
            self.fit_info['settings']['flow_rate']/self.molar_volume/60        # sccm (cm3/min) -> mole/min -> mole/s
        print('molar flow rate: {}'.format(molar_flow_rate))
            
        for detector in self.raw_time_stamp.keys():
            if detector == 'FID' or detector == 'TCD':
                for n_raw, raw in enumerate(self.raw_files[detector]):
                    i = raw.rfind('\\')    
                    raw_file_name = path.splitext(raw[i:])[0]
                    raw_idx = raw_file_name.split('_',2)[2]                  
                    #print(self.fitting_data[detector][raw_file_name].keys())
                    for peak in self.fitting_data[detector][raw_file_name].keys():
                        if peak in self.calibration[detector].keys():
                            # change it to error function or trapx or man instead of "simps"
                            print('\n')
                            print(raw_idx)
                            print(peak)
                            peak_area = self.fitting_data[detector][raw_file_name][peak]['peak_int_lin']['simps']
                            print('peak area is: {}'.format(peak_area))
                            mole_fraction = peak_area/self.calibration[detector][peak]['slope']  # mole fraction in mole%
                            print('slope:{}'.format(self.calibration[detector][peak]['slope']))
                            print('mole fraction: {}'.format(mole_fraction))
                            mole_out = \
                                mole_fraction*molar_flow_rate*self.calibration[detector][peak]['z'] # mole/s
                            mole_in = \
                                (gc_current[raw_idx]*1e-3)/self.faraday_const # mA -> A -> mole/s
                            FE_peak = mole_out/mole_in*100

                            print('mole in {}'.format(mole_in))
                            print('mole out {}'.format(mole_out))
                            #print('mole in {}'.format(mole_in))
                            FE[peak] = {'detector': detector, 
                                        'mole_fraction': round(mole_fraction,2),
                                        'mole_out': round(mole_out,4),
                                        'mole_in': round(mole_in,4),
                                        'FE'     : round(FE_peak, 2),
                                        'integration type': 'lin - simps'}
                        
        return FE
        
    
        """
                   
        faraday_eff_CO = []
        for index in range(len(current_CO)):
            val = current_CO[index]['value']/gc_current[index]['value']
            err = self.uncertainty(current_CO[index],gc_current[index])
            faraday_eff_CO.append({'value':val,
                                    'error':err*val})
        
        # faraday_eff_H2 = []
        # for index in range(len(current_H2)):
        #     val = current_H2[index]['value']/gc_current[index]['value']
        #     err = self.uncertainty(current_H2[index],gc_current[index])
        #     faraday_eff_H2.append({'value':val,'error':err*val})
        """
        
        #return faraday_eff_CO, current_CO#, faraday_eff_H2,current_H2,\
                #gc_current,gc_voltage, cathode_size, gc_measurement_time,normalized_res,gc_inlet_flow
        
    def plot_iv_correction(self,filename,measurement_id,plot_title = 'A title',time_correction = 0, raw_to_analyse = None):
        "Tool to show where the GC measurement is taken in the IV data"
        list_of_rawfiles = self.raw_file_search(filename)
        if raw_to_analyse is None:
            raw_to_analyse = slice(0,len(list_of_rawfiles))
        
        gc_measurement_time, TCD_res = self.get_area_from_raw(list_of_rawfiles)
        iv_data, cathode_size = self.get_iv_data(measurement_id)
        #print('save_rate for {} is {} s'.format(plot_title,(iv_data['time'][10]-iv_data['time'][9])))
        
        gc_inlet_flow, gc_current, gc_voltage = self.iv_gc_comparison(gc_measurement_time,iv_data, time_correction)
        gc_measurement_time[:] = [round((x-time_correction-iv_data['time'][0])/3600,1) for x in gc_measurement_time]
        time_values = [round((x-iv_data['time'][0])/3600,1) for x in iv_data['time']]
        current_plot_vals = [x['value']*1000/cathode_size for x in gc_current]
        #voltage_plot_vals = [x['value'] for x in gc_voltage]
        
        fig, ax1 = plt.subplots()
        
        save_rate = (iv_data['time'][500]-iv_data['time'][499])
        color = 'tab:red'
        ax1.set_xlabel('Time [h]')
        ax1.set_ylabel('Geometric current density [mA/cm$^2$]')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.plot(time_values[int(3.5*3600/save_rate):-1],[x*1000/cathode_size for x in iv_data['current'][int(3.5*3600/save_rate):-1]],color=color)
        ax1.plot(gc_measurement_time,current_plot_vals,'kx', label = 'GC measurement, time correction: {} min'.format(time_correction/60))
        ax1.legend(loc=4, shadow=True, fontsize='xx-small')
        ax1.set_title(plot_title)
        ax1.set_ylim([0, 550])
        ax1.set_yticks(np.arange(0, 550, 50))
        ax1.grid(True)
        
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2.plot(time_values,iv_data['voltage'], color=color)
        ax2.set_ylabel('Voltage [V]', color=color)  # we already handled the x-label with ax1
        ax2.tick_params(axis='y', labelcolor=color)
        #ax2.set_yticks(np.arange(2, 3.8, 0.2))
        ax2.set_ylim([0, 4])
        
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.draw()
    
    def plot_FE_to_current(self,filename,measurement_id,plot_title,time_correction = 0, raw_to_analyse = None):
        
        FE_CO, current_CO, FE_H2,current_H2,gc_current,gc_voltage, cathode_size, gc_measurement_time,_,_=\
        self.FE_calculation(filename,measurement_id, time_correction, raw_to_analyse)
        
        #print(current_H2)
        FE_CO_val = [x['value'] for x in FE_CO]
        FE_CO_err = [x['error'] for x in FE_CO]
        
        FE_H2_val = [x['value'] for x in FE_H2]
        FE_H2_err = [x['error'] for x in FE_H2]
        
        FE_sum = [sum(x) for x in zip(FE_CO_val,FE_H2_val)]
        FE_sum_err = [np.sqrt(FE_CO_err[x]**2 +FE_H2_err[x]**2) for x in range(len(FE_CO_err))]
        geo_current_density = [x['value']*1000/cathode_size for x in gc_current]
        x_err = [x['error']*1000/cathode_size for x in gc_current]
        #print(geo_current_density)
        fig, FE_plot = plt.subplots()
        FE_plot.errorbar(geo_current_density,FE_CO_val, xerr=x_err,yerr=FE_CO_err, fmt='-o',label = 'CO',elinewidth = 0.8, capsize = 3)
        FE_plot.errorbar(geo_current_density,FE_H2_val,xerr=x_err,yerr=FE_H2_err, fmt='-^',label = 'H2',elinewidth = 0.8, capsize = 3)
        FE_plot.errorbar(geo_current_density,FE_sum,xerr=x_err,yerr =FE_sum_err, fmt='-s',label = 'SUM',elinewidth = 0.8, capsize = 3)
        FE_plot.legend(shadow=True,loc=1,fontsize='xx-small',ncol=3)
#        FE_plot.legend(shadow=True,loc='center left', bbox_to_anchor=(1, 0.5))
        FE_plot.set_xlabel('Geometric current density [mA/cm$^2$]')
        FE_plot.set_ylabel('Faraday efficiency')
        FE_plot.tick_params('y')
        FE_plot.set_yticks(np.arange(0, 1.4, 0.2))
        FE_plot.axes.set_ylim([0,1.4]) #y-axis
        FE_plot.set_title(plot_title)
        FE_plot.grid(True)
        plt.tight_layout()
        plt.draw()
    def plot_FE_to_voltage(self,filename,measurement_id,plot_title,time_correction = 0, raw_to_analyse = None):
        
        FE_CO, current_CO, FE_H2,current_H2, gc_current,gc_voltage, cathode_size, gc_measurement_time,_,_=\
        self.FE_calculation(filename,measurement_id, time_correction, raw_to_analyse)
        
        FE_CO_val = [x['value']*100 for x in FE_CO]
        FE_CO_err = [x['error']*100 for x in FE_CO]
        
        FE_H2_val = [x['value']*100 for x in FE_H2]
        FE_H2_err = [x['error']*100 for x in FE_H2]
        
        FE_sum = [sum(x) for x in zip(FE_CO_val,FE_H2_val)]
        FE_sum_err = [np.sqrt(FE_CO_err[x]**2 +FE_H2_err[x]**2) for x in range(len(FE_CO_err))]
        x_vals = [x['value'] for x in gc_voltage]
        x_err = [x['error'] for x in gc_voltage]
        
        fig, FE_plot = plt.subplots()
        FE_plot.errorbar(x_vals,FE_CO_val,xerr=x_err,yerr=FE_CO_err, fmt='-o',label = 'CO',elinewidth = 0.8, capsize = 3)
        FE_plot.errorbar(x_vals,FE_H2_val,xerr=x_err,yerr=FE_H2_err, fmt='-^',label = 'H2',elinewidth = 0.8, capsize = 3)
        FE_plot.errorbar(x_vals,FE_sum,xerr =x_err, yerr =FE_sum_err, fmt='-s',label = 'SUM',elinewidth = 0.8, capsize = 3)
        FE_plot.legend(shadow=True,loc=1,fontsize='xx-small',ncol=3)
        #FE_plot.legend(loc='best', shadow=True)
        FE_plot.set_xlabel('Cell voltage [V]')
        FE_plot.set_ylabel('Faraday efficiency')
        FE_plot.tick_params('y')
        #FE_plot.axes.set_ylim([0,1.2]) #y-axis
        FE_plot.set_title(plot_title)
        FE_plot.grid(True)
        plt.tight_layout()
        plt.draw()
    def plot_FE_to_time(self,filename,measurement_id,plot_title,time_correction = 0, raw_to_analyse = None):
        
        FE_CO, current_CO, FE_H2,current_H2, gc_current, gc_voltage, cathode_size, gc_measurement_time,normalized_res,_=\
        self.FE_calculation(filename,measurement_id, time_correction, raw_to_analyse)
        
        gc_measurement_time = [round((x-gc_measurement_time[0])/60/60,1) for x in gc_measurement_time]
        
        FE_CO_val = [100*x['value'] for x in FE_CO]
        FE_CO_err = [100*x['error'] for x in FE_CO]
        
        FE_H2_val = [100*x['value'] for x in FE_H2]
        FE_H2_err = [100*x['error'] for x in FE_H2]
        
        FE_sum = [sum(x) for x in zip(FE_CO_val,FE_H2_val)]
        FE_sum_err = [np.sqrt(FE_CO_err[x]**2 +FE_H2_err[x]**2) for x in range(len(FE_CO_err))]
        
        fig, FE_plot = plt.subplots()
        FE_plot.errorbar(gc_measurement_time,FE_CO_val,yerr=FE_CO_err, fmt='-o',label = 'CO',elinewidth = 0.8, capsize = 3)
        FE_plot.errorbar(gc_measurement_time,FE_H2_val,yerr=FE_H2_err, fmt='-^',label = 'H2',elinewidth = 0.8, capsize = 3)
        FE_plot.errorbar(gc_measurement_time,FE_sum, yerr =FE_sum_err, fmt='-s',label = 'SUM',elinewidth = 0.8, capsize = 3)
        
        FE_plot.legend(loc='best', shadow=True)
        FE_plot.set_xlabel('Time [h]')
        FE_plot.set_ylabel('Faraday efficiency')
        FE_plot.tick_params('y')
        #FE_plot.axes.set_ylim([0,1.5]) #y-axis
        FE_plot.set_title(plot_title)
        FE_plot.grid(True)
        #plt.setp(FE_plot,xticks = gc_measurement_time, xticklabels=time_ticks)
        #plt.setp(FE_plot.xaxis.get_majorticklabels(), rotation=-60 )
        plt.tight_layout()
        plt.draw()
    def plot_FE_n_to_time_voltage(self,filename,measurement_id,plot_title,time_correction = 0, raw_to_analyse = None):
        
        FE_CO, current_CO, FE_H2,current_H2, gc_current, gc_voltage, cathode_size, gc_measurement_time,normalized_res,_=\
        self.FE_calculation(filename,measurement_id, time_correction, raw_to_analyse)
        
        gc_measurement_time = [round((x-gc_measurement_time[0])/60/60,1) for x in gc_measurement_time]
        #time_ticks = [round((x-gc_measurement_time[0])/60/60,1) for x in gc_measurement_time]
        #time_ticks = [0,10,20,30,40,50,60,70,80]
        FE_CO_val = [100*x['value'] for x in FE_CO]
        FE_CO_err = [100*x['error'] for x in FE_CO]
        
        FE_H2_val = [100*x['value'] for x in FE_H2]
        FE_H2_err = [100*x['error'] for x in FE_H2]
        
        FE_sum = [sum(x) for x in zip(FE_CO_val,FE_H2_val)]
        FE_sum_err = [np.sqrt(FE_CO_err[x]**2 +FE_H2_err[x]**2) for x in range(len(FE_CO_err))]
        
        n_CO = np.array([normalized_res['CO'][index]['value']*10**6 for index in range(len(gc_measurement_time))])
        n_H2 = np.array([normalized_res['H2'][index]['value']*10**6 for index in range(len(gc_measurement_time))])
        n_CO2 = np.array([normalized_res['CO2'][index]['value']*10**6 for index in range(len(gc_measurement_time))])
        
        voltage = [x['value'] for x in gc_voltage]
        verr = [x['error'] for x in gc_voltage]
        
        fig, FE_plot = plt.subplots(2,1,sharex=True)
        FE_plot[0].errorbar(gc_measurement_time,FE_CO_val,yerr=FE_CO_err, fmt='-o',label = 'CO',elinewidth = 0.8, capsize = 3)
        FE_plot[0].errorbar(gc_measurement_time,FE_H2_val,yerr=FE_H2_err, fmt='-^',label = 'H2',elinewidth = 0.8, capsize = 3)
        FE_plot[0].errorbar(gc_measurement_time,FE_sum, yerr =FE_sum_err, fmt='-s',label = 'SUM',elinewidth = 0.8, capsize = 3)
        
        FE_plot[1].errorbar(gc_measurement_time,voltage,yerr=verr,elinewidth = 0.8, capsize = 3,fmt='-rd')
        #FE_plot[0].legend(shadow=True,loc=1,fontsize='xx-small',ncol=3)
        FE_plot[1].set_ylabel('Cell voltage [V]')
        FE_plot[0].set_ylabel('Faradaic efficiency [%]')
        FE_plot[0].tick_params('y')
        FE_plot[0].axes.set_ylim([0,100]) #y-axis        
        FE_plot[0].set_yticks(np.arange(0, 120, 20))
        FE_plot[1].set_yticks(np.arange(3.15,3.24,0.01))
        FE_plot[1].set_xlabel('Time [h]')
        #FE_plot.axes.set_ylim([0,1.5]) #y-axis
        #FE_plot[0].set_title(plot_title)
        FE_plot[0].grid(True)
        FE_plot[1].grid(True)
        #FE_plot[0].legend(shadow=True,bbox_to_anchor=(1.0,1.02), loc="lower right",
        #  borderaxespad=0, ncol=3, fontsize = 'xx-small')
        FE_plot[0].legend(frameon=False,loc='upper right', bbox_to_anchor=(1.03,0.04 ),ncol=3, fontsize='small')
        FE_plot[0].set_title(plot_title,fontsize=14)
        #plt.setp(FE_plot[1],xticks = gc_measurement_time, xticklabels=time_ticks)
        #plt.setp(FE_plot[1].xaxis.get_majorticklabels(), rotation=-60,fontsize=14 )
        plt.tight_layout()
        plt.draw()
        
        fig, nplot = plt.subplots(2,1,sharex=True)
        nplot[0].plot(gc_measurement_time,n_CO,'rx',label='CO')
        nplot[0].plot(gc_measurement_time,n_H2,'bo',label='H2')
        nplot[0].plot(gc_measurement_time,n_CO2,'kd',label='CO2')
        nplot[0].set_title(plot_title)
        nplot[0].legend(frameon=False,loc='best', shadow=True,fontsize='small')
        nplot[0].set_ylabel('Amount of Gas [$\mu$mol]')
        nplot[0].grid(True)
        nplot[0].set_yticks(np.arange(0, 11, 1))
        nplot[1].plot(gc_measurement_time,n_CO*100/(n_CO+n_H2), 'rx')
        nplot[1].plot(gc_measurement_time,n_H2*100/(n_CO+n_H2), 'bo')
        nplot[1].set_xlabel('Time [h]')
        nplot[1].set_ylabel('Selectivity [%]')
        nplot[1].set_yticks(np.arange(0, 110, 10))
        nplot[1].grid(True)
        plt.tight_layout()
        #plt.setp(nplot[1],xticks = gc_measurement_time, xticklabels=time_ticks)
        #plt.setp(nplot[1].xaxis.get_majorticklabels(), rotation=-60, fontsize=14)
        
    def raw_visualization(self,filepath,raw_to_analyse = None):
        
        all_raw_files = self.raw_file_search(filepath)
        #Visualize the raw data
        fig, ax_rainbow = plt.subplots()
        if raw_to_analyse is None:
            raw_to_analyse = slice(0,len(all_raw_files))
               
        for raw in all_raw_files[raw_to_analyse]:
            raw_file = Raw(raw)
            i = raw.rfind('\\')
            ax_rainbow.plot(np.linspace(0,raw_file.ad_header['Number of Data Points'],raw_file.ad_header['Number of Data Points'])/12.5/60,\
                            raw_file.raw_data_points, label = raw[i:]) #
        ax_rainbow.axes.set_title('TCD raw data')
        ax_rainbow.set_xlabel('Retention time [min]')
        ax_rainbow.set_ylabel('A.u.')
        ax_rainbow.tick_params('y')
        ax_rainbow.legend(loc=1, shadow=True, fontsize='xx-small')
        plt.tight_layout()
        plt.draw()
        
        print('Raw data has been plotted succesfully')
        print(' ')
    def plot_FE_V_to_current(self,filename,measurement_id,plot_title,time_correction = 0, raw_to_analyse = None):
        
        FE_CO, current_CO, FE_H2,current_H2,gc_current,gc_voltage, cathode_size, gc_measurement_time,_,_=\
        self.FE_calculation(filename,measurement_id, time_correction, raw_to_analyse)
        
        #print(current_H2)
        FE_CO_val = [100*x['value'] for x in FE_CO]
        FE_CO_err = [100*x['error'] for x in FE_CO]
        
        FE_H2_val = [100*x['value'] for x in FE_H2]
        FE_H2_err = [100*x['error'] for x in FE_H2]
        
        FE_sum = [sum(x) for x in zip(FE_CO_val,FE_H2_val)]
        FE_sum_err = [np.sqrt(FE_CO_err[x]**2 +FE_H2_err[x]**2) for x in range(len(FE_CO_err))]
        FE_sum_err = [FE_CO_err[x] + FE_H2_err[x] for x in range(len(FE_CO_err))]
        geo_current_density = [x['value']*1000/cathode_size for x in gc_current]
        x_err = [x['error']*1000/cathode_size for x in gc_current]
        
        voltage = [x['value'] for x in gc_voltage]
        verr = [x['error'] for x in gc_voltage]
        errorbar_t=3
        #print(geo_current_density)
        fig, FE_plot = plt.subplots(2,1,sharex=True)
        fig.subplots_adjust(hspace=0)
        FE_plot[0].errorbar(geo_current_density,FE_CO_val, xerr=x_err,yerr=FE_CO_err, fmt='-o',label = 'CO',elinewidth = errorbar_t, capsize = 3)
        FE_plot[0].errorbar(geo_current_density,FE_H2_val,xerr=x_err,yerr=FE_H2_err, fmt='-^',label = 'H2',elinewidth = errorbar_t, capsize = 3)
        FE_plot[0].errorbar(geo_current_density,FE_sum,xerr=x_err,yerr =FE_sum_err, fmt='-s',label = 'SUM',elinewidth = errorbar_t, capsize = 3)
        FE_plot[1].errorbar(geo_current_density,voltage,xerr=x_err,yerr=verr,elinewidth = 0.8, capsize = 3,fmt='-rd')
        #FE_plot[0].legend(shadow=True,loc='best',fontsize='xx-small',ncol=3)
        #FE_plot[0].legend(frameon=False, loc=1, ncol=3, fontsize = 'small')
        FE_plot[0].legend(frameon=False,loc='upper right', bbox_to_anchor=(1.03,1.04 ),ncol=3, fontsize='small')
        FE_plot[1].set_xlabel('Geometric current density [mA/cm$^2$]')
        FE_plot[0].set_ylabel('Faradaic efficiency [%]')
        FE_plot[1].set_ylabel('Cell voltage [V]')
        FE_plot[0].axes.set_ylim([0,140]) #y-axis        
        FE_plot[0].set_yticks(np.arange(0, 140, 20))
        FE_plot[1].set_yticks(np.arange(2.4,3.8,0.2))
        FE_plot[1].set_xticks(np.arange(0, 550, 50))
        FE_plot[0].set_xticks(np.arange(0, 550, 50))

        FE_plot[0].set_title(plot_title, fontsize=14)
        FE_plot[0].grid(True)
        FE_plot[1].grid(True)
        plt.tight_layout(pad=0.4)
        plt.draw()
        #plt.savefig(r'..\Finished thesis\Presentation figures'+plot_title,
        #           dpi=300,format = 'png')
        
        
#faraday_eff = FE_calculator('raw_files\\25052018',215)

#faraday_CO, faraday_H2, geo_current_density = faraday_eff.FE_calculation()

""" ----- Patrick's/"original" script edited 18th of May 2020 by ceshuca ----- """

# class FE_calculator():
    
#     def __init__(self,fit_info, iv_average = int(5), bump = None, peak_rise = None):
        
#         # Import the calibration file                                           # ?
#         self.calibration = self.load_obj(name = 'calibrations_direct_CO_pressure_corrected_4')
#         # Constants
#         self.number_of_electrons = 2
#         self.faraday_const = 96485.33289                                        # C/mol
#         gas_constant = 0.08314472                                               # L bar mol^-1 K^-1
#         self.bump = bump                                                        # ?
#         self.peak_rise = peak_rise                                              # ?
        
#         # normal volume is the volume of 1 mole of gas at 1 atm and 0 celcius
#         self.normal_volume = gas_constant*273.15/1.01325
        
#         self.fit_info = fit_info
#         self.detector = 'TCD'                                                   # what is it's the FID detector?
        
#         # define the number of datapoints to average over in the current, voltage
#         # and flow calculations
#         self.time_average_index = iv_average # seconds
    
#     def load_obj(self,name):
#         "Load files from folder obj. fx. calibration file"
#         with open('obj/' + name + '.pkl', 'rb') as f:
#             return pickle.load(f)
        
#     def uncertainty(self,*args):
#         "Calculate the uncertainty on the value as root of squared fractional\
#         uncertainties and return relative error"
#         uncertainties = []
#         for arg in args:
#             #print(arg['value'], arg['error'])
#             uncertainties.append((arg['error']/arg['value'])**2)
        
#         error = np.sqrt(sum(uncertainties))
#         #print(error)
#         return error
            
#     def raw_file_search(self, filepath, raw_to_analyse):
#         "search for raw files in the specified folder"
#         all_raw_files = []
#         print("Searching for raw files")
#         for root, dirs, files in walk("{}".format(filepath)):
#             for file_ in files:
#                 if path.splitext(file_)[1] == '.raw':
#                     all_raw_files.append(path.join(root, file_))
#         if len(all_raw_files) == 0:
#             print("Done! However, no files were found in".format(filepath))
#         else:
#             print("Done! Found {}".format(len(all_raw_files)))
            
#         if raw_to_analyse is None:
#             return all_raw_files
#         else:
#             return all_raw_files[raw_to_analyse]
    
#     def get_area_from_raw(self, list_of_rawfiles):
#         "get_area_from_raw(list_of_rawfiles)-> gc_time, TCD_res[fit_info.peak]"
        
#         "TCD_res[peak] is a dictionary of area corresponding to define peaks in\
#          fit info"
#         # List of time stamp of each chromatogram. E.g. 1537569193
#         gc_measurement_time = []
#         # Dict which contains for all peaks(gases) the intensity
#         TCD_res = {}
#         for peak in self.fit_info[self.detector]:
#             TCD_res[peak]=[]
            
#         for raw in list_of_rawfiles:
#             #print('Integrating spectrum in rawfile: {}'.format(raw))
#             gc_integrator = GCIntegrator(raw,self.fit_info)
#             raw_data = Raw(raw)
#             gc_measurement_time.append(raw_data.raw_data_header['data_header']['time_and_date_created'])

#             peak_integration = gc_integrator.integrate_spectrum(self.bump,self.peak_rise)
#             print(peak_integration)
                
#             for peak in self.fit_info[self.detector]:
#                 TCD_res[peak].append(peak_integration['erf'][peak])
                
#         print('Integration complete')
#         #print(TCD_res)
#         return gc_measurement_time, TCD_res
    
#     def show_fitting(self,filepath, raw_to_analyse = None):
#         """
#         Parameters
#         ----------
#         filepath : TYPE
#             DESCRIPTION.
#         raw_to_analyse : TYPE, optional
#             DESCRIPTION. The default is None.

#         Returns
#         -------
#         None.

#         """
#         "Use this function to show how the background is fitted"
#         # gets the GC raw files
#         list_of_rawfiles = self.raw_file_search(filepath, raw_to_analyse)
        
#         n_row = len(list_of_rawfiles)
#         n_col = len(self.fit_info[self.detector])

#         fig, axs = plt.subplots(n_row, n_col, figsize = (3*n_col,n_row), 
#                                 sharex='col', sharey = False, squeeze=True)
        
#         for j,peak in enumerate(self.fit_info[self.detector]):
            
#             for ax, raw in enumerate(list_of_rawfiles):
#                 gc_integrator = GCIntegrator(raw,self.fit_info)
                
#                 if self.bump is not None and self.peak_rise is not None:
#                     gc_integrator.plot_background_fitting(axs[ax,j], peak,self.bump,self.peak_rise)
#                 else:
#                     gc_integrator.plot_background_fitting(axs[ax,j], peak)
#             # for raw in list_of_rawfiles:
#             #     gc_integrator = GCIntegrator(raw,self.fit_info)
#                 # if self.bump is not None and self.peak_rise is not None:
#                 #     gc_integrator.plot_background(self.bump,self.peak_rise)
#                 # else:
#                 #     gc_integrator.plot_background()
#                 axs[ax,j].ticklabel_format(axis='y', style='sci', scilimits=(0,0))
                
#             #fig.subplots_adjust()
#         plt.tight_layout()
#         fig.subplots_adjust(wspace=0.5, hspace=0)
#         #plt.draw()
#         plt.show()
#         plt.savefig('ceshuca.png')
#         #plt.close(fig)
        
#         # if save_file:
#         #     plt.savefig(save_file)
#         #     plt.close(fig)
#         # else:
#         #     plt.show()
        
#     def show_fitting_all_figures(self,filepath, raw_to_analyse = None):
#         "Use this function to show how the background is fitted"
#         # gets the GC raw files
#         list_of_rawfiles = self.raw_file_search(filepath)
#         if raw_to_analyse is None:
#             raw_to_analyse = slice(0,len(list_of_rawfiles))

                
#         for raw in list_of_rawfiles:
#             gc_integrator = GCIntegrator(raw,self.fit_info)
#             if self.bump is not None and self.peak_rise is not None:
#                 gc_integrator.plot_background(self.bump,self.peak_rise)
#             else:
#                 gc_integrator.plot_background()
 

    
#     def get_iv_data(self,measurement_id):
#         "Import the iv data correpsonding to the measurement ID of the voltage measurement"
#         "get_iv_data(measurement_id) -> iv_data{'time':,'voltage':,'current':,'CO2_flow':}, cathode_size"
#         iv_database = Cinfdata('large_CO2_MEA')
#         print(iv_database)
#         # get the size of the cathode to normalize the current
#         metadata = iv_database.get_metadata(measurement_id)
#         index1 = metadata['cathode_catalyst_description'].find(':')
#         index2 = metadata['cathode_catalyst_description'].rfind('cm2')
#         cathode_size = float(metadata['cathode_catalyst_description'][index1+1:index2].lstrip())
        
#         # Get the I, V and flow data corresponding to the GC measurements.
#         iv_data = { 'time' : iv_database.get_data(measurement_id)[:,0],
#                     'voltage' : iv_database.get_data(measurement_id)[:,1],
#                     'current' : iv_database.get_data(measurement_id+1)[:,1],
#                     'CO2_flow' : iv_database.get_data(measurement_id+2)[:,1],
#                     }
        
#         return iv_data, cathode_size
    
#     def iv_gc_comparison(self,gc_measurement_times,iv_data,time_correction = 0):
#         "Compare the timestamp of the GC-measurement and the IV data and select\
#         corresponding iv and flow data for calculations"
#         # initialize the GC_iv comparisons as dicts with std. and mean
        
#         # The error on the current reading is 0.3% +- 20 mA
#         gc_inlet_flow =[]
#         gc_current =[]
#         gc_voltage =[]
#         corrected_measurement_times = [x-time_correction for x in gc_measurement_times]
        
#         for gc_time in corrected_measurement_times:
#             gc_iv_index = min(range(len(iv_data['time'])), key=lambda i: abs(iv_data['time'][i]-gc_time))

#             if gc_iv_index - self.time_average_index < 0:
#                 iv_index_mask = np.logical_and(iv_data['time'][0],
#                                                iv_data['time']<iv_data['time'][gc_iv_index])
#             else:
#                 iv_index_mask = np.logical_and(iv_data['time']>iv_data['time'][gc_iv_index-self.time_average_index],
#                                                    iv_data['time']<iv_data['time'][gc_iv_index])
            
            
#             # The error on the current reading is 0.3% +- 20 mA
#             v_current = np.mean(iv_data['current'][iv_index_mask])
#             e_current = sum([np.std(iv_data['current'][iv_index_mask]),(20/(1000)),(0.3/100)*v_current])
#             gc_current.append({'value':v_current,
#                                'error':e_current})
            
#             # The error on the voltage reading is 0.5%
#             v_voltage = np.mean(iv_data['voltage'][iv_index_mask])
#             e_voltage = sum([np.std(iv_data['voltage'][iv_index_mask]),(0.05/100)*v_voltage])
#             gc_voltage.append({'value':v_voltage,'error':e_voltage})

            
#         for gc_time in gc_measurement_times:
#             gc_iv_index = min(range(len(iv_data['time'])), key=lambda i: abs(iv_data['time'][i]-gc_time))
#             if gc_iv_index - self.time_average_index < 0:
#                 flow_index_mask = np.logical_and(iv_data['time'][0],
#                                                iv_data['time']<iv_data['time'][gc_iv_index])
#             else:
#                 flow_index_mask = np.logical_and(iv_data['time']>iv_data['time'][gc_iv_index-self.time_average_index],
#                                                    iv_data['time']<iv_data['time'][gc_iv_index])
            
#             # Accuracy of the flowcontroller is 1% of full scale
            
#             v_flow = np.mean(iv_data['CO2_flow'][flow_index_mask])
#             e_flow = sum([np.std(iv_data['CO2_flow'][flow_index_mask]),(1/100)*200]) 
#             gc_inlet_flow.append({'value':v_flow,'error':e_flow})
            
#         #print(gc_inlet_flow,gc_current,gc_voltage)
#         return gc_inlet_flow, gc_current, gc_voltage
        
#     def FE_calculation(self,filename,measurement_id, time_correction=0, raw_to_analyse = None):
#         """Do Faradaic efficiency calculation
        
#         time_correction: "correction to get the right current value"
#         raw_to_analyse: "slice of raw files"
        
#         """
#         # Import of CHOSEN GC data to use in the calculation
#         list_of_rawfiles = self.raw_file_search(filename, raw_to_analyse)

#         " peak integration etc"
#         gc_measurement_time, TCD_res = self.get_area_from_raw(list_of_rawfiles)
        
#         iv_data, cathode_size = self.get_iv_data(measurement_id)
        
#         gc_inlet_flow, gc_current, gc_voltage = self.iv_gc_comparison(gc_measurement_time,iv_data,time_correction)
        
#         # Find the amount of moles of each component from the calibration
#         normalized_res = {}
#         for peak in self.fit_info[self.detector]:
#             normalized_res[peak] = []
            
#             for area in TCD_res[peak]:
#                 val = (area/self.calibration[peak]['slope'])
#                 err = self.calibration[peak]['col_std']
#                 normalized_res[peak].append({'value':val,
#                                          'error':err*val})
        
#         # Calculate the flow of CO
#         gc_flow_CO = []
#         for index in range(len(gc_inlet_flow)):
#             val = normalized_res['CO'][index]['value']/(normalized_res['CO'][index]['value']\
#                                 +normalized_res['CO2'][index]['value'])*gc_inlet_flow[index]['value']
#             err = self.uncertainty(normalized_res['CO'][index],normalized_res['CO2'][index],gc_inlet_flow[index])
#             gc_flow_CO.append({'value':val,
#                                 'error':err*val})
            
#         # current to CO and H2 in amps
#         current_CO = []
#         for index in range(len(gc_flow_CO)):
#             val = self.number_of_electrons*gc_flow_CO[index]['value']*self.faraday_const/(self.normal_volume*1000*60)
#             err = self.uncertainty(gc_flow_CO[index])
#             current_CO.append({'value':val,'error':err*val})
        
#         current_H2 = []
#         for index in range(len(gc_flow_CO)):
#             val = current_CO[index]['value']*normalized_res['H2'][index]['value']/normalized_res['CO'][index]['value']
#             err = self.uncertainty(current_CO[index],normalized_res['H2'][index],normalized_res['CO'][index])
#             current_H2.append({'value':val,
#                                'error':err*val})
            
#         faraday_eff_CO = []
#         for index in range(len(current_CO)):
#             val = current_CO[index]['value']/gc_current[index]['value']
#             err = self.uncertainty(current_CO[index],gc_current[index])
#             faraday_eff_CO.append({'value':val,
#                                    'error':err*val})
        
#         faraday_eff_H2 = []
#         for index in range(len(current_H2)):
#             val = current_H2[index]['value']/gc_current[index]['value']
#             err = self.uncertainty(current_H2[index],gc_current[index])
#             faraday_eff_H2.append({'value':val,'error':err*val})
        
#         return faraday_eff_CO, current_CO, faraday_eff_H2,current_H2,\
#                 gc_current,gc_voltage, cathode_size, gc_measurement_time,normalized_res,gc_inlet_flow
        
#     def plot_iv_correction(self,filename,measurement_id,plot_title = 'A title',time_correction = 0, raw_to_analyse = None):
#         "Tool to show where the GC measurement is taken in the IV data"
#         list_of_rawfiles = self.raw_file_search(filename)
#         if raw_to_analyse is None:
#             raw_to_analyse = slice(0,len(list_of_rawfiles))
        
#         gc_measurement_time, TCD_res = self.get_area_from_raw(list_of_rawfiles)
#         iv_data, cathode_size = self.get_iv_data(measurement_id)
#         #print('save_rate for {} is {} s'.format(plot_title,(iv_data['time'][10]-iv_data['time'][9])))
        
#         gc_inlet_flow, gc_current, gc_voltage = self.iv_gc_comparison(gc_measurement_time,iv_data, time_correction)
#         gc_measurement_time[:] = [round((x-time_correction-iv_data['time'][0])/3600,1) for x in gc_measurement_time]
#         time_values = [round((x-iv_data['time'][0])/3600,1) for x in iv_data['time']]
#         current_plot_vals = [x['value']*1000/cathode_size for x in gc_current]
#         #voltage_plot_vals = [x['value'] for x in gc_voltage]
        
#         fig, ax1 = plt.subplots()
        
#         save_rate = (iv_data['time'][500]-iv_data['time'][499])
#         color = 'tab:red'
#         ax1.set_xlabel('Time [h]')
#         ax1.set_ylabel('Geometric current density [mA/cm$^2$]')
#         ax1.tick_params(axis='y', labelcolor=color)
#         ax1.plot(time_values[int(3.5*3600/save_rate):-1],[x*1000/cathode_size for x in iv_data['current'][int(3.5*3600/save_rate):-1]],color=color)
#         ax1.plot(gc_measurement_time,current_plot_vals,'kx', label = 'GC measurement, time correction: {} min'.format(time_correction/60))
#         ax1.legend(loc=4, shadow=True, fontsize='xx-small')
#         ax1.set_title(plot_title)
#         ax1.set_ylim([0, 550])
#         ax1.set_yticks(np.arange(0, 550, 50))
#         ax1.grid(True)
        
#         ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

#         color = 'tab:blue'
#         ax2.plot(time_values,iv_data['voltage'], color=color)
#         ax2.set_ylabel('Voltage [V]', color=color)  # we already handled the x-label with ax1
#         ax2.tick_params(axis='y', labelcolor=color)
#         #ax2.set_yticks(np.arange(2, 3.8, 0.2))
#         ax2.set_ylim([0, 4])
        
#         fig.tight_layout()  # otherwise the right y-label is slightly clipped
#         plt.draw()
    
#     def plot_FE_to_current(self,filename,measurement_id,plot_title,time_correction = 0, raw_to_analyse = None):
        
#         FE_CO, current_CO, FE_H2,current_H2,gc_current,gc_voltage, cathode_size, gc_measurement_time,_,_=\
#         self.FE_calculation(filename,measurement_id, time_correction, raw_to_analyse)
        
#         #print(current_H2)
#         FE_CO_val = [x['value'] for x in FE_CO]
#         FE_CO_err = [x['error'] for x in FE_CO]
        
#         FE_H2_val = [x['value'] for x in FE_H2]
#         FE_H2_err = [x['error'] for x in FE_H2]
        
#         FE_sum = [sum(x) for x in zip(FE_CO_val,FE_H2_val)]
#         FE_sum_err = [np.sqrt(FE_CO_err[x]**2 +FE_H2_err[x]**2) for x in range(len(FE_CO_err))]
#         geo_current_density = [x['value']*1000/cathode_size for x in gc_current]
#         x_err = [x['error']*1000/cathode_size for x in gc_current]
#         #print(geo_current_density)
#         fig, FE_plot = plt.subplots()
#         FE_plot.errorbar(geo_current_density,FE_CO_val, xerr=x_err,yerr=FE_CO_err, fmt='-o',label = 'CO',elinewidth = 0.8, capsize = 3)
#         FE_plot.errorbar(geo_current_density,FE_H2_val,xerr=x_err,yerr=FE_H2_err, fmt='-^',label = 'H2',elinewidth = 0.8, capsize = 3)
#         FE_plot.errorbar(geo_current_density,FE_sum,xerr=x_err,yerr =FE_sum_err, fmt='-s',label = 'SUM',elinewidth = 0.8, capsize = 3)
#         FE_plot.legend(shadow=True,loc=1,fontsize='xx-small',ncol=3)
# #        FE_plot.legend(shadow=True,loc='center left', bbox_to_anchor=(1, 0.5))
#         FE_plot.set_xlabel('Geometric current density [mA/cm$^2$]')
#         FE_plot.set_ylabel('Faraday efficiency')
#         FE_plot.tick_params('y')
#         FE_plot.set_yticks(np.arange(0, 1.4, 0.2))
#         FE_plot.axes.set_ylim([0,1.4]) #y-axis
#         FE_plot.set_title(plot_title)
#         FE_plot.grid(True)
#         plt.tight_layout()
#         plt.draw()
#     def plot_FE_to_voltage(self,filename,measurement_id,plot_title,time_correction = 0, raw_to_analyse = None):
        
#         FE_CO, current_CO, FE_H2,current_H2, gc_current,gc_voltage, cathode_size, gc_measurement_time,_,_=\
#         self.FE_calculation(filename,measurement_id, time_correction, raw_to_analyse)
        
#         FE_CO_val = [x['value']*100 for x in FE_CO]
#         FE_CO_err = [x['error']*100 for x in FE_CO]
        
#         FE_H2_val = [x['value']*100 for x in FE_H2]
#         FE_H2_err = [x['error']*100 for x in FE_H2]
        
#         FE_sum = [sum(x) for x in zip(FE_CO_val,FE_H2_val)]
#         FE_sum_err = [np.sqrt(FE_CO_err[x]**2 +FE_H2_err[x]**2) for x in range(len(FE_CO_err))]
#         x_vals = [x['value'] for x in gc_voltage]
#         x_err = [x['error'] for x in gc_voltage]
        
#         fig, FE_plot = plt.subplots()
#         FE_plot.errorbar(x_vals,FE_CO_val,xerr=x_err,yerr=FE_CO_err, fmt='-o',label = 'CO',elinewidth = 0.8, capsize = 3)
#         FE_plot.errorbar(x_vals,FE_H2_val,xerr=x_err,yerr=FE_H2_err, fmt='-^',label = 'H2',elinewidth = 0.8, capsize = 3)
#         FE_plot.errorbar(x_vals,FE_sum,xerr =x_err, yerr =FE_sum_err, fmt='-s',label = 'SUM',elinewidth = 0.8, capsize = 3)
#         FE_plot.legend(shadow=True,loc=1,fontsize='xx-small',ncol=3)
#         #FE_plot.legend(loc='best', shadow=True)
#         FE_plot.set_xlabel('Cell voltage [V]')
#         FE_plot.set_ylabel('Faraday efficiency')
#         FE_plot.tick_params('y')
#         #FE_plot.axes.set_ylim([0,1.2]) #y-axis
#         FE_plot.set_title(plot_title)
#         FE_plot.grid(True)
#         plt.tight_layout()
#         plt.draw()
#     def plot_FE_to_time(self,filename,measurement_id,plot_title,time_correction = 0, raw_to_analyse = None):
        
#         FE_CO, current_CO, FE_H2,current_H2, gc_current, gc_voltage, cathode_size, gc_measurement_time,normalized_res,_=\
#         self.FE_calculation(filename,measurement_id, time_correction, raw_to_analyse)
        
#         gc_measurement_time = [round((x-gc_measurement_time[0])/60/60,1) for x in gc_measurement_time]
        
#         FE_CO_val = [100*x['value'] for x in FE_CO]
#         FE_CO_err = [100*x['error'] for x in FE_CO]
        
#         FE_H2_val = [100*x['value'] for x in FE_H2]
#         FE_H2_err = [100*x['error'] for x in FE_H2]
        
#         FE_sum = [sum(x) for x in zip(FE_CO_val,FE_H2_val)]
#         FE_sum_err = [np.sqrt(FE_CO_err[x]**2 +FE_H2_err[x]**2) for x in range(len(FE_CO_err))]
        
#         fig, FE_plot = plt.subplots()
#         FE_plot.errorbar(gc_measurement_time,FE_CO_val,yerr=FE_CO_err, fmt='-o',label = 'CO',elinewidth = 0.8, capsize = 3)
#         FE_plot.errorbar(gc_measurement_time,FE_H2_val,yerr=FE_H2_err, fmt='-^',label = 'H2',elinewidth = 0.8, capsize = 3)
#         FE_plot.errorbar(gc_measurement_time,FE_sum, yerr =FE_sum_err, fmt='-s',label = 'SUM',elinewidth = 0.8, capsize = 3)
        
#         FE_plot.legend(loc='best', shadow=True)
#         FE_plot.set_xlabel('Time [h]')
#         FE_plot.set_ylabel('Faraday efficiency')
#         FE_plot.tick_params('y')
#         #FE_plot.axes.set_ylim([0,1.5]) #y-axis
#         FE_plot.set_title(plot_title)
#         FE_plot.grid(True)
#         #plt.setp(FE_plot,xticks = gc_measurement_time, xticklabels=time_ticks)
#         #plt.setp(FE_plot.xaxis.get_majorticklabels(), rotation=-60 )
#         plt.tight_layout()
#         plt.draw()
#     def plot_FE_n_to_time_voltage(self,filename,measurement_id,plot_title,time_correction = 0, raw_to_analyse = None):
        
#         FE_CO, current_CO, FE_H2,current_H2, gc_current, gc_voltage, cathode_size, gc_measurement_time,normalized_res,_=\
#         self.FE_calculation(filename,measurement_id, time_correction, raw_to_analyse)
        
#         gc_measurement_time = [round((x-gc_measurement_time[0])/60/60,1) for x in gc_measurement_time]
#         #time_ticks = [round((x-gc_measurement_time[0])/60/60,1) for x in gc_measurement_time]
#         #time_ticks = [0,10,20,30,40,50,60,70,80]
#         FE_CO_val = [100*x['value'] for x in FE_CO]
#         FE_CO_err = [100*x['error'] for x in FE_CO]
        
#         FE_H2_val = [100*x['value'] for x in FE_H2]
#         FE_H2_err = [100*x['error'] for x in FE_H2]
        
#         FE_sum = [sum(x) for x in zip(FE_CO_val,FE_H2_val)]
#         FE_sum_err = [np.sqrt(FE_CO_err[x]**2 +FE_H2_err[x]**2) for x in range(len(FE_CO_err))]
        
#         n_CO = np.array([normalized_res['CO'][index]['value']*10**6 for index in range(len(gc_measurement_time))])
#         n_H2 = np.array([normalized_res['H2'][index]['value']*10**6 for index in range(len(gc_measurement_time))])
#         n_CO2 = np.array([normalized_res['CO2'][index]['value']*10**6 for index in range(len(gc_measurement_time))])
        
#         voltage = [x['value'] for x in gc_voltage]
#         verr = [x['error'] for x in gc_voltage]
        
#         fig, FE_plot = plt.subplots(2,1,sharex=True)
#         FE_plot[0].errorbar(gc_measurement_time,FE_CO_val,yerr=FE_CO_err, fmt='-o',label = 'CO',elinewidth = 0.8, capsize = 3)
#         FE_plot[0].errorbar(gc_measurement_time,FE_H2_val,yerr=FE_H2_err, fmt='-^',label = 'H2',elinewidth = 0.8, capsize = 3)
#         FE_plot[0].errorbar(gc_measurement_time,FE_sum, yerr =FE_sum_err, fmt='-s',label = 'SUM',elinewidth = 0.8, capsize = 3)
        
#         FE_plot[1].errorbar(gc_measurement_time,voltage,yerr=verr,elinewidth = 0.8, capsize = 3,fmt='-rd')
#         #FE_plot[0].legend(shadow=True,loc=1,fontsize='xx-small',ncol=3)
#         FE_plot[1].set_ylabel('Cell voltage [V]')
#         FE_plot[0].set_ylabel('Faradaic efficiency [%]')
#         FE_plot[0].tick_params('y')
#         FE_plot[0].axes.set_ylim([0,100]) #y-axis        
#         FE_plot[0].set_yticks(np.arange(0, 120, 20))
#         FE_plot[1].set_yticks(np.arange(3.15,3.24,0.01))
#         FE_plot[1].set_xlabel('Time [h]')
#         #FE_plot.axes.set_ylim([0,1.5]) #y-axis
#         #FE_plot[0].set_title(plot_title)
#         FE_plot[0].grid(True)
#         FE_plot[1].grid(True)
#         #FE_plot[0].legend(shadow=True,bbox_to_anchor=(1.0,1.02), loc="lower right",
#         #  borderaxespad=0, ncol=3, fontsize = 'xx-small')
#         FE_plot[0].legend(frameon=False,loc='upper right', bbox_to_anchor=(1.03,0.04 ),ncol=3, fontsize='small')
#         FE_plot[0].set_title(plot_title,fontsize=14)
#         #plt.setp(FE_plot[1],xticks = gc_measurement_time, xticklabels=time_ticks)
#         #plt.setp(FE_plot[1].xaxis.get_majorticklabels(), rotation=-60,fontsize=14 )
#         plt.tight_layout()
#         plt.draw()
        
#         fig, nplot = plt.subplots(2,1,sharex=True)
#         nplot[0].plot(gc_measurement_time,n_CO,'rx',label='CO')
#         nplot[0].plot(gc_measurement_time,n_H2,'bo',label='H2')
#         nplot[0].plot(gc_measurement_time,n_CO2,'kd',label='CO2')
#         nplot[0].set_title(plot_title)
#         nplot[0].legend(frameon=False,loc='best', shadow=True,fontsize='small')
#         nplot[0].set_ylabel('Amount of Gas [$\mu$mol]')
#         nplot[0].grid(True)
#         nplot[0].set_yticks(np.arange(0, 11, 1))
#         nplot[1].plot(gc_measurement_time,n_CO*100/(n_CO+n_H2), 'rx')
#         nplot[1].plot(gc_measurement_time,n_H2*100/(n_CO+n_H2), 'bo')
#         nplot[1].set_xlabel('Time [h]')
#         nplot[1].set_ylabel('Selectivity [%]')
#         nplot[1].set_yticks(np.arange(0, 110, 10))
#         nplot[1].grid(True)
#         plt.tight_layout()
#         #plt.setp(nplot[1],xticks = gc_measurement_time, xticklabels=time_ticks)
#         #plt.setp(nplot[1].xaxis.get_majorticklabels(), rotation=-60, fontsize=14)
        
#     def raw_visualization(self,filepath,raw_to_analyse = None):
        
#         all_raw_files = self.raw_file_search(filepath)
#         #Visualize the raw data
#         fig, ax_rainbow = plt.subplots()
#         if raw_to_analyse is None:
#             raw_to_analyse = slice(0,len(all_raw_files))
               
#         for raw in all_raw_files[raw_to_analyse]:
#             raw_file = Raw(raw)
#             i = raw.rfind('\\')
#             ax_rainbow.plot(np.linspace(0,raw_file.ad_header['Number of Data Points'],raw_file.ad_header['Number of Data Points'])/12.5/60,\
#                             raw_file.raw_data_points, label = raw[i:]) #
#         ax_rainbow.axes.set_title('TCD raw data')
#         ax_rainbow.set_xlabel('Retention time [min]')
#         ax_rainbow.set_ylabel('A.u.')
#         ax_rainbow.tick_params('y')
#         ax_rainbow.legend(loc=1, shadow=True, fontsize='xx-small')
#         plt.tight_layout()
#         plt.draw()
        
#         print('Raw data has been plotted succesfully')
#         print(' ')
#     def plot_FE_V_to_current(self,filename,measurement_id,plot_title,time_correction = 0, raw_to_analyse = None):
        
#         FE_CO, current_CO, FE_H2,current_H2,gc_current,gc_voltage, cathode_size, gc_measurement_time,_,_=\
#         self.FE_calculation(filename,measurement_id, time_correction, raw_to_analyse)
        
#         #print(current_H2)
#         FE_CO_val = [100*x['value'] for x in FE_CO]
#         FE_CO_err = [100*x['error'] for x in FE_CO]
        
#         FE_H2_val = [100*x['value'] for x in FE_H2]
#         FE_H2_err = [100*x['error'] for x in FE_H2]
        
#         FE_sum = [sum(x) for x in zip(FE_CO_val,FE_H2_val)]
#         FE_sum_err = [np.sqrt(FE_CO_err[x]**2 +FE_H2_err[x]**2) for x in range(len(FE_CO_err))]
#         FE_sum_err = [FE_CO_err[x] + FE_H2_err[x] for x in range(len(FE_CO_err))]
#         geo_current_density = [x['value']*1000/cathode_size for x in gc_current]
#         x_err = [x['error']*1000/cathode_size for x in gc_current]
        
#         voltage = [x['value'] for x in gc_voltage]
#         verr = [x['error'] for x in gc_voltage]
#         errorbar_t=3
#         #print(geo_current_density)
#         fig, FE_plot = plt.subplots(2,1,sharex=True)
#         fig.subplots_adjust(hspace=0)
#         FE_plot[0].errorbar(geo_current_density,FE_CO_val, xerr=x_err,yerr=FE_CO_err, fmt='-o',label = 'CO',elinewidth = errorbar_t, capsize = 3)
#         FE_plot[0].errorbar(geo_current_density,FE_H2_val,xerr=x_err,yerr=FE_H2_err, fmt='-^',label = 'H2',elinewidth = errorbar_t, capsize = 3)
#         FE_plot[0].errorbar(geo_current_density,FE_sum,xerr=x_err,yerr =FE_sum_err, fmt='-s',label = 'SUM',elinewidth = errorbar_t, capsize = 3)
#         FE_plot[1].errorbar(geo_current_density,voltage,xerr=x_err,yerr=verr,elinewidth = 0.8, capsize = 3,fmt='-rd')
#         #FE_plot[0].legend(shadow=True,loc='best',fontsize='xx-small',ncol=3)
#         #FE_plot[0].legend(frameon=False, loc=1, ncol=3, fontsize = 'small')
#         FE_plot[0].legend(frameon=False,loc='upper right', bbox_to_anchor=(1.03,1.04 ),ncol=3, fontsize='small')
#         FE_plot[1].set_xlabel('Geometric current density [mA/cm$^2$]')
#         FE_plot[0].set_ylabel('Faradaic efficiency [%]')
#         FE_plot[1].set_ylabel('Cell voltage [V]')
#         FE_plot[0].axes.set_ylim([0,140]) #y-axis        
#         FE_plot[0].set_yticks(np.arange(0, 140, 20))
#         FE_plot[1].set_yticks(np.arange(2.4,3.8,0.2))
#         FE_plot[1].set_xticks(np.arange(0, 550, 50))
#         FE_plot[0].set_xticks(np.arange(0, 550, 50))

#         FE_plot[0].set_title(plot_title, fontsize=14)
#         FE_plot[0].grid(True)
#         FE_plot[1].grid(True)
#         plt.tight_layout(pad=0.4)
#         plt.draw()
#         #plt.savefig(r'..\Finished thesis\Presentation figures'+plot_title,
#         #           dpi=300,format = 'png')
        
        
# #faraday_eff = FE_calculator('raw_files\\25052018',215)

# #faraday_CO, faraday_H2, geo_current_density = faraday_eff.FE_calculation()

        