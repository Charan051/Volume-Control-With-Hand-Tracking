import cv2
import time
import numpy as np
import handtrackingmodule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#setting image height and width
wcam,hcam=640,480

cap=cv2.VideoCapture(0)
#setting image weidth and height
cap.set(3,wcam)
cap.set(4,hcam)
ptime=0
#creating an object
#detectioncon increases accuracy of detecting the hands
detector=htm.handdetector(detectioncon=0.7)

#pycaw usage
#initializations start
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#initialization ends
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()
minvol=volrange[0]
maxvol=volrange[1]






while True:
    s,img=cap.read()
    #to find hands
    img=detector.findhands(img)
    lmlist=detector.findpos(img,draw=False)
    if len(lmlist)!=0:
        # print(lmlist[4],lmlist[8])
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        #getting center point between  line from thumb to index
        cx,cy=(x1+x2)//2,(y1+y2)//2

        #putting  circles on thumb and index
        cv2.circle(img,(x1,y1),7,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),7,(255,0,255),cv2.FILLED)
        #joining thumb and indexx with a line
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),7,(255,0,255),cv2.FILLED)

        #to get length of line
        length=math.hypot(x2-x1,y2-y1)
        # print(length)
        
        #handrange 20-130
        #vol range -65-0
        vol=np.interp(length,[20,130],[minvol,maxvol])
        volume.SetMasterVolumeLevel(vol, None)

        # print(int(length),vol)


        if length<20:
             cv2.circle(img,(cx,cy),7,(0,255,0),cv2.FILLED)



    
    #fps
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,str(int(fps)),(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

    cv2.imshow("img",img)
    cv2.waitKey(1)