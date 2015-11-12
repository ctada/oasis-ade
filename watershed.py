import numpy as np
import cv2
from matplotlib import pyplot as pyplot

img = cv2.imread('4tube720x720.jpg')
height, width = img.shape[:2]
img2 = cv2.line(img, (720/4,0), (height/2,width/2), [255,255,255], thickness=1, lineType=8, shift=0)
img2 = cv2.line(img, (3*(720/4),720), (height/2,width/2), [255,255,255], thickness=1, lineType=8, shift=0)
img2 = cv2.line(img, (0,720), (height/2,width/2), [255,255,255], thickness=1, lineType=8, shift=0)
img2 = cv2.line(img, (720,0), (height/2,width/2), [255,255,255], thickness=1, lineType=8, shift=0)
# img2 = cv2.line(img, (720/2,0), (height/2,width/2), [255,255,255], thickness=1, lineType=8, shift=0)
img2 = cv2.line(img, (0,720/2), (height/2,width/2), [255,255,255], thickness=1, lineType=8, shift=0)
img2 = cv2.line(img, (720,720/2), (height/2,width/2), [255,255,255], thickness=1, lineType=8, shift=0)
# img2 = cv2.line(img, (720/2,720), (height/2,width/2), [255,255,255], thickness=1, lineType=8, shift=0)
cv2.namedWindow('line', cv2.WINDOW_NORMAL)
cv2.imshow('line', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()