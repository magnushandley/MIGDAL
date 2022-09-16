import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from scipy import interpolate
from ITOstripcore import *

driftvel = 13
#we aren't using the main data array in the ITO class here, so set the 'eventstoconsider' variable to 1, so we don't generate an unnesesarily large array for no reason
#filepath = "/Users/magnus/Documents/MIGDAL/datawithito/3D/MIG_Fe55_data_220803T152221.CAL/daq.txt"
filepath = "/Users/magnus/Documents/MIGDAL/Ar_0634/MIG_full_readout_Fe55_Ar_CF4_220805T150634.CAL/daq.txt"

eventstoconsider = 500

strips = ITO(filepath,1000,eventstoconsider)

#data = strips.readevent(296)
#peaks = strips.peaktime(296)

#eventdata = data[3054]
#integrals = []
#sparkcount = 0
#for l in range(eventstoconsider):
#    eventdata = strips.readnextevent()
#
##    if (j%10 == 0):
##        print(j)
#    rowintegrals = np.zeros(60)
#    for i in range(60):
#        rowdata = eventdata[i][1]
#        offsetmean = np.mean(rowdata[:200])
#        std = np.std(rowdata[:200])
#        rowdata = np.subtract(rowdata, offsetmean)
#        max = np.amax(rowdata)
#        maxindex = int(np.where(rowdata == max)[0][0])
#
#        #finds the points at which the signal drops below
#        startfound = False
#        j = maxindex
#        while ((startfound == False) and (j >= 0)):
#            if rowdata[j] <= 0:
#                startpoint = j
#                startfound = True
#            else:
#                j -= 1
#
#        endfound = False
#        k = maxindex
#        while ((endfound == False) and (k<1000)):
#            if rowdata[k] <= 0:
#                endpoint = k
#                endfound = True
#            else:
#                k += 1
#
#        if (max > 5*std):
#            integral = np.sum(rowdata[startpoint:endpoint])
#            rowintegrals[i] = integral
#        else:
#            rowintegrals[i] = 0
#    integral = np.sum(rowintegrals)
#    integrals.append(np.sum(rowintegrals))
#    if (integral < 100):
#        print(str(l)+','+str(integral))
        
#print(integrals)
#print("Spark count: "+str(sparkcount))
#print("Spark rate: "+str(sparkcount/eventstoconsider)+" per event")

#plt.plot(summedtrace)
#plt.hist(integrals,100)
#plt.xlabel("Energy [au]")
#plt.ylabel("Events")
strips.readevent(494)
#strips.displaygivenevent(eventdata)
strips.displayfullevent(494)
eventdata = strips.data[494]
np.save("long.npy",eventdata)
#x = np.arange(start = 13,stop = 60)
#y = peaks[13:]
#plt.plot(x,y*driftvel)
#plt.xlim(0,60)
#plt.xlabel("Strip Number")
#plt.ylabel("Extracted height in z [cm]")
#plt.plot(eventdata[0][0][:-5],summedtrace[:-5],label = "Summed ITO")
#plt.plot(eventdata[0][0][:-5],data[3054][60][1][:-5],label = "PMT pulse")
#plt.xlabel("Time [$\mu$s]")
#plt.ylabel("Voltage [V]")
#plt.legend()
plt.show()

