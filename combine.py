#function to combine Adnrzej's radio data with the new data.
import numpy as np

def combine(data1, data2, output): # data1 is mine and 2 is Andrzej's
    mjd1, flux1, error1 = np.loadtxt(data1, unpack=True, usecols=(0, 1, 4))
    mjd2, flux2, error2 = np.loadtxt(data2, unpack=True, usecols=(0, 1, 2))

    mjd = mjd2.append(mjd1)
    flux = flux2.append(flux1)
    error = error2.append(error1)

    np.savetxt(output, np.c_[mjd, flux, error],
    fmt='%.4f, %e, %e')
    
