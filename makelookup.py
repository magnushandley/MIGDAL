from ITOstripcore import *

daqfilepath = "/Users/magnus/Documents/MIGDAL/Ar_0634/MIG_full_readout_Fe55_Ar_CF4_220805T150634.CAL/daq.txt"

imgdir = "/Users/magnus/Documents/MIGDAL/Ar_0634/images/"
maxsamples = 1000
eventstoconsider = 9000

#Inititialise an instance of the ITO class

strips = ITO(daqfilepath,maxsamples,eventstoconsider)
strips.lookuptable(18.07,imgdir)
