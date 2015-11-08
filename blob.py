# Standard imports
import cv2
import numpy as np;
import struct
import imghdr
import math

def read_image_file():
	#Gets the image path information as a terminal argument. "python blob.py --image [image path]"
	ap=argparse.ArgumentParser()
	ap.add_argument("-i", "--image", help="path to the image")
	args = vars(ap.parse_args())
	image = cv2.imread(args["image"])

	# Draw detected blobs as red circles.
	# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
	im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
	# Show keypoints
	cv2.imshow("Keypoints", im_with_keypoints)
	cv2.waitKey(0)

	return image

def detect_blobs(image):
# Set up the detector with default parameters.
	params = cv2.SimpleBlobDetector_Params()

	params.filterByArea = True
	params.minArea = 20.5
	params.maxArea = 23
	params.maxThreshold = 150
	params.minThreshold = 1
	params.filterByInertia = True
	params.minInertiaRatio = 0.0000001
	detector = cv2.SimpleBlobDetector_create(params)
 
	# Detect blobs.
	keypoints = detector.detect(im)
	cartesianCoordinates=[]
	for i in keypoints:
		x = keypoints[count].pt[0] #i is the index of the blob you want to get the position
		y = keypoints[count].pt[1]
		coordinates.append((x,y))
	return cartesianCoordinates

def changeOrigin(coordinates):
	height, width = im.shape[:2]
	center = [height/2, width/2]
	REcoordinates=[]
	for i in coordinates:
		REcoordinates.append((center[0]-i[0], center[1]-i[1]))
	return REcoordinates

def returnPolarCoordinates(REcoordinates):
	
	angles=[]
	for i in REcoordinates:
		angles.append((math.atan2(i[1],i[0]))*57.2958)
	return angles

def main():
	image=read_image_file()
	coordinates = detect_blobs(image)
	newCoor= changeOrigin(coordinates)
	angles=returnPolarCoordinates(newCoor)
	print angles

if __name__ == '__main__':
	main()
