import cv2

#openCV reads the image
im = cv2.imread("4tube720x720.jpg")
im2= cv2.bilateralFilter(im, 15, 25, 15, 15)
cv2.namedWindow("Bilateral", cv2.WINDOW_NORMAL)
cv2.imshow("Bilateral", im2)
cv2.waitKey(0)