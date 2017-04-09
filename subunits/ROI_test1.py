import cv2
import numpy as np

#img = cv2.imread('nature02.jpg')
vid = cv2.VideoCapture(0)

while True:
	_,img = vid.read()
	
# Get dimensions of image and assign middle 3rd as ROI
	h,w,_ = img.shape
	cv2.rectangle(img,(w/3,h),(2*w/3,0),(255,128,0),2) 
	
	cv2.imshow('img',img)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
		
#print h, w
#cv2.imshow('img',img)
#cv2.waitKey(0)

cv2.destroyAllWindows()
vid.release()