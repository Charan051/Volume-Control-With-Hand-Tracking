import cv2
import mediapipe as mp
import time


cap=cv2.VideoCapture(0)

mpHands=mp.solutions.hands
hands=mpHands.Hands()
#to draw lines between handpoints
mpdraw=mp.solutions.drawing_utils

ptime=0
ctime=0

while True:
    success,img=cap.read()
    imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgrgb)
    # print(results.multi_hand_landmarks)
    #to check multiple hands
    if results.multi_hand_landmarks:
        for hadnlms in results.multi_hand_landmarks:
            for id,lm in enumerate(hadnlms.landmark):
                # print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                print(id, cx , cy)
                if id==0:
                    cv2.circle(img,(cx,cy),25,(255,8,255),cv2.FILLED)
            # mpdraw.draw_landmarks(img,hadnlms)
            mpdraw.draw_landmarks(img,hadnlms,mpHands.HAND_CONNECTIONS)

    #to get fps
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,8,255),3)
    cv2.imshow("image",img)
    cv2.waitKey(1)

