import cv2
import numpy as np;

def markdetect(im):
	boundaries = [
	([0,250,40], [10, 255, 50])]
	# marker is 48,255,0
	#BGR vs RGB
	# loop over the boundaries
	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")
		mask = cv2.inRange(im, lower, upper)
		# cv2.namedWindow('markermask', cv2.WINDOW_NORMAL)
		# cv2.imshow("markermask", mask)
		#mask = cv2.inRange(image, np.array([17.,15.,100.]), np.array([50.,56.,200.]))
		detector1 = cv2.SimpleBlobDetector_create()
		keypoints1 = detector1.detect(im)
		count1 = 0
		for i in keypoints1:
			x1 = keypoints1[count1].pt[0] #i is the index of the blob you want to get the position
			y1 = keypoints1[count1].pt[1]
			count1 += 1
			return (x1,y1)
