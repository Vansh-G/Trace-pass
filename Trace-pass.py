import cv2
import numpy as np
import winsound #only for windows devices. Have given an alternative for cross-platform use 
import threading

def click_event(event, x, y, flags, param):
    global draw, a, b
    if event==cv2.EVENT_LBUTTONDOWN:
        a,b = x,y
        draw = 1
    elif event==cv2.EVENT_MOUSEMOVE:
        if draw == 1:
            frame = frame1
            cv2.imshow('frame', frame1)
            cv2.waitKey(1)

    elif event==cv2.EVENT_LBUTTONUP:
        cv2.rectangle(frame1, (a,b), (x,y), (0,0,255), 1)
        global rect
        rect = a,b,x,y
        draw = 0
        cv2.imshow("frame", frame1)
        cv2.waitKey(1)

global draw, frame1, rect
draw = 0
cap = cv2.VideoCapture('demo1.mp4')

ret, frame1 = cap.read()
ret, frame2 = cap.read()
rect = 0,0, frame1.shape[1], frame1.shape[0]
cv2.imshow("frame", frame1)
cv2.setMouseCallback('frame', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

while cap.isOpened():
    try:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        _, thresh = cv2.threshold(blur,20,255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        crop = dilated[rect[1]:rect[3], rect[0]:rect[2]]
        cv2.imshow("mask", dilated)
        contours,_ = cv2.findContours(crop, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.rectangle(frame1, (rect[0], rect[1]), (rect[2], rect[3]), (0,0,255), 2)
        for contour in contours:
            (x,y,w,h) = cv2.boundingRect(contour)
            
            if cv2.contourArea(contour)<300:
                continue
            cv2.rectangle(frame1, (rect[0]+x, rect[1]+y), (rect[0]+x+w, rect[1]+y+h), (0,255,0), 2)
            cv2.putText(frame1, "Intruder Found", (10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),3)
            threading.Thread(
            target=lambda: winsound.Beep(2000, 200)
            #Alternatively you can simply use " print('\a') " instead of
            # the winsound statement for cross platform compatibility. 
            ).start()
            

        cv2.imshow('feed', frame1)
        frame1 = frame2
        ret,frame2 = cap.read()
    except:
        print("Video Analysis Complete. Thank you!")
        break
        

    if cv2.waitKey(40)==27:
        break

cv2.destroyAllWindows()
cap.release()