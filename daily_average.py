#Make daily averages from raw data.

def average(file, output):
    import numpy as np
    hourly_mjd, hourly_flux, hourly_error = np.loadtxt(file, unpack= True, skiprows=7)

    for_offset = open(file, 'r')
    counter = 0
    for line in for_offset:
        if counter > 0: break
        offset = int(line.split('-')[1])
        counter += 1
        #print(offset)


    daily_mjd = []
    daily_flux = []
    daily_error = []
    points = []
    systamatic_error = []
    total_error = []
    for i in range(int(min(hourly_mjd)), int(max(hourly_mjd)) ):
        sum_flux = 0
        n = 0
        error_flux = 0
        day = i
        average_day = 0
        for index in range(len(hourly_mjd)):
            if int(hourly_mjd[index]) == day:
                sum_flux += hourly_flux[index]
                n += 1
                error_flux += hourly_error[index]**2
                average_day += hourly_mjd[index]

        if sum_flux > 0:
            daily_mjd.append((average_day/float(n)) + offset)
            daily_flux.append(sum_flux/float(n))
            daily_error.append((1./n) * np.sqrt(error_flux))
            points.append(n)
            systamatic_error.append((sum_flux/float(n)) * (5/100))
            total_error.append(np.sqrt(error_flux + ((sum_flux/n) * (5/100))**2))


    np.savetxt(output,
    np.c_[daily_mjd, daily_flux, daily_error, systamatic_error, total_error,points],
    header='Daily averaged data\nMJD\tFlux[Jy]\tError[Jy]\tSysError\tTotal Error\t# of points',
    fmt = '%.4f %e %e %e %e %d',
    delimiter='\t')
