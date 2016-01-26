import cv2
import Image
import numpy as np;
import math
import argparse
import collections

## Most recent version -- end of Fall 2015

def imageMask(imageFile, maskFile):
	"""
	Combines the image from hardware with a mask image. Saves it in the repository.
	Returns the 
	"""
	background = Image.open(imageFile)
	foreground = Image.open(maskFile)

	Image.alpha_composite(background, foreground).save("maskedImage.png")
	im = cv2.imread("maskedImage.png") #to be able to access to the masked image later in case needed
	return im

def imageRead(filename):
	"""
	Reads in the image for opencv.
	"""
	im = cv2.imread(filename)	
	return im

def markdetect(im):
	"""
	Detects the green marker and returns its Cartesian coordinates.
	"""
	boundaries = [([0,200,0], [50, 255, 50])] # the range for green color to detect the marker.
	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")

	params = cv2.SimpleBlobDetector_Params()
	params.filterByColor=True
	params.blobColor=255
	detector = cv2.SimpleBlobDetector_create(params)
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
	"""
	Defines some properties of blood blobs. Returns the coordinates of the blobs that have these properties.
	"""
	#Setting up parameters. 
	params = cv2.SimpleBlobDetector_Params()
	params.filterByColor=True
	params.blobColor<150
	params.blobColor>50
	params.filterByConvexity=True
	params.minConvexity=0
	params.maxConvexity = 2
	params.filterByArea = True
	params.minArea = 70 #7
	params.maxArea = 900 #900
	params.maxThreshold= 5000
	params.minThreshold = 1
	params.filterByInertia = True
	params.minInertiaRatio = 0.1
	params.maxInertiaRatio = 5
	detector = cv2.SimpleBlobDetector_create(params)
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

def drawBlobs(im, coordinates, keypoints):
	for (x,y) in coordinates:
		im2 = cv2.circle(im, (int(x),int(y)), 30, (0,0,255), 3, 1, 0)
	im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.namedWindow("Keypoints", cv2.WINDOW_NORMAL)
	cv2.imshow("Keypoints", im)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

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
	print divisions
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
def updateDivisions(divisions, markerPolar, numberDivisions):
	for key, value in markerPolar.iteritems():
		markerCoord=value
	newDivisions={}
	for i in divisions.iterkeys():
		if [i-(markerCoord-i)]>1:
			newDivisions[i-(markerCoord-i)]=divisions[i]
		else:
			newDivisions[i-(markerCoord-i)+12]=divisions[i]
	print collections.OrderedDict(sorted(newDivisions.items()))
	return collections.OrderedDict(sorted(newDivisions.items()))

def drawRegions(im, divisions):
	# for (x,y) in coordinates:
		# im2 = cv2.circle(im, (int(x),int(y)), 30, (0,0,255), 8, 8, 0)
	# # im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	angles=[]
	for i in divisions:
		start, end = divisions.get(i)
		angles.append(start)
	counts ={}
	count=1
	height, width = im.shape[:2]
	im2=None
	for angle in angles:
		length=width/2
		alpha = angle * math.pi / 180.0
		cos = math.cos(alpha)
		sin = math.sin(alpha)
		x= ( length - (length * cos))
		y= (length - (length*sin))
		pt1=(length,length)
		pt2=(int(x),int(y))
		im2 = cv2.line(im, pt1, pt2, [255,255,255], thickness=5, lineType=8, shift=0)
		im2=cv2.putText(im2,str(count), (int(x),int(y)), cv2.FONT_HERSHEY_DUPLEX, 2, (255,255,255), thickness=2)
		counts[count]=pt2
		count+=1

	return im2

def printTubeStatus(positives, numDivisions):
	status={}
	positiveResults= positives.values()
	for i in range(1,numDivisions+1):
	 	if i in positiveResults:
	 		status[i] = 'positive'
	 	else:
			status[i] = 'negative'
	return status

def main(numDivisions, imageFile, maskFile):
	im = imageMask(imageFile, maskFile)
	markerCoor= markdetect(im)
	markerPolar= convertToPolarCoordinates(im,markerCoor)
	print markerPolar
	divisions = divideIntoRegions(markerPolar[0]-20,divisionNum)
	keypoints = detectBlobs(im)
	print checkRegion(divisions, markerPolar)

	redCoord = blob(im)
	redPolar = convertToPolarCoordinates(im, redCoord)
	positives= checkRegion(divisions, redPolar)
	print printTubeStatus(positives, divisionNum)
	drawBlobs(drawRegions(im,divisions),redCoord,keypoints)

if __name__ == '__main__':
	## detecting arguments given by the terminal command:
	ap=argparse.ArgumentParser()
	ap.add_argument("-i", "--image", help="path to the image")
	ap.add_argument("-d", "--divisions", help="number of divisions")
	ap.add_argument("-m", "--mask", help = "mask image")

	## what these arguments are:
	args = vars(ap.parse_args())
	divisionNum = int(args["divisions"])
	imageFile = args["image"]
	maskFile = args["mask"]
	
	##running the code
	main(divisionNum, imageFile, maskFile)
