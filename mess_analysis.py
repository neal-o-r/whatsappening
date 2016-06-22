import datetime
from time import strptime
import numpy as np
import matplotlib.pyplot as plt

##########################################################################
##########################################################################

def time2float(x):
	"""converts datetime to float, so that interpolation/smoothing can be performed"""
	if (type(x) == np.ndarray) or (type(x) == list):
		emptyarray = []
		for i in x:
			z = (i - datetime.datetime(1970, 1, 1, 0)).total_seconds()
			emptyarray.append(z)
		emptyarray = np.array([emptyarray])
		return emptyarray[0]
	else:
		return (x - datetime.datetime(1970, 1, 1, 0)).total_seconds()

##########################################################################
##########################################################################

def float2time(x):
	"""converts array back to datetime so that it can be plotted with time on the axis"""
	if (type(x) == np.ndarray) or (type(x) == list):
		emptyarray = []
		for i in x:
			z = datetime.datetime.utcfromtimestamp(i)
			emptyarray.append(z)
		emptyarray = np.array([emptyarray])
		return emptyarray[0]
	else:
		return datetime.datetime.utcfromtimestamp(x)

##########################################################################
##########################################################################s



f = open("a_mess.txt", 'r')
block = f.readlines()
f.close()

sender      = []
recipient   = []
message     = []
date        = []
full_string = ''

for i in range(0,len(block),5):

    date.append(block[i])
    sender.append(block[i+1])
    recipient.append(block[i+2])
    message.append(block[i+3])

    full_string = full_string + block[i+3]


datetiming = []
link = 0
for i in range(len(date)):
    
    time = date[i].split("-")[0].split(",")[1]
    
    datetiming.append(datetime.datetime(*strptime(time, " %d %b %Y %H:%M:%S ")[0:6]))

    if "http" in message[i]:
        link += 1

float_time = time2float(datetiming)

binsize = 60*60*24*7
plt.hist(float_time - float_time[0], bins=binsize)




plt.show()
