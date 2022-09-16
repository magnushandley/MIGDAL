import numpy as np

def createlocus(curve, distance):
    """
    creates a locus of points within a certain range of a curve.

    Parameters
    ----------
    curve: int
        array containing the x and y coordinates of points along the curve
    distance: int
        number of pixels from the curve that the locus should include
        
    Returns
    ----------
    locus: int
        array containing the set of points contained within the specified distance of the curve
    """
    xmin = np.min(curve[0])
    xmax = np.max(curve[0])
    ymin = np.min(curve[1])
    ymax = np.max(curve[1])
    xrange = int(xmax - xmin)
    yrange = int(ymax - ymin)
    
    tcurve = np.transpose(curve)
    toffsetcurve = tcurve - np.array([xmin, ymin])
    locus = []
    
    for i in range(xrange+(distance*2)+1):
        for j in range(yrange+(distance*2)+1):
        #offset coordinate
            x = i - distance
            y = j - distance
            coord = np.array([x,y])
            
            #distances from coordinate to curve
            deltaset = np.subtract(toffsetcurve,coord)
            tdeltaoffset = np.transpose(deltaset)
            
            #squared offsets
            sqoffsets = tdeltaoffset[0]**2 + tdeltaoffset[1]**2
            
            if np.min(sqoffsets) <= distance**2:
#                print(str(x+xmin)+' '+str(y+ymin))
                locus = np.append(locus,[(x+xmin),(y+ymin)])
                
    print(len(locus))
    locus = np.reshape(locus, (int(len(locus)/2), 2))
    return(np.transpose(locus))
       
def sumnearby(x,y,img):
    #sums over the pixel intensities near a curve
    xint = [int(m) for m in x]
    yint = [int(n) for n in y]
    xint = np.array(xint)
    yint = np.array(yint)
    pxenergy = img[xint,yint]
    totalenergy = np.sum(pxenergy)
    return totalenergy

    
def segmentedbragg(x,y,avglength,stripwidth,redfactor,img):
    """
    Generates a bragg curve, through integration across strips perpendicular to the path, adapting the offset to avoid strips overlapping.
    Parameters
    ---------
    x: float
        array of floating point x coordinates of the curve to be integrated along
    y: float
        array of floating point x coordinates of the curve to be integrated along
    avglength: float
        the length along the line with which gradients are calculated, in pixels x 3
    stripwidth: float
        width of the strips that we average intensity over, in pixels
    redfactor: float
        redundancy factor, how much wider should we make the slit separation
        than the theoretical minimum separation distance.
    img: the actual data

    Returns
    ---------
    bragg: float
        array containing [0]: the points along the curve where the intensity has
        been evaluated, and [1]: the lateral integrated intensity at that point
    """
    def perpvector(x,y):
        perpendicular = np.array([1,-x/y])
        perpendicular *= (1/(x**2 + y**2))
    
    def connect(ends):
        d0, d1 = np.diff(ends, axis=0)[0]
        if np.abs(d0) > np.abs(d1):
            return np.c_[np.arange(ends[0, 0], ends[1,0] + np.sign(d0), np.sign(d0), dtype=np.int32),
                         np.arange(ends[0, 1] * np.abs(d0) + np.abs(d0)//2,
                                   ends[0, 1] * np.abs(d0) + np.abs(d0)//2 + (np.abs(d0)+1) * d1, d1, dtype=np.int32) // np.abs(d0)]
        else:
            return np.c_[np.arange(ends[0, 0] * np.abs(d1) + np.abs(d1)//2,
                                   ends[0, 0] * np.abs(d1) + np.abs(d1)//2 + (np.abs(d1)+1) * d0, d0, dtype=np.int32) // np.abs(d1),
                         np.arange(ends[0, 1], ends[1,1] + np.sign(d1), np.sign(d1), dtype=np.int32)]
                         
    curvelen = len(x)
    tangents = []
    separations = np.zeros(curvelen-avglength)
    integrals = []
    evalpositions = []
    for i in range(curvelen - avglength):
        deltax = x[i + avglength] - x[i]
        deltay = y[i + avglength] - y[i]
        grad = deltay/deltax
        tangent = (deltax, deltay)
        tangents.append(tangent)
        perpendicular = perpvector(tangent[0],tangent[1])
        
    position = 0
    while position < (curvelen-avglength):
        if (position == 0):
            
        
        if i>0:
            #addition formula for tan, assuming the difference between gradients is a small angle
            deltatheta = (grad - lastgrad)/(1+(grad*lastgrad))
            stripseparation = 0.5*stripwidth*deltatheta*redfactor*3
            separations[i] = stripseparation
            delthetas.append(deltatheta)
            
        lastgrad = grad
    
    
    print(separations)
    print(delthetas)
    
    
    
    return()
                
                
            
            
