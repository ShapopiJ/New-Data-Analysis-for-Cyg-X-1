#function to combine Adnrzej's radio data with the new data.
import numpy as np

def combine(data1, data2, output): # data1 is mine and 2 is Andrzej's
    mjd1, flux1, error1, points1 = np.loadtxt(data1, unpack=True, usecols=(0, 1, 4, 5))
    mjd2, flux2, error2, points2 = np.loadtxt(data2, unpack=True, usecols=(0, 1, 2,3))

    mjd = np.append(mjd2, mjd1)
    flux = np.append(flux2, flux1)
    error = np.append(error2, error1)
    points = np.append(points2, points1)

    np.savetxt(output, np.c_[mjd, flux, error, points],
    fmt='%.4f %e %e %d',
    delimiter='\t')
    
