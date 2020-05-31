import numpy as np
import matplotlib.pyplot as plt

import argparse
Input = argparse.ArgumentParser(description = "Please pass all these arguments in sequence:")
Input.add_argument('x_ray_file', type = str,  nargs = 1, help = 'x-ray file name')
Input.add_argument('radio_file', type = str, nargs = 1, help = 'radio file name')
Input.add_argument('title', type = str, nargs = 1, help = 'Plot title')
args = Input.parse_args()
x_ray_file = args.x_ray_file[0]
radio_file = args.radio_file[0]
title = args.title[0]
limit = 0.5
r_mjd, r_flux = np.loadtxt(radio_file, unpack = True, usecols = (0,1))      #radio data
x_mjd, x_counts, x_err_counts = np.loadtxt(x_ray_file, unpack = True, usecols = (0,7,8))    #x-ray mjd and 3-5 keV band counts
#data reduction
x_err = x_err_counts*0.18657702     #units are keV cm^-2 s^-1
x_flux = x_counts*0.18657702    #convert to flux. x_counts is a numpy array so this will work
x_err_frac = [x_err[i]/x_flux[i] for i in range(len(x_flux))]   #fractional error calculation

x_mjd_for_cross_corr = [x_mjd[i] for  i in range(len(x_flux)) if x_flux[i] > 0.0 and x_err_frac[i] < limit]
x_flux_for_cross_corr = [np.log10(x_flux[i]) for i in range(len(x_flux)) if x_flux[i] > 0.0 and x_err_frac[i] < limit]    #want a flux larger than 0.5 and a fractional error lower than 0.5
x_error = [np.log10(x_err[i]) for i in range(len(x_flux)) if x_flux[i] > 0.0 and x_err_frac[i] < limit]
r_mjd_cross = [r_mjd[i] for i in range(len(r_flux)) if r_flux[i] > 0.0] #remove negative fluxes
r_flux_cross = [np.log10(r_flux[i]) for i in range(len(r_flux)) if r_flux[i] > 0.0]

#split between hard and soft states
hard_start, hard_stop = np.loadtxt("../hard_intermediate_dates.txt", unpack = True)
x_mjd_hard = []
x_flux_hard = []
x_mjd_soft = []
x_flux_soft = []
error_hard = []
error_soft = []
counter = 0
for i in range(len(hard_stop)):
    for j in range(len(x_mjd_for_cross_corr)):
        if hard_start[i] <= x_mjd_for_cross_corr[j] <= hard_stop[i]:
            x_mjd_hard.append(x_mjd_for_cross_corr[j])
            x_flux_hard.append(x_flux_for_cross_corr[j])
            error_hard.append(x_error[j])
        elif 0 < x_mjd_for_cross_corr[j] < hard_start[i] and counter == 0:
            x_mjd_soft.append(x_mjd_for_cross_corr[j])
            x_flux_soft.append(x_flux_for_cross_corr[j])
            error_soft.append(x_error[j])
            counter += 1
        else:
            try:
                hard_start[i+1]
                if hard_stop[i] < x_mjd_for_cross_corr[j] < hard_start[i+1]:
                    x_mjd_soft.append(x_mjd_for_cross_corr[j])
                    x_flux_soft.append(x_flux_for_cross_corr[j])
                    error_soft.append(x_error[j])
            except IndexError:
                if x_mjd_for_cross_corr[j] > hard_stop[i]:
                    x_mjd_soft.append(x_mjd_for_cross_corr[j])
                    x_flux_soft.append(x_flux_for_cross_corr[j])
                    error_soft.append(x_error[j])
            continue

#turn all MJD's to integers
x_mjd_hard = np.array(x_mjd_hard).astype(int)
x_flux_hard = np.array(x_flux_hard)
x_mjd_soft = np.array(x_mjd_soft).astype(int)
x_flux_soft = np.array(x_flux_soft)

r_mjd_cross = np.array(r_mjd_cross).astype(int)
r_flux_cross = np.array(r_flux_cross)

#pair and append

#pair and append
flux_hard_R = []
flux_hard_X = []
flux_soft_X = []
flux_soft_R = []
err_hard_X = []
err_soft_X = []
for i in range(len(r_mjd_cross)):             #span of radio data is longer so i will use radio data
    val = r_mjd_cross[i]
    if val in x_mjd_hard:
        index = np.int(np.argwhere(x_mjd_hard==val))
        flux_hard_R.append(r_flux_cross[i])
        flux_hard_X.append(x_flux_hard[index])
        err_hard_X.append(error_hard[index])
    elif val in x_mjd_soft:
        index = np.int(np.argwhere(x_mjd_soft==val))
        flux_soft_R.append(r_flux_cross[i])
        flux_soft_X.append(x_flux_soft[index])
        err_soft_X.append(error_soft[index])

#plotting
fig = plt.figure(figsize=(15,30))
plt.rc('font', size=18)
plot = fig.add_subplot(111)
plot.errorbar(flux_hard_X, flux_hard_R, fmt = 'ro', label = 'Hard state')
plot.errorbar(flux_soft_X, flux_soft_R,  fmt = 'bo', label = 'Soft state')
plt.title("Zero Lag flux in hard and soft state for MAXI [10-20 keV] vs 15-GHz")
plt.ylabel(r"logarithmic 15 GHz flux $[keV\ cm^{-2}\ s^{-1}]$")
plt.ylim(ymin = -4.5)
plt.xlabel(r"logarithmic X-ray Flux $[keV\ cm^{-2}\ s^{-1}]$")
plt.xlim(xmin = -2)
plt.legend()
fig.savefig(title+".png")
#fig.show()
