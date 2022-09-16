"""
This is a crude way to search a directory for image pairs that have a rolling shutter cutting an event that spans the two.
Functions:

stitch:
Does what it says on the tin, stitches two images cut at row "cut"

capturecut
Returns the filenames of consecutive images which need stitching together, followed by the line number of the expected cut
"""

import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from PIL import Image

dir = "/Users/magnus/Documents/MIGDAL/MIGDAL_day_1/2022-07-25-Chamber_test/630V_580V_200ms/quietdarkremoved/"
outputdir = "/Users/magnus/Documents/MIGDAL/MIGDAL_day_1/2022-07-25-Chamber_test/630V_580V_200ms/qdrstitched/"
#pathname1 = "/Users/magnus/Documents/MIGDAL/MIGDAL_day_1/2022-07-25-Chamber_test/630V_580V_200ms/quietdarkremoved/quiet630_580_200_62nodark.tif"
#pathname2 = "/Users/magnus/Documents/MIGDAL/MIGDAL_day_1/2022-07-25-Chamber_test/630V_580V_200ms/quietdarkremoved/quiet630_580_200_63nodark.tif"

resolution = 1152
avglen = 8
threshold = 40

def stitch(topstring, bottomstring, cut,outputstring):
    """
    stiches two images cut by the rolling shutter at 'cut'
    """
    topimage = Image.open(topstring)
    bottomimage = Image.open(bottomstring)


    top = np.asarray(topimage)
    bottom = np.asarray(bottomimage)

    out = np.zeros((np.shape(top)[0],np.shape(top)[1]))

    out[0:len(top)][0:cut] = top[0:len(top)][0:cut]
    out[0:len(top)][cut:len(top)] = bottom[0:len(top)][cut:len(top)]

    output = Image.fromarray(out)
    output.save(outputstring, format="TIFF")

def capturecut(directory, resolution, avglen, threshold,outputdir):
    """
    Returns the filenames of consecutive images which need stitching together, followed by the line number of the expected cut
    Inputs
    ---------
    directory: string
        location of the image files
        
    Outputs (printed, consectutively)
    ---------
    cut: int
        the integer number of pixels to the row below the discontinuity
    pathname1: string
    pathname2: string
        
    Returns cuts, a list of of file numbers affected by the cut
    """
    stitchnum = 1
    def groupedAvg(myArray, N):
        result = np.cumsum(myArray)[N-1::N]/float(N)
        result[1:] = result[1:] - result[:-1]
        return result

    def maxgrad(pathname,resolution,avglen,threshold):
        
        img = io.imread(pathname)
        img[img < threshold] = 0

        newimg = np.zeros((resolution, int(resolution/avglen)))

        for i in range(resolution):
            row = img[i,:]
            rowavg = groupedAvg(row, avglen)
            newimg[i] = rowavg
        
        grady = np.diff(newimg, axis = 0)
        absgrady = np.absolute(grady)
        
        coords = np.where(absgrady == np.max(absgrady))
        sign = np.sign(grady[int(coords[0][0])][int(coords[1][0])])
        
        return int(coords[0][0]), int(coords[1][0]), sign

    files = sorted(glob.glob(dir+'*.tif'), key=os.path.getmtime)
    cuts = []

    for i in range(len(files)-1):
        print(i)
        pathname1 = files[i]
        pathname2 = files[i+1]
    
#        try:
        y1, x1, sign1 = maxgrad(pathname1,resolution,avglen,threshold)
        y2, x2, sign2 = maxgrad(pathname2,resolution,avglen,threshold)
        
        if (abs((y1 - sign1) - y2) <= 1) and ((x1 - x2) <= 2):
            if (y1==y2):
                cutpoint = y1 + 1
            elif (abs(y1-y2)==1):
                cutpoint = y1
            else:
                print("no scenario")
                cutpoint = y1
            #stitch(pathname2,pathname1,cutpoint,outputdir+str(i+1)+'_'+str(i+2)+'.tif')
            stitchnum += 1
            print(cutpoint,' ',pathname1,' ',pathname2)
            cuts.append(i+1)
            cuts.append(i+2)
    
    print(cuts)

capturecut(dir, resolution, avglen, threshold,outputdir)



