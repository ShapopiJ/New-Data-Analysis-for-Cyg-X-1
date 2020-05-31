#general plotting algorithm
import argparse
import matplotlib.pyplot as plt
import numpy as np

Input = argparse.ArgumentParser(description = "Please pass all these arguments in sequence:")
Input.add_argument('data_file', type = str,  nargs = 1, help = 'Data_file')
Input.add_argument('Title', type = str, nargs = 1, help = 'title of plot')
args = Input.parse_args()

data_file = args.data_file[0]
title = args.Title[0]


lag, r, dev = np.loadtxt(data_file, unpack = True, usecols = (0,1,2))
fig = plt.figure(figsize=(25,8))
plt.rc('font', size=20)
cross = fig.add_subplot(111)
cross.plot(lag, r, 'b-', label = 'cross x_ray '+title+' vs 15-GHz')
cross.plot(lag, (r+dev), 'c--', label = 'error')        #upper limit
cross.plot(lag, (r-dev), 'c--')       #lower limit
#plt.title("Cross Correlation X_Ray "+ title +" vs. Radio 15GHz ")
plt.xlabel(r'$\Delta$ T [d]')
plt.ylabel('r')
#plt.xlim(-100,100)
cross.grid(ls = '--', which = 'major')
#cross.legend()
#plt.show()

#Get max and plot is with the value displayed.
max_index = np.where(r == max(r))[0][0]
max_r = r[max_index]
max_lag = lag[max_index]
#plt.errorbar(max_lag, max_r, dev[max_index] , fmt='+', barsabove=True, ecolor='red', label = 'Highest point of Correlation')
#plt.text(max_lag+5, max_r, 'MAX')
#plt.legend()
fig.savefig(str(data_file.split('.')[0])+".png")
