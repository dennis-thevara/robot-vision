# ------------------------------------------------------------------------------
# Vision libraries:
# ------------------------------------------------------------------------------
import cv2
import numpy as np
# ------------------------------------------------------------------------------
# Arduino interfacing:
# ------------------------------------------------------------------------------
#from nanpy import ArduinoApi
#from nanpy import SerialManager
#from time import sleep


# ------------------------------------------------------------------------------
# Arduino connection setup:
# ------------------------------------------------------------------------------
#link = SerialManager(device='/dev/ttyACM0')
#link = SerialManager(device='COM5')
#A = ArduinoApi(connection=link)
#led = 13
# ------------------------------------------------------------------------------
# Video Processing:
# ------------------------------------------------------------------------------


def intersect(a,b):
	# COORDINATE DEFINITION FOR INTERSECTION RECTANGLE:
	if b[0] > a[2]:
		x1 = a[2]
	else:
		x1 = max(b[0],a[0])
	
	if b[2] < a[0]:
		x2 = a[0]
	else:
		x2 = min(b[2],a[2])
	
	y1 = b[1]
	y2 = b[3]
	return (x1,y1,x2,y2)
	


vid = cv2.VideoCapture(1)


while True:
    _,img = vid.read()
    	
    #DEFINING CENTRAL REGION OF INTEREST:
    roiH,roiW,_ = img.shape
    cv2.rectangle(img,(2*roiW/5,roiH),(3*roiW/5,0),(255,128,0),2)
    pointSetROI = [2*roiW/5,roiH,3*roiW/5,0]
	
    # Define centroids:
    ROI_Xcent = pointSetROI[0]+abs(pointSetROI[0]-pointSetROI[2])/2
    ROI_Ycent = pointSetROI[1]+abs(pointSetROI[1]-pointSetROI[3])/2

    StepSize = 8
    EdgeArray = []


    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   
    #imgGray = cv2.bilateralFilter(imgGray,9,30,30)              
    imgGray = cv2.GaussianBlur(img,(5,5),0)
    imgEdge = cv2.Canny(imgGray, 100, 200)           
    
    imagewidth = imgEdge.shape[1] - 1
    imageheight = imgEdge.shape[0] - 1
    
    for j in range (0,imagewidth,StepSize):    
        for i in range(imageheight-5,0,-1):    #step through every pixel in height of array from bottom to top
                                               #Ignore first couple of pixels as may trigger due to undistort
            if imgEdge.item(i,j) == 255:       #check to see if the pixel is white which indicates an edge has been found
                EdgeArray.append((j,i))        #if it is, add x,y coordinates to ObstacleArray
                break                          #if white pixel is found, skip rest of pixels in column
        else:                                  #no white pixel found
            EdgeArray.append((j,0))            #if nothing found, assume no obstacle. Set pixel position way off the screen to indicate
                                               #no obstacle detected
            
    
    #for x in range (len(EdgeArray)-1):      #draw lines between points in ObstacleArray 
    #    cv2.line(img, EdgeArray[x], EdgeArray[x+1],(0,255,0),1) 
    for x in range (len(EdgeArray)):        #draw lines from bottom of the screen to points in ObstacleArray
        cv2.line(img, (x*StepSize,imageheight), EdgeArray[x],(0,255,0),1)

    cv2.imshow('camera',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
            

vid.release()
cv2.destroyAllWindows()
