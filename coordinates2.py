import math

coordinates=[(0,0), (360,0), (720,0), (720,360), (720,720), (360,720), (0,720), (0,360)]
center = [(720/2, 720/2)]
for c in coordinates:
	coordinatesNew=[(center[0][0]-c[0],center[0][1]-c[1])]
	print math.degrees(math.atan2(coordinatesNew[0][1],coordinatesNew[0][0]))
