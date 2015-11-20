import cv2
import numpy as np;
import math
import argparse

def imageRead(filename):
	im = cv2.imread(filename)
	
	return im

def markdetect(im):
	boundaries = [
	([0,200,10], [10, 255, 50])]
	# 15 240 4 RGB  BGR = 4 240 15
	# marker is 48,255,0
	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")

	detector = cv2.SimpleBlobDetector_create()
	mask = cv2.inRange(im, lower, upper)
	keypoints = detector.detect(mask)
	cartesianCoordinates=[]
	count=0
	for i in keypoints:
		x = keypoints[count].pt[0] #i is the index of the blob you want to get the position
		y = keypoints[count].pt[1]
		cartesianCoordinates.append((x,y))
		count+=1
	return cartesianCoordinates

def detectBlobs(im):
	#Setting up parameters. 
	params = cv2.SimpleBlobDetector_Params()
	params.filterByArea = True
	params.minArea = 10
	params.maxArea = 500000
	# params.maxThreshold= 150
	# params.minThreshold = 100
	# params.filterByInertia = True
	# params.minInertiaRatio = 0.0000000001
	# params.maxInertiaRatio = 5
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

def drawBlobs(im, coordinates):
	for (x,y) in coordinates:
		im2 = cv2.circle(im, (int(x),int(y)), 100, (0,0,255), 8, 8, 0)
	# # im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.namedWindow("Keypoints", cv2.WINDOW_NORMAL)
	cv2.imshow("Keypoints", im2)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	# im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	# cv2.imshow("Keypoints", im_with_keypoints)
	# cv2.waitKey(0)

def convertToPolarCoordinates(im, cartesianCoordinates):
	height, width = im.shape[:2]
	center = [height/2, width/2]
	polarCoordinates=[]
	for i in cartesianCoordinates:
		polarCoordinates.append(math.degrees(math.atan2((center[1]-i[1]),(center[0]-i[0]))))

	return polarCoordinates

def blob(im):
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

def checkRegion(divisions, polarCoordinates):
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

def drawRegions(im, divisions, coordinates):
	for (x,y) in coordinates:
		im2 = cv2.circle(im, (int(x),int(y)), 100, (0,0,255), 8, 8, 0)
	# # im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	angles=[]
	for i in divisions:
		start, end = divisions.get(i)
		angles.append(start)

	count=1
	height, width = im.shape[:2]
	for angle in angles:
		length=width/2
		alpha = angle * math.pi / 180.0
		cos = math.cos(alpha)
		sin = math.sin(alpha)
		x= ( length - (length * cos))
		y= (length - (length*sin))
		pt1=(length,length)
		pt2=(int(x),int(y))
		im2 = cv2.line(im2, pt1, pt2, [255,255,255], thickness=5, lineType=8, shift=0)
		im2=cv2.putText(im2,str(count), pt2, cv2.FONT_HERSHEY_DUPLEX, 12, (255,255,255), thickness=3)
		count+=1
	cv2.namedWindow('line', cv2.WINDOW_NORMAL)
	cv2.imshow('line', im2)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def printTubeStatus(positives, numDivisions):
	status={}
	positiveResults= positives.values()
	for i in range(numDivisions):
	 	if i in positiveResults:
	 		status[i+1] = 'positive'
	 	else:
			status[i+1] = 'negative'
	return status

def main(numDivisions, startAngle, filename):
		#openCV reads the image	ap=argparse.ArgumentParser()
	ap=argparse.ArgumentParser()
	ap.add_argument("-i", "--image", help="path to the image")
	ap.add_argument("-d", "--divisions", help="number of divisions")
	ap.add_argument("-a", "--angle", help = "starting angle")
	args = vars(ap.parse_args())

	divisionNum = int(args["divisions"])
	startAngle=int(args["angle"])
	im = imageRead(args["image"])

	markerCoor= markdetect(im)
	markerPolar= convertToPolarCoordinates(im,markerCoor)
	divisions = divideIntoRegions(startAngle,divisionNum)
	keypoints = detectBlobs(im)

	redCoord = blob(im)
	redPolar = convertToPolarCoordinates(im, redCoord)
	positives= checkRegion(divisions, redPolar)
	print printTubeStatus(positives, divisionNum)
	markerRegion = checkRegion(divisions ,markerPolar)
	print "Marker in region: ", markerRegion.values()
	drawRegions(im, divisions, redCoord)
	# drawBlobs(im,redCoord)



	# markerDetect.main()
	# keypoints= detectBlobs(im)
	# divisions=divideIntoRegions(startAngle,numDivisions)
	# marker = getMarkerPolar(im, divisions, markerCoor)
	# print markerCoor
	# print "Marker in region: ", marker
	# polarCoordinates = convertToPolarCoordinates(im, getBlobCoordinates(keypoints))
	# positives = checkRegionOfRed(divisions, polarCoordinates)
	# print positives
	# print printTubeStatus(positives, 12)
	# drawRegions(im, divisions, keypoints)

main(6, 0, "tube10800x10800marker.jpg")