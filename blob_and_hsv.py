import cv2
import numpy as np
import argparse

def read_image_file():
	#Gets the image path information as a terminal argument. "python blob.py --image [image path]"
	ap=argparse.ArgumentParser()
	ap.add_argument("-i", "--image", help="path to the image")
	args = vars(ap.parse_args())
	image = cv2.imread(args["image"])
	return image

def hsv_finding():
	image=read_image_file()
	hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
	boundaries = [([0,50,50], [10, 255, 255])] #A thing to fiddle with in order to capture all the reds

	for (lower, upper) in boundaries:
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")
	 
		mask = cv2.inRange(hsv, lower, upper)
		output = cv2.bitwise_and(image, image, mask = mask)

		return output

def blob():
	im = hsv_finding()

	# Set up the detector with default parameters.
	params = cv2.SimpleBlobDetector_Params()

	params.filterByArea = True
	params.minArea = 22
	params.maxArea = 25
	params.maxThreshold = 150
	params.minThreshold = 1
	params.filterByInertia = True
	params.minInertiaRatio = 0.0000001


	detector = cv2.SimpleBlobDetector_create(params)
	 
	# Detect blobs.
	keypoints = detector.detect(im)
	count = 0
	positions = {}
	for i in keypoints:
		x = keypoints[count].pt[0] #i is the index of the blob you want to get the position
		y = keypoints[count].pt[1]
		positions[y]=x
		count+=1

	print positions
 
	# Draw detected blobs as red circles.
	# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
	im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	 
	# Show keypoints
	cv2.imshow("Keypoints", im_with_keypoints)
	cv2.waitKey(0)

if __name__ == "__main__":
	blob()