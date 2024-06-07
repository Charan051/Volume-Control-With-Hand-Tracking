import cv2
import mediapipe as mp
import time


class handdetector():
    def __init__(self,mode=False,maxhands=2,modelcomp=1,detectioncon=0.5,trackcon=0.5):
        self.mode=mode
        self.maxhands=maxhands
        self.detectioncon=detectioncon
        self.trackcon=trackcon
        self.modelcomp=modelcomp
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxhands,self.modelcomp,self.detectioncon,self.trackcon)
        #to draw lines between handpoints
        self.mpdraw=mp.solutions.drawing_utils

    def findhands(self,img,draw=True):        
        imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgrgb)
        # print(results.multi_hand_landmarks)
        #to check multiple hands
        if self.results.multi_hand_landmarks:
            for hadnlms in self.results.multi_hand_landmarks:               
                # mpdraw.draw_landmarks(img,hadnlms)
                if draw:
                    self.mpdraw.draw_landmarks(img,hadnlms,self.mpHands.HAND_CONNECTIONS)

        return img
    
    def findpos(self,img,handno=0,draw=True):

        lmlist=[]
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handno]           

            for id,lm in enumerate(myhand.landmark):
                # print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                # print(id, cx , cy)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),4,(255,8,255),cv2.FILLED)
        return lmlist            


def main():
    ptime=0
    ctime=0
    cap=cv2.VideoCapture(0)
    detector=handdetector()


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



if __name__ == "__main__":
    main()