import cv2
import numpy as np;
import math

def imageRead(filename):
	#openCV reads the image
	im = cv2.imread(filename)
	return im

def detectBlobs(im):
	#Setting up parameters. 
	params = cv2.SimpleBlobDetector_Params()
	# params.filterByColor = 1
	# params.blobColor=0.99999999999999995
	params.filterByArea = True
	params.minArea = 19 #20
	params.maxArea = 28 #23
	params.maxThreshold = 150
	params.minThreshold = 100
	params.filterByInertia = True
	params.minInertiaRatio = 0.09
	params.maxInertiaRatio = 0.15
	detector = cv2.SimpleBlobDetector_create(params)
	# Detect blobs.
	keypoints = detector.detect(im)
	return keypoints

def getBlobCoordinates(keypoints):
	cartesianCoordinates=[]
	count=0
	for i in keypoints:
		x = keypoints[count].pt[0] #i is the index of the blob you want to get the position
		y = keypoints[count].pt[1]
		cartesianCoordinates.append((x,y))
		count+=1
	return cartesianCoordinates

def drawBlobs(im, keypoints):
	im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("Keypoints", im_with_keypoints)
	cv2.waitKey(0)

def convertToPolarCoordinates(im, cartesianCoordinates):
	height, width = im.shape[:2]
	center = [height/2, width/2]
	polarCoordinates=[]
	for i in cartesianCoordinates:
		polarCoordinates.append(math.degrees(math.atan2((center[1]-i[1]),(center[0]-i[0]))))

	return polarCoordinates

def blob(filename):
	im = imageRead(filename)
	keypoints = detectBlobs(im)
	coordinates= getBlobCoordinates(keypoints)
	return coordinates

def divideIntoRegions(startingAngle, numDivisions):
	angleAddition = 360/numDivisions
	divisions = {}

	for i in range(1,(numDivisions/2)+1):
		start = startingAngle + (angleAddition*(i-1)) 
		if start > 180:
			start = -180 + (start-180)
		end = startingAngle + (angleAddition*i)
		if end > 180:
			end = -180 + (end-180)
		divisions[i]=(start,end)
		start=-180+(startingAngle + (angleAddition*(i-1)))
		end=-180+(startingAngle + (angleAddition*i))
		if start == -180:
			start = 180
	 	divisions[(numDivisions/2)+i] = (start,end)
	return divisions

def checkRegionOfRed(divisions, polarCoordinates):
	positives={}
	for c in polarCoordinates:
		for i in divisions:
			start, end = divisions.get(i)
			if c>=0:
				if c>=start and c<end:
					positives[c]=i
			else:
				if(start < 0 or end<0) and ( (abs(c)<abs(start) and (abs(c)>abs(end)))):
					positives[c] = i
	return positives

def drawRegions(image, divisions, keypoints):

	im = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	angles=[]
	for i in divisions:
		start, end = divisions.get(i)
		angles.append(start)

	count=1
	for angle in angles:
		length=360
		alpha = angle * math.pi / 180.0
		cos = math.cos(alpha)
		sin = math.sin(alpha)
		x= ( 360 - (length * cos))
		y= (360 - (length*sin))
		pt1=(360,360)
		pt2=(int(x),int(y))
		img2 = cv2.line(im, pt1, pt2, [255,255,255], thickness=1, lineType=8, shift=0)
		img2=cv2.putText(im,str(count), pt2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
		count+=1
	cv2.namedWindow('line', cv2.WINDOW_NORMAL)
	cv2.imshow('line', img2)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def printTubeStatus(positives, numDivisions):
	status={}
	positiveResults= positives.values()
	for i in range(numDivisions+1):
	 	if i in positiveResults:
	 		status[i] = 'positive'
	 	else:
			status[i] = 'negative'
	return status

def main(numDivisions, startAngle, filename):
	im = imageRead(filename)
	keypoints= detectBlobs(im)
	divisions=divideIntoRegions(startAngle,numDivisions)
	polarCoordinates = convertToPolarCoordinates(im, getBlobCoordinates(keypoints))
	positives = checkRegionOfRed(divisions, polarCoordinates)
	print positives
	print printTubeStatus(positives, 12)
	drawRegions(im, divisions, keypoints)

main(6, 30, "4tube720x720.jpg")