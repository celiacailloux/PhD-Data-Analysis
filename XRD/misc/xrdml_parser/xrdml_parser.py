"""
Script for parsing ".xrdml" files, generated by the XRD equipment at DTU Physics.

There are two parts of this script: 
    The definition of the parser-functions.
    An example of the use of the functions
"""
import numpy as np
import re
import pandas as pd


#wave_length of source
def read_xrdml_wavelength(path):
    raw_file = open(path)
    lines = raw_file.readlines()
    for index, line in enumerate(lines):
        if line.find('<usedWavelength intended="K-Alpha 1">') != -1:
            kAlpha1 = [float(value) for value in re.findall(r'\d+\.\d+',lines[index+1])]
            kAlpha2 = [float(value) for value in re.findall(r'\d+\.\d+',lines[index+2])]
            ratio_kA2_over_kA1 = [float(value) for value in re.findall(r'\d+\.\d+',lines[index+4])]
            wavelength = (ratio_kA2_over_kA1[0]*kAlpha2[0]+kAlpha1[0])/(ratio_kA2_over_kA1[0]+1)
            break
    return wavelength

#read spectrum
def read_xrdml_spectrum(path):
    file = open(path)
    lines = file.readlines()
    
    for index, line in enumerate(lines):
        if line.find('<positions axis="2Theta" unit="deg">') != -1:
            start_angle = [float(value) for value in re.findall(r'\d+\.\d+',lines[index+1])]
            end_angle = [float(value) for value in re.findall(r'\d+\.\d+',lines[index+2])]
        
        if line.find('intensities') != -1:
            spectrum = [float(value) for value in re.findall(r'\d+',lines[index])]
            spectrum = np.array(spectrum)
    
    angle_step = (end_angle[0]-start_angle[0])/len(spectrum)
    angles = np.arange(start_angle[0],end_angle[0],angle_step)
    return angles, spectrum

#Bragg's law, for angles to inverse length
def inverse_length(angles,wavelength):
    angles = np.pi*np.array(angles)/180
    return 2*np.sin(angles/2)/wavelength

# reads reference spectrum (csv file)
def read_ref_spectrum(path):
    file = pd.read_csv(path, delimiter = ',',names = ['angles', 'spectrum'], header = None)    
    angles = file['angles']
    spectrum = file['spectrum']
    return angles, spectrum
            
    
    

"""
example
"""
import matplotlib as mpl
from matplotlib import pyplot as plt


#fonts for matplotlib
font = {'family' : 'Palatino Linotype',
        #'weight' : 'bold',
        'size'   : 18}
mpl.rc('font', **font)

reffiles = ['test_ref1.csv']
files = ['test1.xrdml','test2.xrdml']
labels = ['Some sample','Some other sample'] #labels

fig, rainbow = plt.subplots() #rainbow is just the call-name of the figure
for file,n in zip(files,range(0,len(files))):
        spectrum = read_xrdml_spectrum(file)
        rainbow.plot(spectrum[0],spectrum[1],label=labels[n])
        
for file,n in zip(reffiles,range(0,len(files))):
        spectrum = read_ref_spectrum(file)
        rainbow.plot(spectrum[0],spectrum[1],label=labels[n])
    
rainbow.set_xlabel(r'2$\theta$ [degrees]')
rainbow.set_ylabel('Counts')
#rainbow.tick_params('y')
rainbow.axes.set_title('A fishy title')
rainbow.legend(loc=4)
#rainbow.axes.set_xlim(range)
plt.draw()

fig, rainbow = plt.subplots() #rainbow is just the call-name of the figure
for file,n in zip(files,range(0,len(files))):
        spectrum = read_xrdml_spectrum(file)
        rainbow.plot(inverse_length(spectrum[0],read_xrdml_wavelength(file)),spectrum[1],label=labels[n])
rainbow.set_xlabel(r'Scattering length [1/angstrom]')
rainbow.set_ylabel('Counts')
#rainbow.tick_params('y')
rainbow.axes.set_title('A fishy title, but with inverse length')
rainbow.legend(loc=4)
#rainbow.axes.set_xlim(range)
plt.draw()

plt.tight_layout()
plt.show() #printer figurne. Matplotlib gui'en kan zoome og flytte på grafen. "pil til venstre" går et skridt tilbage
