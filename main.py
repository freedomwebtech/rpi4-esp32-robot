import cv2
import numpy as np
import paho.mqtt.client as mqtt
from time import sleep

 
cap=cv2.VideoCapture(0)

ret,frame=cap.read()
frame=cv2.resize(frame,(840,480))
cx1,cy1=840//2,480//2
lower_range=np.array([79,134,57])
upper_range=np.array([125,255,255])

count=0

def stop():
    mqttBroker ="mqtt.fluux.io"
    client = mqtt.Client("raspberry pi 40")
    client.connect(mqttBroker)
    client.publish("test2",(bytes("stop",'utf-8')))
def turn():
    mqttBroker ="mqtt.fluux.io"
    client = mqtt.Client("raspberry pi 40")
    client.connect(mqttBroker)
    client.publish("test2",(bytes("turn",'utf-8')))
def turn1():
    mqttBroker ="mqtt.fluux.io"
    client = mqtt.Client("raspberry pi 40")
    client.connect(mqttBroker)
    client.publish("test2",(bytes("turn1",'utf-8')))
def forward():
    mqttBroker ="mqtt.fluux.io"
    client = mqtt.Client("raspberry pi 40")
    client.connect(mqttBroker)
    client.publish("test2",(bytes("forward",'utf-8')))


def obj_data(img):
     obj_width = 0

     hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
     mask=cv2.inRange(hsv,lower_range,upper_range)
     _,mask1=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
     cnts,_=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
     stop()
     for c in cnts:
        x=800
        if cv2.contourArea(c)>x:
            x,y,w,h=cv2.boundingRect(c)
            found_area = w * h
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            cv2.circle(frame, (cx, cy), 7, (0, 0, 255), -1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.line(frame,(cx,0),(cx,480),(0,0,255),2)
            print(cx,cx1)
            if cx > 414:
                print('turn clockwise')
                turn1()
                cv2.putText(img, 'turn clockwise', (630, 35),cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,0,0), 2)

            if cx < 262:
                print('turn1 anti-clockwise')
                turn()
                cv2.putText(img, 'turn1 anti-clockwise', (30, 35),cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,0,0), 2)

            if 262 < cx < 414:
                print("forward")
                forward()
                cv2.putText(img, 'forward', (403, 35),cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,0,0), 2)

                
while True:
    ret,frame=cap.read()
    count += 1
    if count % 14 != 0:
        continue

   
    frame=cv2.resize(frame,(840,480))
    frame=cv2.flip(frame,1)
    obj_data(frame) 
    cv2.circle(frame, (cx1, cy1), 7, (0, 0, 255), -1)
   
    cv2.imshow("FRAME",frame)
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()
