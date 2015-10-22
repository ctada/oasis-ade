# Standard imports
import cv2
import numpy as np;
 
# Read image
im = cv2.imread("4tube720x720.jpg")
 
# Set up the detector with default parameters.
params = cv2.SimpleBlobDetector_Params()

params.filterByArea = True
params.minArea = 20
params.maxThreshold = 150
params.minThreshold = 1
params.filterByInertia = True
params.minInertiaRatio = 0.0000001

print params.filterByCircularity, params.minCircularity


detector = cv2.SimpleBlobDetector_create(params)
 
# Detect blobs.
keypoints = detector.detect(im)
count = 0
for i in keypoints:
	x = keypoints[count].pt[0] #i is the index of the blob you want to get the position
	y = keypoints[count].pt[1]
	count+=1
	print x,y
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)