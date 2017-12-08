#a simple test to see if we can take pictures with the webcam:

import cv2
import time
import os



class cameraService:
	""" a module that maintains the cameras (reboots them if junk fails)"""
	def __init__(self, timeout = 10):		
		self.init_camera(timeout = timeout)

	def init_camera(self, timeout = 10):

		#attempt to start a camera:
		break_time = time.time() + timeout
		while time.time() < break_time:
			self.camera = cv2.VideoCapture(-1) #-1 targets the last camera, whatever its id is
			if self.camera.isOpened():
				print("opened stream for camera")
				return
		raise(Exception("could not initialize camera, pehaps unplug and try again???"))

	def snap(self):
		#first, are we open?
		if not self.camera.isOpened():
			print("camera seems to have disconnected, reconnecting...")
			self.init_camera()
			return False
		
		#ok, so now we get an image:
		retval, img = self.camera.read()
		if retval:
			if img.shape[0] == 0 or img.shape[1]==0:
				print("snapped an empty image, you should restart the camera")
				return img, False
		return img, retval

if __name__=="__main__":
		cs = cameraService(timeout = 5)		
		img, retval = cs.snap()
		if retval:
			cv2.imwrite("front_img.png",img)
			print("snapped a new front image, check it out!")
		else:
			print("failed to snap a front image :(")

