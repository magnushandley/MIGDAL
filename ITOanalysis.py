import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from PIL import Image
from PIL.TiffTags import TAGS
from scipy import interpolate
from ITOstripcore import *
from RFsingletiff import *

pathname = "/Users/magnus/Documents/MIGDAL/deconvolution/auger_0634_img0306.tif"
pathnameraw = "/Users/magnus/Documents/MIGDAL/deconvolution/auger_0634_img0306nodark.tif"

SIGMA = 2.5 #sigma for derivative determination ~> Related to track width
lthresh = 10 #tracks with a response lower than this are rejected (0 accepts all)
uthresh = 0 #tracks with a response higher than this are rejected (0 accepts all)
minlen = 12 #minimum track length accepted
linkthresh = 40 #maximum distance to be linked
logim = False

braggimg = io.imread(pathname)/20

#strip offset, in strips
offset = 3
#velocity in cm/mus
driftvel = 13

filepath = "/Users/magnus/Documents/MIGDAL/Ar_0634/MIG_full_readout_Fe55_Ar_CF4_220805T150634.CAL/daq.txt"
lookuppath = "/Users/magnus/Documents/MIGDAL/datawithito/3D/MIG_Fe55_data_220803T152221.CAL/eventstoimages2.csv"
event = 617

lookupfile = open(lookuppath, 'r')
lookupdata = np.loadtxt(lookupfile,delimiter = ",",skiprows=1)

def lookup(daq,ludata = lookupdata):
    return(ludata[daq-1][1])

#def plotvoxels(centers, sizes):
#    for i in range(len(sizes)):
        

x,y = returnlines(pathname,
    SIGMA,
    lthresh,
    uthresh,
    minlen,
    linkthresh,
    logim)

#taking every ::nth value
x = x[::5]
y = y[::5]

#deposition = np.log(RF.simplebragg(y,x,braggimg))

strips = ITO(filepath,1000,event+1)

print(len(x),len(y))
trackstrip = pixeltostrip(x,2)
for i in range(len(trackstrip)):
    if (int(trackstrip[i]) > 59.5):
        trackstrip[i] = trackstrip[i] - 60

deltaz = np.zeros(len(x))



data = strips.readevent(event)
peaks = strips.peaktime(event)

stripdep = strips.stripintegrals(event)
stripdepinterp = interpolate.interp1d(np.arange(60),stripdep)
deposition = stripdepinterp(trackstrip)

        
interpolatedpeaks = interpolate.interp1d(np.arange(60), peaks)

for i in range(len(trackstrip)):
    deltaz[i] = interpolatedpeaks(trackstrip[i])*driftvel
    
#print(deltaz)
#strips.displayfullevent(3054)
#plt.plot(np.add(peaks*500,500),np.add(np.arange(60),0.5))
fig = plt.figure()
ax = plt.axes(projection='3d')
scatter_plot = ax.scatter3D(x,y,deltaz,c=deposition,s=deposition*150,cmap='turbo')

output = np.zeros((4,len(x)))

output[0] = x
output[1] = y
output[2] = deltaz
output[3] = deposition
np.savetxt("3Dtrack.txt",output)

ax.set_xlabel("x [pix]")
ax.set_ylabel("y [pix]")
ax.set_zlabel("z [cm]")
ax.set_zlim(-0.8,-0.4)
#ax.set_xlim(220,320)
ax.set_ylim(540,600)
plt.colorbar(scatter_plot, label="Charge deposited to strip [Au]")
plt.show()

