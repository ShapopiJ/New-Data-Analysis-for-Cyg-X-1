import numpy as np
import matplotlib.pyplot as plt

import argparse
Input = argparse.ArgumentParser(description = "Please pass all these arguments in sequence:")
Input.add_argument('data_file', type = str,  nargs = 1, help = 'Data file name')
Input.add_argument('title', type = str, nargs = 1, help = 'Plot title')
args = Input.parse_args()
data_file = args.data_file[0]
title = args.title[0]

#Load data
mjd, flux, error = np.loadtxt(data_file, unpack = True, usecols = (0, 1, 2))      #data
#remove negative flux'
mjd_filtered = [mjd[i] for i in range(len(flux)) if flux[i] > 0.0] #remove negative fluxes
error_filtered = [error[i] for i in range(len(flux)) if flux[i] > 0.0]
flux_filtered = [flux[i] for i in range(len(flux)) if flux[i] > 0.0]

#plotting
fig = plt.figure(1, figsize=(30,15))
plt.errorbar(mjd_filtered, 
    flux_filtered, 
    error_filtered, 
    fmt='r.', 
    barsabove=True,
    ms = 2,
    elinewidth=0.3,
    ecolor='black')

#plt.rc('font', size=30)
plt.ylabel("flux $[keV\ cm^{-2}\ s^{-1}]$ ")
plt.xlabel("MJD")
plt.title(title+'Light Curve')
plt.savefig('LC_'+title+'.png')