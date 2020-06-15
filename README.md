# New-Data-Analysis-for-Cyg-X-1

## Publications from this work

1. [The Persistent Radio Jet Coupled to Hard X-Rays in the Soft State of Cyg X-1](https://ui.adsabs.harvard.edu/abs/2020ApJ...894L..18Z/abstract)
2. [Correlations and lags between X-ray and radio emission of Cyg X-1](https://arxiv.org/abs/2004.11786v2)

### CODES

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
