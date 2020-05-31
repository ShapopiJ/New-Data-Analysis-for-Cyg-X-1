# New-Data-Analysis-for-Cyg-X-1

## CODES

* cc.py - Class for the cross correlation. Contains 3 functions.
    - read() reading in the data
    - split() hard/intermediate and soft state spliting of days.
    - correlate() do correlation after initial cleaning.

* combine.py - Function for the comibantion of data sets seperated by year.
* daily_average.py - Function for calculation of average flux in 1 day bins.
    - Also does error propagation.
* New_Correlation.py - Incomplete. Changing cc.py
* lc_plot.py - Plot lightcurve.
    - Argument 1 Data file
    - Argument 2 Title
* plotting.py - Plot correlation. 
    - Argument 1 Data file
    - Argument 2 Title
* zero_log_flux_plots.py - This plots the flux vs flux of two data sets at Zero lag.
    - Argument 1 Data file 1
    - Argument 2 Data file 2
    - Argument 3 Title