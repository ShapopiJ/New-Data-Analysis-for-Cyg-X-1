import numpy as np
"""
This is a class for correlating data from the Ryle/AMI and X-ray data
I will try to generalize it as much as possible
"""
"""
Structure from the back:

    1 In a pdf called r.pdf under texfiles folder, that is the expression that guides me
    The epression is for the r value of two light curves. One function for that would be nice.
    2 Then a function to split is good
    3 One more function for reading values is great.
"""

class Correlate():

    def __init__(self, l_range, limit, step, delta, name, split_value=False):
        self.l_range = l_range
        self.limit = limit
        self.step = step
        self.delta = delta
        self.name = name
        self.split_value = split_value
    def correlate(self, r_mjd, r_flux, x_mjd, x_flux):

        lags = np.arange(-self.l_range, self.l_range+self.delta, self.delta)    #this is the lag values
        ibin = np.zeros(2*int(self.l_range/self.delta) + 1)      #all K values for each bin or lag range
        xbin = np.zeros(2*int(self.l_range/self.delta) + 1)      #all I values for each bin or lag range
        ybin = np.zeros(2*int(self.l_range/self.delta) + 1)      #all J values for each bin or lag range
        r = np.zeros(2*int(self.l_range/self.delta) + 1)         #all r values for each bin or lag range
        x = np.zeros(2*int(self.l_range/self.delta) + 1)         #all x flux values for each pair in bin that will be incremented every time we find a pair
        x2 = np.zeros(2*int(self.l_range/self.delta) + 1)        #all x squared flux values for each pair in bin that will be incremented every time we find a pair
        y = np.zeros(2*int(self.l_range/self.delta) + 1)         #all y flux values for each pair in bin that will be incremented every time we find a pair
        y2 = np.zeros(2*int(self.l_range/self.delta) + 1)        #all y squared flux values for each pair in bin that will be incremented every time we find a pair
        sigma = np.zeros(2*int(self.l_range/self.delta) + 1)     #standard deviation calulations
        sigmax = np.zeros(2*int(self.l_range/self.delta) + 1)    # deviation can be calculated by sig = sqrt(<x**2> - <x>**2)
        sigmay = np.zeros(2*int(self.l_range/self.delta) + 1)
        max_lag = self.l_range/self.delta

        """
        #Loop 1: This loop runs over all possible pairs, finds their bin places in all arrays defined...
        above and increments by the respective amount
        The numerator of r can be written as <xy> + <x><y>
        """
        for m in range(len(x_mjd)):
            for n in range(len(r_mjd)):
                j = r_flux[n]
                i = x_flux[m]
                lg = r_mjd[n] - x_mjd[m]
                if abs(lg) <= (self.l_range + (self.delta/2.0)):
                    b = int(np.round(lg/self.delta) + max_lag)      #bin number/point/index
                    #print(lg)
                    ibin[b] += 1        #This list has K values in each bin
                    xbin[b] += 1        #This list has J' values for each bin
                    ybin[b] += 1        #This list has J' values for each bin
                    x[b] += i           #This list now contains the sum of x_fluxes falling in each bin
                    y[b] += j           #This list now contains the sum of y_fluxes falling in each bin
                    x2[b] += i*i        #This list now contains the sum of x**2_fluxes falling in each bin
                    y2[b] += j*j        #This list now contains the sum of y**2_fluxes falling in each bin
                    r[b] += i*j         #This list now contains the sum of x*j which is the numerator of the first term in the numerator calulation
        for i in range(len(xbin)):
            r[i] = r[i]/ibin[i]         #this now contains <xy>
            y[i] = y[i]/ybin[i]         #this now contains <y>
            x[i] = x[i]/xbin[i]         #this now contains <x>
            x2[i] = x2[i]/xbin[i]       #this now contains <x**2>
            y2[i] = y2[i]/ybin[i]       #this now contains <y**2>
            r[i] -=  x[i]*y[i]   #NOW r CONTAINS THE NUMERATOR OF THE EQUATION. NOW IT MUST BE NORMALIZED WITH THE SIGMAS OF x AND y
            sigmax[i] = np.sqrt(x2[i] - x[i]*x[i]) #standard deviations are now completed
            sigmay[i] = np.sqrt(y2[i] - y[i]*y[i])


        """
        Loop 2: In this loop I use the same conditions for the first loop but I have the ability to do
        more arithmetic on the values in each bin and begin sums for standard deviations
        """
        for m in range(len(x_mjd)):
            for n in range(len(r_mjd)):
                j = r_flux[n]
                i = x_flux[m]
                lg = r_mjd[n] - x_mjd[m]
                if abs(lg) <= (self.l_range + (self.delta/2.0)):
                    b = int(np.round(lg/self.delta) + max_lag)
                    sigma[b] += ((i - x[b])*(j - y[b]) - r[b])**2.0     #Numerator of equation 5 is complete
        """
        Loop 3: This loop is necessary because I can do not more in the preivious loop to get the standard deviation done
        Also I would like to write out everything now.
        """
        fi = open(self.name+".dat", "w")
        fi.write("#Lag\t r\t dev\t K\n")


        for i in range(len(sigma)):
            r[i] = r[i]/(sigmax[i] * sigmay[i])     #r is now complete
            sigma[i] = np.sqrt(sigma[i])/((ibin[i] - 1.0) * sigmax[i] * sigmay[i])     #sigma is complete
            fi.write("%.1f\t%f\t%f\t%i\n" %(lags[i], r[i], sigma[i], ibin[i]))
        fi.close()

    def split(self, x_mjd, x_flux, state):        #state is a string
        if self.split_value:
            r_mjd_hard = []
            r_flux_hard = []
            r_mjd_soft = []
            r_flux_soft = []
            x_mjd_hard = []
            x_flux_hard = []
            x_mjd_soft = []
            x_flux_soft = []
            counter = 0
            hard_start, hard_stop = np.loadtxt("hard_intermediate_dates.txt", unpack = True)
            for i in range(len(hard_stop)):
                for j in range(len(x_mjd)):
                    if hard_start[i] <= int(x_mjd[j]) <= hard_stop[i]:
                        x_mjd_hard.append(x_mjd[j])
                        x_flux_hard.append(x_flux[j])
                    elif 0 < int(x_mjd[j]) < hard_start[i] and counter == 0:
                        x_mjd_soft.append(x_mjd[j])
                        x_flux_soft.append(x_flux[j])
                        counter += 1
                    else:
                        try:
                            hard_start[i+1]
                            if hard_stop[i] < int(x_mjd[j]) < hard_start[i+1]:
                                x_mjd_soft.append(x_mjd[j])
                                x_flux_soft.append(x_flux[j])
                        except IndexError:
                            if int(x_mjd[j]) > hard_stop[i]:
                                x_mjd_soft.append(x_mjd[j])
                                x_flux_soft.append(x_flux[j])
                        continue
                """ This was to split r as well
                for j in range(len(r_mjd)):
                    if hard_start[i] <= int(r_mjd[j]) <= hard_stop[i]:
                        r_mjd_hard.append(r_mjd[j])
                        r_flux_hard.append(r_flux[j])
                    elif 0 < int(r_mjd[j]) < hard_start[i] and counter == 0:
                        r_mjd_soft.append(r_mjd[j])
                        r_flux_soft.append(r_flux[j])
                        counter += 1
                    else:
                        try:
                            hard_start[i+1]
                            if hard_stop[i] < int(r_mjd[j]) < hard_start[i+1]:
                                r_mjd_soft.append(r_mjd[j])
                                r_flux_soft.append(r_flux[j])
                        except IndexError:
                            if int(r_mjd[j]) > hard_stop[i]:
                                r_mjd_soft.append(r_mjd[j])
                                r_flux_soft.append(r_flux[j])
                        continue
                """
        if state.title() == 'Hard':
            x_mjd = x_mjd_hard
            x_flux = x_flux_hard
            #r_mjd = r_mjd_hard
            #r_flux = r_flux_hard
            return x_mjd,x_flux #r_mjd, r_flux
        elif state.title() == 'Soft':
            x_mjd = x_mjd_soft
            x_flux = x_flux_soft
            #r_mjd = r_mjd_soft
            #r_flux = r_flux_soft
            return x_mjd, x_flux #, r_mjd, r_flux

    def read(self, radio, x_ray, band=None, band_error=None):                 #feed in data files as strings
        if band == None:
            band = 1
            band_error = 2
        r_mjd, r_flux = np.loadtxt(radio, unpack = True, usecols = (0,1))      #radio data
        x_mjd, x_counts, x_err_counts = np.loadtxt(x_ray, unpack = True, usecols = (0,band , band_error))    #x-ray mjd and 3-5 keV band counts

        x_err = x_err_counts*0.18657702 #error on flux
        x_flux = x_counts*0.18657702    #convert to flux. x_counts is a numpy array so this will work
        x_err_frac = [x_err[i]/x_flux[i] for i in range(len(x_flux))]   #fractional error calculation
        x_mjd_for_cross_corr = [x_mjd[i] for i in range(len(x_flux)) if x_flux[i] > 0.5 and x_err_frac[i] < self.limit]  #No negative fluxes and no fluxes with error above limit
        x_flux_for_cross_corr = [np.log10(x_flux[i]) for i in range(len(x_flux)) if x_flux[i] > 0.5 and x_err_frac[i] < self.limit]    #want a flux larger than 0.5 and a fractional error lower than 0.5
        r_mjd_cross = [r_mjd[i] for i in range(len(r_flux)) if r_flux[i] > 0.0] #remove negative fluxes
        r_flux_cross = [np.log10(r_flux[i]) for i in range(len(r_flux)) if r_flux[i] > 0.0]
        print("radio = %i, X-ray = %i" %(len(r_mjd_cross), len(x_mjd_for_cross_corr)))
        return r_mjd_cross, r_flux_cross, x_mjd_for_cross_corr, x_flux_for_cross_corr

c = Correlate(200, 0.5, 1.0, 1.0, 'class_test', split_value=True)
rm,rf,xm,xf = c.read('cygx1_radio15_1day.dat', 'cygx1_asm_1day.dat')
xm , xf = c.split(xm, xf, 'soft')
c.correlate(rm, rf, xm, xf)
