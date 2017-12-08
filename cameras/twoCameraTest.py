#a simple test to see if we can take pictures with the webcam:

import cv2
import time

cameras = [False,False]

def openCamera(camera):
	id = camera.get(

while True:
		for i in [-1,-2]:
			cameras[i] = cv2.VideoCapture(i)
			print("camera",i,"is opened:", cameras[i].isOpened())
		if all( [camera.isOpened() for camera in cameras]):
				break

firstTime = time.clock()
lastTime = time.clock()
i = 0
breakme = 100

while i<3:
	if lastTime + 5< time.clock():
			break

	if lastTime + .1 < time.clock():
		continue
	lastTime = time.clock()

	for j,camera in enumerate(cameras):
		retval, img = camera.read()
		print("camera has image ready:",retval)
	
		if retval:
			cv2.imwrite("test_"+str(j)+str(i)+".png", img)
			if i == 1:
				i = i +1

 
for camera in cameras:
	del(camera)

