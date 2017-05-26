import numpy as np
import cv2
from Utils import PerspectiveWarp

class Image:
    
    def __init__(self):
        self.image = None
        self.contourCenterX = 0
        self.MainContour = None
        
    def Process(self):
        self.dir = 0
        altura, anchura  = self.image.shape[:2]
        sl = altura / 4
        for i in range(4):
            cv2.line(self.image,(0,i*sl),(640,i*sl),(255,0,0),1)
            for j in range(640):
                if (j+1) < 640:
                    if abs(int(self.thresh[i*sl,j])-int(self.thresh[i*sl,j+1])) > 250:
                        cv2.circle(self.image, (j,i*sl), 2, (255,255,255), -1)
                        self.dir += (anchura-j)/100
         
    def getContourCenter(self, contour):
        M = cv2.moments(contour)
        
        if M["m00"] == 0:
            return 0
        
        x = int(M["m10"]/M["m00"])
        y = int(M["m01"]/M["m00"])
        
        return [x,y]
        
    def getContourExtent(self, contour):
        area = cv2.contourArea(contour)
        x,y,w,h = cv2.boundingRect(contour)
        rect_area = w*h
        if rect_area > 0:
            return (float(area)/rect_area)
            
    def Aprox(self, a, b, error):
        if abs(a - b) < error:
            return True
        else:
            return False
            
    def correctMainContour(self, prev_cx):
        if abs(prev_cx-self.contourCenterX) > 5:
            for i in range(len(self.contours)):
                if self.getContourCenter(self.contours[i]) != 0:
                    tmp_cx = self.getContourCenter(self.contours[i])[0]
                    if self.Aprox(tmp_cx, prev_cx, 5) == True:
                        self.MainContour = self.contours[i]
                        if self.getContourCenter(self.MainContour) != 0:
                            self.contourCenterX = self.getContourCenter(self.MainContour)[0]