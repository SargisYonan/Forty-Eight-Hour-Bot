import cv2
from matplotlib import pyplot as plt
import numpy as np
import glob
import camera_service
import framework

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

def checkForTargetByBlob(threshed_in, img_scale):
	#set up a blob detector:
	# Setup SimpleBlobDetector parameters.
	params = cv2.SimpleBlobDetector_Params()
	# Change thresholds
	params.minThreshold = 1
	params.maxThreshold = 1000
	# Filter by Area.
	params.filterByArea =True
	params.minArea = 3000
	params.maxArea = 9000
	# Filter by Circularity
	params.filterByCircularity = True
	params.minCircularity = 0.3
	# Filter by Convexity
	params.filterByConvexity = True
	params.minConvexity = .5
		# Filter by Inertia
	params.filterByInertia = False
	params.minInertiaRatio = 0.75
	
	detector = cv2.SimpleBlobDetector_create(params)
	keypts = detector.detect(threshed_in)
	return keypts

def find_hole(gray_img):
	rawimg = cv2.imread(fname, 0) # 0 argument opens as gray
	img = cv2.resize(rawimg, (0,0), fx=img_scale, fy=img_scale) 

	threshed = bottomSliceThresholder(img)
	keypts = checkForTargetByBlob(threshed, img_scale)
	if len(keypts) > 0:
		keypt = keypts[0] # we're grabbing the first hole found
		theta = np.concatenate((np.linspace(0, 2*np.pi, 100), [0]))
		x,y = keypt.pt
		r = keypt.size

		plt.plot(x + r*np.cos(theta), y+r*np.sin(theta), 'r')
		plt.plot(x, y)
		plt.imshow(threshed, cmap = 'gray', interpolation = 'bicubic')
		plt.show()
		return (x, y, r)
	else:
		return (-1, -1, -1)

camera_snapper = camera_service.cameraService()
img_scale = 0.5

def init():
    return

hole_epsilon = 50
hole_close_threshold = 200

def hole_event_checker():
	img, retval = camera_snapper.snap()
	if retval:
		gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img = cv2.resize(gray_image, (0,0), fx=img_scale, fy=img_scale) 
		x,y,r = find_hole(img)

		if x >= 0 and y >= 0 and r >= 0:
			row, col, ch = img.shape
			pos_dif = x - int(math.floor(cols/2))

			if (math.abs(pos_dif) > hole_epsilon):
				if (pos_dif > 0):
					post_event = framework.Event('HOLE_RIGHT', params)
					framework.framework_post_event(post_event)
				elif (pos_dif < 0):
					post_event = framework.Event('HOLE_LEFT', params)
					framework.framework_post_event(post_event)
			else:
				if (r > hole_close_threshold):
					post_event = framework.Event('HOLE_CLOSE', params)
					framework.framework_post_event(post_event)
				else:
					post_event = framework.Event('HOLE_CENTER', params)
					framework.framework_post_event(post_event)
		else:
			return False
	else:
		return False

'''
threshed = bottomSliceThresholder(img)
keypts = checkForTargetByBlob(threshed, img_scale)

for keypt in keypts:
	theta = np.concatenate((np.linspace(0, 2*np.pi, 100), [0]))
	x,y = keypt.pt
	r = keypt.size
	print(x,y,r)
	plt.plot(x + r*np.cos(theta), y+r*np.sin(theta), 'r')
	plt.plot(x, y)
	plt.imshow(threshed, cmap = 'gray', interpolation = 'bicubic')
	
	#plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
	plt.show()
'''









