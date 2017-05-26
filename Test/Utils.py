import numpy as np
import cv2
import time
from Image import *

def SlicePart(im, images, slices):
    height, width = im.shape[:2]
    sl = int(height/slices);
    
    for i in range(slices):
        part = sl*i
        crop_img = im[part:part+sl, 0:width]
        images[i].image = crop_img
        _, images[i].thresh = cv2.threshold(cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY),100,255,cv2.THRESH_BINARY_INV)
        images[i].Process()
        
def SlicePartFibonacci(im, images, slices):
    fibo = [0,2,5,10,18,31]
    height, width = im.shape[:2]
    sl = int(height/fibo[slices-1]);
    
    for i in range(slices):
        part = sl*fibo[i]
        if i == 0:
            crop_img = im[part:int(part+sl), 0:width]
        else:
            if (i-1) == 0:
                crop_img = im[sl*fibo[i-1]+sl:part, 0:width]
            else:
                crop_img = im[sl*fibo[i-1]:part, 0:width]
        images[i].image = crop_img
        images[i].Process()
        
def PerspectiveWarp(img):
    height, width  = img.shape[:2]
    M_Translate = np.float32([[1,0,0],[0,1,162]])
    dst = cv2.warpAffine(img,M_Translate,(640,480))
    
    cX = (width/2)
    cY = (height/2) + 162
    LADO = 34
    
    pts1 = np.float32([[cX-66,cY-96],[cX-89,cY-12],[cX+90,cY-12],[cX+68,cY-96]])
    pts2 = np.float32([[cX-LADO,cY-LADO],[cX-LADO,cY+LADO],[cX+LADO,cY+LADO],[cX+LADO,cY-LADO]])

    M_Perspective = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(dst,M_Perspective,(640,480))
    
    return dst

def RepackImages(images):
    img = images[0].image
    for i in range(len(images)):
        if i == 0:
            img = np.concatenate((img, images[1].image), axis=0)
        if i > 1:
            img = np.concatenate((img, images[i].image), axis=0)
            
    return img

def Center(moments):
    if moments["m00"] == 0:
        return 0
        
    x = int(moments["m10"]/moments["m00"])
    y = int(moments["m01"]/moments["m00"])

    return x, y
    
def RemoveBackground(image, b):
    up = 100
    # create NumPy arrays from the boundaries
    lower = np.array([0, 0, 0], dtype = "uint8")
    upper = np.array([up, up, up], dtype = "uint8")
    #----------------COLOR SELECTION-------------- (Remove any area that is whiter than 'upper')
    if b == True:
        mask = cv2.inRange(image, lower, upper)
        image = cv2.bitwise_and(image, image, mask = mask)
        image = cv2.bitwise_not(image, image, mask = mask)
        image = (255-image)
        return image
    else:
        return image
    #////////////////COLOR SELECTION/////////////
    