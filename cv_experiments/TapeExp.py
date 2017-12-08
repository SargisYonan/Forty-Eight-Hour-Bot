# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 20:37:58 2017

@author: AutonomousSystemsLab
"""


import cv2

#%% Bring in a random test targe image:
import random
import os
from matplotlib import pyplot as plt

def getRandTape(downsample = None):
    allfiles = os.listdir("tape/")
    to_load = "tape/" + random.choice(allfiles)
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