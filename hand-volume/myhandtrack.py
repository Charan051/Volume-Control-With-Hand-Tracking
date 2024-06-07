import cv2
import mediapipe as mp
import time
import handtrackingmodule as htm

ptime=0
ctime=0
cap=cv2.VideoCapture(0)
detector=htm.handdetector()


while True:
    success,img=cap.read()
    img=detector.findhands(img)
    lmlist=detector.findpos(img)
    if len(lmlist)!=0:
        print(lmlist[4])
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,8,255),3)
    cv2.imshow("image",img)
    cv2.waitKey(1)