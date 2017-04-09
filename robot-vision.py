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

frontalface_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
fullbody_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

def multi_scale(frame):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ffaces = frontalface_cascade.detectMultiScale(gray, 1.3, 5)
    fullbody = fullbody_cascade.detectMultiScale(gray, 1.3, 5)
    return gray, ffaces, fullbody

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

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
	
hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

vid = cv2.VideoCapture(0)
while True:
    _,frame = vid.read()
    [gray, ffaces, fullbody] = multi_scale(frame)
	
	#DEFINING CENTRAL REGION OF INTEREST:
    roiH,roiW,_ = frame.shape
    cv2.rectangle(frame,(roiW/3,roiH),(2*roiW/3,0),(255,128,0),2)
    pointSetROI = [roiW/3,roiH,2*roiW/3,0]

    found,w=hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
    found_filtered = []
    for ri, r in enumerate(found):
        for qi, q in enumerate(found):
            if ri != qi and inside(r, q):
                break
            else:
                found_filtered.append(r)
    draw_detections(frame,found)
    draw_detections(frame, found_filtered, 3)
	
	
	# FACE DETECTIONS:
    for (qx,qy,qw,qh) in ffaces:
        cv2.rectangle(frame, (qx,qy), (qx+qw,qy+qh), (255,0,255), 2)
		# Begin checking for overlap with ROI:
        pointSetFACE = [qx,qy,qx+qw,qy+qh]
        (X1,Y1,X2,Y2) = intersect(pointSetROI,pointSetFACE)
        cv2.rectangle(frame,(X1,Y1),(X2,Y2),(0,0,0),2)
        # Calculate overlap area:
        overlapBox = np.int0([[X1,Y1],[X2,Y1],[X2,Y2],[X1,Y2]])
        print cv2.contourArea(overlapBox)
	#print "face" # print face if face detected

	# UPPER BODY DETECTIONS:
    for (tx,ty,tw,th) in fullbody:
        cv2.rectangle(frame, (tx,ty), (tx+tw,ty+th), (255,34,255), 2)

            
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
