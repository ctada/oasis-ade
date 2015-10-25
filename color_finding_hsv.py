# import the necessary packages

import numpy as np
import argparse
import cv2
 
# load the image
image = cv2.imread('test.png')
hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV) #have to convert back for imshow
# define the list of boundaries

# crop_img = image[200:400, 100:300]

# cv2.namedWindow('cropped', cv2.WINDOW_NORMAL)
# cv2.imshow("cropped", crop_img)

boundaries = [
	([0,50,50], [10, 255, 255])#, red in BGR
	#([86, 31, 4], [220, 88, 50]),
	#([25, 146, 190], [62, 174, 250]),
	#([103, 86, 65], [145, 133, 128])
]

# loop over the boundaries
for (lower, upper) in boundaries:
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
 
	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(hsv, lower, upper)
	output = cv2.bitwise_and(image, image, mask = mask)
 
	# show the images
	cv2.namedWindow('images', cv2.WINDOW_NORMAL)
	cv2.imshow("images", np.hstack([image, output]))

	# displays the mask
	# cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
	# cv2.imshow("mask", mask)

	#find and draw contours
	im, contours, hierarchy = cv2.findContours(mask, 1, 2)
	cv2.drawContours(image,contours,-1,(128,255,40),5)
	cv2.namedWindow('contours', cv2.WINDOW_NORMAL)
	cv2.imshow('contours', image)


	#might be better to use blob detection

	cv2.waitKey(0)
	cv2.destroyAllWindows()

	# cv2.imwrite("images.png", np.hstack([image,output]))