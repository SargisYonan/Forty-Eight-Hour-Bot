# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 15:48:05 2017

@author: AutonomousSystemsLab
"""

import cv2

#%% Bring in a random test targe image:
import random
import os
from matplotlib import pyplot as plt

def getRandTarget(downsample = None):
    allfiles = os.listdir("targets/")
    to_load = "targets/" + random.choice(allfiles)
    print("reading",to_load,"...")
    im_out = cv2.imread(to_load,cv2.IMREAD_COLOR)
    
    if downsample:
        im_out = cv2.resize(im_out,None,
                            fx=downsample, fy=downsample,
                            interpolation = cv2.INTER_CUBIC)    
    
    return im_out

def testGetRandTarget():
    rawimg = getRandTarget(downsample = .5)
    cv2.imshow("image",rawimg)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    
#testGetRandTarget()

#%% does it work in matplotlib?
import numpy as np

def testImagePlotting():
    plt.figure()
    plt.imshow(rawimg)
    #plot on top of it:
    shape = rawimg.shape
    x = shape[1]/2  #interesting, so shape goes height, width...
    y = shape[0]/2
    
    theta = np.concatenate((np.linspace(0, 2*np.pi, 100), [0]))
    
    plt.plot(x + x*np.cos(theta), y+y*np.sin(theta), 'r')
    plt.show()

#testImagePlotting()

#%% cool what else can we do with it?  Let's try a basic histEq:

def plotHistogram(img):
     hist,bins = np.histogram(img.flatten(),256,[0,256]) 
     cdf = hist.cumsum()
     cdf_normalized = cdf * hist.max()/ cdf.max()
     plt.plot(cdf_normalized, color = 'b')
     plt.hist(img.flatten(),256,[0,256], color = 'r')

def histogramExplore():
    plt.figure()
    grayimg = cv2.cvtColor(rawimg,cv2.COLOR_RGB2GRAY)
    
    plt.subplot(321)
    plt.imshow(grayimg,cmap = "gray")
    plt.subplot(322)
    plotHistogram(grayimg)
    
    #try equalizing the histogram?
    eqimg = cv2.equalizeHist(grayimg)
    
    plt.subplot(323)
    plt.imshow(eqimg,cmap = "gray")
    plt.subplot(324)
    plotHistogram(eqimg)
    
    #hmm, basic equalization comes out spotty, but perhaps preps us for thresh?
    threshimg = eqimg > 127
    plt.subplot(325)
    plt.imshow(threshimg,cmap = "gray")
    plt.subplot(326)
    plotHistogram(threshimg)

histogramExplore()
    
    
# Yeah, that's no good.  Hmm, a big part of the issue here is that the background
# is quite unpredictable.  What to do what to do...

#%% Hmm, maybe use a threshold made from a small slice of the bottom image?
plt.figure()


def bottomSliceThresholder(grayimg_in):
    slicept = int( grayimg_in.shape[0]*.9 )
    bottom_slice = grayimg_in[slicept:,:]
    hist,bins = np.histogram(bottom_slice,256,[0,256]) 
    maxthresh = np.argmax(hist)
    minthresh = int(maxthresh*.75)  #parameter to tune
    thresh = minthresh + np.argmin(hist[minthresh:maxthresh])
    threshedimg_out = cv2.threshold(grayimg_in,thresh,255,cv2.THRESH_BINARY)[1]
    return threshedimg_out


def testBottomSliceThresholder():

    grayimg = cv2.cvtColor( getRandTarget(), cv2.COLOR_RGB2GRAY)
    slicept = int( grayimg.shape[0]*.9 )
    bottom_slice = grayimg[slicept:,:]
    
    plt.subplot(321)
    plt.imshow(grayimg,cmap = "gray")
    plt.subplot(322)
    plotHistogram(grayimg)
    
    #try equalizing the histogram?
    plt.subplot(323)
    plt.imshow(bottom_slice,cmap = "gray")
    plt.subplot(324)
    plotHistogram(bottom_slice)
    
    #ok, this might work -- the max in bottom_slice is almost certainly a good approx of white.  So,
#    hist,bins = np.histogram(bottom_slice,256,[0,256]) 
#    maxthresh = np.argmax(hist)
#    minthresh = int(maxthresh*.75)  #parameter to tune
#    thresh = minthresh + np.argmin(hist[minthresh:maxthresh])
#    print("thresh =",thresh)
#    plt.plot([thresh,thresh],[0, max(hist)], "magenta")
#    plt.plot([minthresh, maxthresh],[max(hist)/2, max(hist)/2], "magenta")
#    
    
    threshimg = bottomSliceThresholder(grayimg)
    plt.subplot(325)
    plt.imshow(threshimg,cmap = "gray")
    plt.subplot(326)
    plotHistogram(threshimg)

testBottomSliceThresholder()

#%% Now let's get some edges:

def getEdges(threshimg):
    edgeimg = cv2.Laplacian(threshimg, 0, 255)
    return edgeimg

def testGetEdges():
    plt.figure()
    grayimg = cv2.cvtColor(getRandTarget(downsample = 0.5),
                           cv2.COLOR_RGB2GRAY)
    threshed = bottomSliceThresholder(grayimg)
    
    #Canny
    plt.subplot(311)
    plt.imshow(threshed,cmap = "gray")
    
    plt.subplot(312)
    edgeimg = cv2.Canny(threshed, 0, 255)
    plt.imshow(edgeimg)
    
    plt.subplot(313)
    edgeimg2 = getEdges(threshed)
    plt.imshow(edgeimg2)

testGetEdges()

#wow, looking good!

#%% Ok, let's see if we can find the circle with some blob detection?



def checkForTargetByBlob(threshed_in):
    #set up a blob detector:
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()
    # Change thresholds
    params.minThreshold = 1
    params.maxThreshold = 200
    # Filter by Area.
    params.filterByArea =True
    params.minArea = 50
    params.maxArea = 2500
    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.2
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.87
        # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.75
    
    
    detector = cv2.SimpleBlobDetector_create(params)
    keypts = detector.detect(threshed_in)
    return keypts

def testCheckForTargetByBlob():
    grayimg = cv2.cvtColor(getRandTarget(downsample = 0.25),
                       cv2.COLOR_RGB2GRAY)
    threshed = bottomSliceThresholder(grayimg)
    plt.figure()
    plt.subplot(212)
    plt.imshow(grayimg)
    plt.subplot(211)
    plt.imshow(threshed)
    keypts = checkForTargetByBlob(threshed)
    
    for keypt in keypts:
        theta = np.concatenate((np.linspace(0, 2*np.pi, 100), [0]))
        x,y = keypt.pt
        r = keypt.size
        print(x,y,r)
        plt.plot(x + r*np.cos(theta), y+r*np.sin(theta), 'r')

testCheckForTargetByBlob()

#%% not terrible, but not super reliable...Maybe that kerneling thing?

def convolutionSearchExp():
    from scipy.signal import convolve2d
    
    grayimg = cv2.cvtColor(getRandTarget(downsample = 0.5),
                           cv2.COLOR_RGB2GRAY)
    threshed = bottomSliceThresholder(grayimg)
    edgeimg = getEdges(threshed)
    
    kernellist = []
    kernellist.append(np.array([[1, 1, 1, 1],
                            [1,-3,-3, 1],
                            [1,-3,-3, 1],
                            [1, 1, 1, 1]]))
    kernellist.append(np.array([[1, 1, 1],
                            [1,-5, 1],
                            [1,-5, 1],
                            [1, 1, 1]]))
    
    conv_size = 30
    for k,kernel in enumerate(kernellist):
        plt.figure()
        #downscale:
        scale = threshed.shape[0]/conv_size
        img = cv2.resize(threshed,None, fx = (1.0/scale), fy= (1.0/scale) ,
                                interpolation = cv2.INTER_CUBIC)
        img = (np.array(img, dtype = "int16")-127)
        conv = convolve2d(img,kernel)
        maxpt = np.where(conv == conv.max())
        
        #plot original image:
        plt.subplot(311)
        plt.imshow(img,cmap = "gray")
        
        #sneaky way to plot the location of the maximum of conv:
        xcoords = np.array([0,1,1,0,0])*kernel.shape[1] + maxpt[1]
        ycoords = np.array([0,0,1,1,0])*kernel.shape[0] + maxpt[0]
        plt.plot(xcoords, ycoords, color = "red")
        
        plt.subplot(312)
        plt.imshow(conv)
            
        plt.subplot(313)
        plt.imshow(grayimg,cmap = "gray")
        
        #sneaky way to plot the location of the maximum of conv:
        xcoords = np.array([0,1,1,0,0])*kernel.shape[1]*scale + maxpt[1]*scale
        ycoords = np.array([0,0,1,1,0])*kernel.shape[0]*scale + maxpt[0]*scale
        plt.plot(xcoords, ycoords, color = "red")    
        

    

#%% Ok, let's see if we can find an ellipse...
#the dumb thing to try is doing hough transform, maybe our ellipse will be circle-y enoung?

# openCV's hough function isn't very transparent, maybe we can reproduce it?


#grayimg = cv2.cvtColor(getRandTarget(downsample = 0.5),
#                       cv2.COLOR_RGB2GRAY)
#threshed = bottomSliceThresholder(grayimg)
#edgeimg = getEdges(threshed)
#
##okay, so we want to iterate over a range of possible radii and centers:
#radRange = range( 10,   int( max(edgeimg.shape)/2 ) )
#xRange = range( 0, edgeimg.shape[0])
#yRange = range( 0, edgeimg.shape[1])
#
##radRange = [50, 60]
##xRange = [100, 200]
##yRange = [150, 250]
#
#hough = edgeimg * 0
##now, we iterate:
#plt.figure()
#plt.subplot(311)
#plt.imshow(edgeimg)
#for x in xRange:
#    for y in yRange:
#        for rad in radRange:
#            print((x,y,rad))
#            #make a circle mask:
#            mask = edgeimg*0
#            cv2.circle(mask,(x,y),rad, 1)
#            
##            plt.subplot(312)
##            plt.imshow(mask)
#            
#            votes = sum(mask.flatten()*edgeimg.flatten())
#            hough[x,y] = votes
#
#plt.subplot(313)            
#plt.imshow(hough)            

#BLEH, that's not gonna work...

#%% Trying openCV's 
























