#Correlate Maxi and Asm data

import argparse

Input = argparse.ArgumentParser(description = "Please pass all these arguments in sequence:")
Input.add_argument('band', type = str,  nargs = 1, help = 'Energy Band')
args = Input.parse_args()

band = list(str(args.band[0]))[0].lower()     #Turn it all into one letter in lower case
if band == 'a':
    flux_collumn = 3
    error_collumn = 4
elif band == 'b':
    flux_collumn = 5
    error_collumn = 6
elif band == 'c':
    flux_collumn = 7
    error_collumn = 8
else:           #For sum calculations
    flux_collumn = 1
    error_collumn = 2
    band = sum

from combine import combine
radio_data = 'cygx1_radio15_1day_complete.dat'
combine('../radio15_2017_2018_1day.dat', '../cygx1_radio15_1day.ascii', radio_data)
combine('../radio15_2019_1day.dat', radio_data, radio_data)

from cc import Correlate
c = Correlate(200, 0.5, 1.0, 1.0, 'radio15_maxi_' + band + 'band')
rm,rf,xm,xf = c.read(radio_data, 'cygx1_maxi_1day.dat',band=flux_collumn, band_error=error_collumn)
c.correlate(rm, rf, xm, xf)