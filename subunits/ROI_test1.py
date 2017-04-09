import cv2
import numpy as np

#img = cv2.imread('nature02.jpg')
vid = cv2.VideoCapture(0)

def intersect(a,b):
	# COORDINATE DEFINITION FOR INTERSECTION RECTANGLE:
	if b[0] < a[0]:
		x1 = a[0]
	elif a[0] < b[0] & b[0] < a[2]:
		x1 = b[0]
	else:
		x1 = b[0]
	
	if b[2] < a[2]:
		x2 = b[2]
	elif a[0] < b[2] & b[2] < a[2]:
		x2 = b[2]
	else:
		x2 = a[2]
	
	y1 = b[1]
	y2 = b[3]
	return (x1,y1,x2,y2)

while True:
	_,img = vid.read()
	
# Get dimensions of image and assign middle 3rd as ROI
	h,w,_ = img.shape
	cv2.rectangle(img,(w/3,h),(2*w/3,0),(255,128,0),2)
	cv2.rectangle(img,(w/5,h/2),(2*w/5,h/6),(0,0,255),2)
	cv2.rectangle(img,(3*w/5,h/3),(4*w/5,h/4),(0,0,255),2)
	cv2.rectangle(img,(w/6,4*h/5),(5*w/6,2*h/5),(0,0,255),2)
	
	pointSetROI = [w/3,h,2*w/3,0]
	pointSetBOX1 = [w/5,h/2,2*w/5,h/6]
	pointSetBOX2 = [3*w/5,h/3,4*w/5,h/4]
	pointSetBOX3 = [w/6,4*h/5,5*w/6,2*h/5]
	
	(X1,Y1,X2,Y2) = intersect(pointSetROI,pointSetBOX1)
	(Xa,Ya,Xb,Yb) = intersect(pointSetROI,pointSetBOX2)
	(Xaa,Yaa,Xbb,Ybb) = intersect(pointSetROI,pointSetBOX3)
	cv2.rectangle(img,(X1,Y1),(X2,Y2),(0,0,0),2)
	cv2.rectangle(img,(Xa,Ya),(Xb,Yb),(0,0,0),2)
	cv2.rectangle(img,(Xaa,Yaa),(Xbb,Ybb),(0,0,0),2)
	
	cv2.imshow('img',img)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
		
#print h, w
#cv2.imshow('img',img)
#cv2.waitKey(0)

cv2.destroyAllWindows()
vid.release()