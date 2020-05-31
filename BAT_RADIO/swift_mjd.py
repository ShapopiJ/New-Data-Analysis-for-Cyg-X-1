def mjd_swift(tsec):

	mjd0=53414.00704410
	tsec0=129946208.0
	tday=3600*24.0
	mjd_swift=mjd0+(tsec-tsec0)/tday
	return mjd_swift
