#a simple test to see if we can take pictures with the webcam:

import cv2
import time
import os

cameras = [False,False]


class Camera:
	def __init__(self, cam_id,name):
		self.cam_id = int(cam_id)
		self.name = name 

	def startVideo(self, timeout=10):
		"""attempt to open video capture"""
		startTime = time.clock()
		while True:	
			self.video_capture = cv2.VideoCapture(self.cam_id)
			if self.video_capture.isOpened():
				print("opened stream for camera"+str(self.cam_id))
				break
			else:
				if startTime + timeout > time.clock():
					raise(Exception("Could not initialize camera"+str(self.cam_id)))


class cameraService:
	""" a module that maintains the cameras (reboots them if junk fails)"""
	def __init__(self,retry = False):
		#check with os about available devices:
		self.avail_cameras = []
		for dev in os.listdir("/dev/"):
			if dev[0:5] == "video":
				self.avail_cameras.append(int(dev[5]))
		if not len(self.avail_cameras) == 2:
			raise(Exception(
			"Error! Less than two cameras detected:"+str(self.avail_cameras) ))
		print("found cameras", self.avail_cameras)
		self.cam_dict = {"front":None, "down":None}

		#now start up these cameras!	
		self.initCamera("front", retry)
		self.initCamera("down", retry)

	def initCamera(self, cam_name, retry = False):
		if cam_name == "front":
			cam_id = self.avail_cameras[0]
		if cam_name == "down":
			cam_id = self.avail_cameras[1]
		while True:
			cam	= Camera(cam_id, cam_name)
			try:
				cam.startVideo()
			except Exception as e:
				if retry:
					continue
				raise(e)
						
			self.cam_dict[cam_name] = cam 
			print("started video capture for camera",cam_name)

	def snap(self, camname):
		"""attempt a snapshot, enter "front" or "down" to indicate which camera you like"""
		cam = self.cam_dict[cam_name]

		"""attempt a snapshot, if we fail we'll restart the camera"""
		#first, are we open?
		if not cam.video_capture.isOpened():
			raise(Exception("can't snap unless camera is open!"))
		retval, img = cam.video_capture.read()
		if retval:
			#first, make sure that the image exists!
			if any( [dim == 0 for dim in img.shape] ):
				raise(Exception("snapped an empty image, you should restart the camera"))
			else:
				return img
		else:
			return False

if __name__=="__main__":
		cs = cameraService(retry = True)		
		img = cs.snap("front")
		if img:
			cv2.write("front_img.png")
			print("snapped a new front image, check it out!")
		else:
			print("failed to snap a front image :(")


#-------------------------- REFERENCE JUNK BELOW -------------------------------
quit()
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

