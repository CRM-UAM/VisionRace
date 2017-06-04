import numpy as np
import cv2
import time

LADO = 51
X = 0
Y = 0
DIV = 8
RESOLUTION = (240, 288)

def nothing(x):
    pass

img = cv2.imread('persp2.png')
cv2.namedWindow('image')

rows,cols,ch = img.shape
height, width  = img.shape[:2]
height /= 2
width /= 2

#cv2.createTrackbar('Lado', 'image', 30, 100, nothing)
#cv2.createTrackbar('X', 'image', 1, 200, nothing)
#cv2.createTrackbar('Y', 'image', 1, 200, nothing)

#LADO = cv2.getTrackbarPos('Lado','image')
X = cv2.getTrackbarPos('X','image')
Y = cv2.getTrackbarPos('Y','image')

cX = width + X
cY = height + Y

pts1 = np.float32([[cX-66,cY-96],[cX-89,cY-12],[cX+90,cY-12],[cX+68,cY-96]])
pts2 = np.float32([[cX-LADO,cY-LADO],[cX-LADO,cY+LADO],[cX+LADO,cY+LADO],[cX+LADO,cY-LADO]])

M_Perspective = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(img,M_Perspective,RESOLUTION)

imgray = cv2.cvtColor(dst,cv2.COLOR_BGR2GRAY) #Convert to Gray Scale
ret, thresh = cv2.threshold(imgray,122,255,cv2.THRESH_BINARY_INV) #Get Threshold
            
altura, anchura  = img.shape[:2]
sl = altura / DIV

centers = []

t1 = time.clock()
for i in range(DIV):
    altura = i*sl
    diff = np.diff(thresh[altura], n=2)
    inx = np.where(diff == diff.max())[0]
    for j in range(len(inx)):
        #cv2.circle(dst, (inx[j],altura), 2, (255,255,255), -1)
        print(str(altura) + " " + str(inx[j]))
        
print 'Derivada: ' + str((time.clock()-t1)*1000) + ' ms'
t1 = time.clock()
for i in range(DIV):
    altura = i*sl
    diff = np.diff(thresh[altura], n=2)
    inx = np.where(diff == diff.max())[0]
    test = thresh[int(altura-5):int(altura+5), int(inx[0]-5):int(inx[0]+5)]
    
print 'Squares: ' + str((time.clock()-t1)*1000) + ' ms'
cv2.imshow('image', test)
cv2.imwrite("test.png", test)

if cv2.waitKey(0) == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
#if cv2.waitKey(1) & 0xFF == ord('q'):
#    break
