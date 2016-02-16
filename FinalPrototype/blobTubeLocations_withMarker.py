import cv2
import Image
import numpy as np;
import math
import argparse
import collections

## Most recent version -- end of Fall 2015

class bloodBlobDetection(object):

	def __init__(self, inputs):
		### Input Parameters
		self.imageFile=inputs[0]
		self.maskFile=inputs[1]
		self.numDiv= int(inputs[2])

		### Intermediate Parameters
		self.maskedIm = None
		self.markerCartesian=[]
		self.keypoints = None
		self.blobCartesian=[]
		self.blobPolar=[]
		self.markerPolar=[]
		self.positiveResults={}
		self.divisionBorders = {}
		self.blobIm = None

		### Output Parameters
		self.results={}
		self.finalIm=None

	def main(self):

		self.imageMask()
		self.markdetect()
		self.markerPolar = self.convertToPolarCoordinates(self.markerCartesian)
		self.divideIntoRegions()
		self.detectBlobs()
		self.detectBlobs()
		self.getBlobCoordinates()
		self.blobPolar=self.convertToPolarCoordinates(self.blobCartesian)
		self.checkRegion()
		self.drawBlobs()
		self.drawRegions()
		self.printTubeStatus()


########################################################## BASIC METHODS #########################################################################

	def imageMask(self):
		"""
		Combines the image from hardware with a mask image. Saves it in the repository.
		Returns the masked image.
		"""
		background = Image.open(self.imageFile)
		foreground = Image.open(self.maskFile)

		Image.alpha_composite(background, foreground).save("maskedImage.png")
		self.maskedIm = cv2.imread("maskedImage.png") #to be able to access to the masked image later in case needed
		return self.maskedIm

	def markdetect(self):
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
		mask = cv2.inRange(self.maskedIm, lower, upper)

		keypoints = detector.detect(mask)
		count=0
		for i in keypoints:
			x = keypoints[count].pt[0] #i is the index of the blob you want to get the position
			y = keypoints[count].pt[1]
			self.markerCartesian.append((x,y))
			count+=1
		return self.markerCartesian

	def detectBlobs(self):
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
		self.keypoints = detector.detect(self.maskedIm)
		return self.keypoints

	def getBlobCoordinates(self):
		count=0
		for i in self.keypoints:
			x = self.keypoints[count].pt[0] #i is the index of the blob you want to get the position
			y = self.keypoints[count].pt[1]
			self.blobCartesian.append((x,y))
			count+=1
		return self.blobCartesian

	def drawBlobs(self):
		# im2=None
		# for (x,y) in self.blobCartesian:
		# 	im2 = cv2.circle(self.maskedIm, (int(x),int(y)), 30, (0,0,255), 3, 1, 0)
		self.blobIm = cv2.drawKeypoints(self.maskedIm, self.keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	def convertToPolarCoordinates(self, cartesianCoordinates):
		height, width = self.maskedIm.shape[:2]
		center = [height/2, width/2]
		polarCoordinates=[]
		for i in cartesianCoordinates:
			polarCoordinates.append(math.degrees(math.atan2((center[1]-i[1]),(center[0]-i[0]))))

		return polarCoordinates


	def divideIntoRegions(self):
		angleAddition = 360/self.numDiv

		for i in range(1,(self.numDiv/2)+1):
			start = -15 + (angleAddition*(i-1)) 
			if start > 180:
				start = -180 + (start-180)
			end = -15 + (angleAddition*i)
			if end > 180:
				end = -180 + (end-180)
			self.divisionBorders[i]=(start,end)
			start=-180+(-15 + (angleAddition*(i-1)))
			end=-180+(-15 + (angleAddition*i))
			if start == -180:
				start = 180
		 	self.divisionBorders[(self.numDiv/2)+i] = (start,end)
		return self.divisionBorders

	def checkRegion(self):
		for c in self.blobPolar:
			for i in self.divisionBorders:
				start, end = self.divisionBorders.get(i)
				if c>=0:
					if c>=start and c<end:
						self.positiveResults[c]=i
				else:
					if(start < 0 or end<0) and ( (abs(c)<abs(start) and (abs(c)>abs(end)))):
						self.positiveResults[c] = i
		return self.positiveResults

	def updateDivisions(self):
		for key, value in self.markerPolar.iteritems():
			markerCoord=value
		newDivisions={}
		for i in self.divisionBorders.iterkeys():
			if [i-(markerCoord-i)]>1:
				newDivisions[i-(markerCoord-i)]=self.divisionBorders[i]
			else:
				newDivisions[i-(markerCoord-i)+12]=self.divisionBorders[i]
		self.newDivisions=collections.OrderedDict(sorted(newDivisions.items()))
		return self.newDivisions

	def drawRegions(self):
		# for (x,y) in coordinates:
			# im2 = cv2.circle(im, (int(x),int(y)), 30, (0,0,255), 8, 8, 0)
		# # im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		angles=[]
		for i in self.divisionBorders:
			start, end = self.divisionBorders.get(i)
			angles.append(start)
		counts ={}
		count=1
		height, width = self.maskedIm.shape[:2]
		for angle in angles:
			length=width/2
			alpha = angle * math.pi / 180.0
			cos = math.cos(alpha)
			sin = math.sin(alpha)
			x= ( length - (length * cos))
			y= (length - (length*sin))
			pt1=(length,length)
			pt2=(int(x),int(y))
			self.finalIm = cv2.line(self.blobIm, pt1, pt2, [255,255,255], thickness=5, lineType=8, shift=0)
			self.finalIm =cv2.putText(self.blobIm,str(count), (int(x),int(y)), cv2.FONT_HERSHEY_DUPLEX, 2, (255,255,255), thickness=2)
			counts[count]=pt2
			count+=1
		
		cv2.namedWindow("Keypoints", cv2.WINDOW_NORMAL)
		cv2.imshow("Keypoints", self.finalIm)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def printTubeStatus(self):
		positiveResults= self.positiveResults.values()
		for i in range(1,self.numDiv+1):
		 	if i in positiveResults:
		 		self.results[i] = ['positive',5]
		 		# self.results[i] = 'positive'
		 	else:
				self.results[i] = ['negative',1]
				# self.results[i] = 'negative'
		return self.results


# if __name__ == '__main__':
# 	## detecting arguments given by the terminal command:
# 	ap=argparse.ArgumentParser()
# 	ap.add_argument("-i", "--image", help="path to the image")
# 	ap.add_argument("-d", "--divisions", help="number of divisions")
# 	ap.add_argument("-m", "--mask", help = "mask image")

# 	## what these arguments are:
# 	args = vars(ap.parse_args())
# 	divisionNum = int(args["divisions"])
# 	imageFile = args["image"]
# 	maskFile = args["mask"]
	
# 	##running the code
# 	b= bloodBlobDetection(numDiv=divisionNum, imageFile=imageFile, maskFile=maskFile)
# 	b.main()