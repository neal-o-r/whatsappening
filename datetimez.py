##########################################################################
##########################################################################

def time2float(x):
	"""converts datetime to float, so that interpolation/smoothing can be performed"""
	if (type(x) == numpy.ndarray) or (type(x) == list):
		emptyarray = []
		for i in x:
			z = (i - datetime.datetime(1970, 1, 1, 0)).total_seconds()
			emptyarray.append(z)
		emptyarray = array([emptyarray])
		return emptyarray[0]
	else:
		return (x - datetime.datetime(1970, 1, 1, 0)).total_seconds()

##########################################################################
##########################################################################

def float2time(x):
	"""converts array back to datetime so that it can be plotted with time on the axis"""
	if (type(x) == numpy.ndarray) or (type(x) == list):
		emptyarray = []
		for i in x:
			z = datetime.datetime.utcfromtimestamp(i)
			emptyarray.append(z)
		emptyarray = array([emptyarray])
		return emptyarray[0]
	else:
		return datetime.datetime.utcfromtimestamp(x)

##########################################################################
##########################################################################s
