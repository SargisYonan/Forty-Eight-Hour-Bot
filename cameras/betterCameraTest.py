#a simple test to see if we can take pictures with the webcam:

import cv2
import time

camera_port = 0
 
camera = cv2.VideoCapture(0)
print("camera is opened:", camera.isOpened())


lastTime = time.clock()
i = 0

while i<10:
        retval, img = camera.read()
        print("camera has image ready:",retval)
        if retval:
            cv2.imwrite("testimg_"+str(i)+".png", img)
            i = i+1
 
# You'll want to release the camera, otherwise you won't be able to create a new
# capture object until your script exits
del(camera)

