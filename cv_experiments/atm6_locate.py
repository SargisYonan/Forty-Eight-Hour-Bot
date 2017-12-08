import cv2
from matplotlib import pyplot as plt
import numpy as np
import glob

# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 15:48:05 2017

@author: AutonomousSystemsLab
"""

def bottomSliceThresholder(grayimg_in):
    slicept = int( grayimg_in.shape[0]*.9 )
    bottom_slice = grayimg_in[slicept:,:]
    hist,bins = np.histogram(bottom_slice,256,[0,256]) 
    maxthresh = np.argmax(hist)
    minthresh = int(maxthresh*.75)  #parameter to tune
    thresh = minthresh + np.argmin(hist[minthresh:maxthresh])
    threshedimg_out = cv2.threshold(grayimg_in,thresh,255,cv2.THRESH_BINARY)[1]
    return threshedimg_out

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


filenames = glob.glob('targets/*.jpg')


for fname in filenames:
    img = cv2.imread(fname, 0) # 0 argument opens as gray
    threshed = bottomSliceThresholder(img)
    keypts = checkForTargetByBlob(threshed)
    
    for keypt in keypts:
        theta = np.concatenate((np.linspace(0, 2*np.pi, 100), [0]))
        x,y = keypt.pt
        r = keypt.size
        print(x,y,r)
        plt.plot(x + r*np.cos(theta), y+r*np.sin(theta), 'r')























