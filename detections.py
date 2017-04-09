import cv2
import numpy as np

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

hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

vid = cv2.VideoCapture(0)
while True:
    _,frame = vid.read()
    [gray, ffaces, fullbody] = multi_scale(frame)

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

    for (qx,qy,qw,qh) in ffaces:
        cv2.rectangle(frame, (qx,qy), (qx+qw,qy+qh), (255,0,255), 2)

    for (tx,ty,tw,th) in fullbody:
        cv2.rectangle(frame, (tx,ty), (tx+tw,ty+th), (255,34,255), 2)

            
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()
