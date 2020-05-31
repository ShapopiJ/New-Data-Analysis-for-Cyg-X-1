#Correlate radio and BAT data

import numpy as np
#import sys
#sys.path.insert(1, 'home/jimmy/Dropbox/projects/lag_correlation')
#print(sys.path)

from combine import combine
radio_data = 'cygx1_radio15_1day_complete.dat'
combine('../radio15_2017_2018_1day.dat', '../cygx1_radio15_1day.ascii', radio_data)
combine('../radio15_2019_1day.dat', radio_data, radio_data)

from cc import Correlate
c = Correlate(200, 0.5, 1.0, 1.0, 'radio15_bat')
rm,rf,xm,xf = c.read(radio_data, 'cygx1_bat_1day.dat', is_bat=False)
c.correlate(rm, rf, xm, xf)