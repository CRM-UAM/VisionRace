import numpy as np
import io
import cv2
import time
from crop import SlicePart
from picamera import PiCamera
from scipy.interpolate import griddata
from picamera.array import PiRGBArray

RESOLUTION = (240, 288)
dir = 0
DIV = 8
LADO = 51
cam = PiCamera()
cam.resolution = RESOLUTION
rawCapture = PiRGBArray(cam, size = RESOLUTION)

imgList=[]
pointsList=[]
warped = None

h = int(250/2)
w = 100

pts1 = np.float32([[w-66,h-96],[w-89,h-12],[w+90,h-12],[w+68,h-96]])
pts2 = np.float32([[w-LADO,h-LADO],[w-LADO,h+LADO],[w+LADO,h+LADO],[w+LADO,h-LADO]])

M_Perspective = cv2.getPerspectiveTransform(pts1,pts2)

time_1 = 0

t1 = time.clock()
grid_x, grid_y = np.mgrid[0:287:288j, 0:239:240j]
source = np.array([[0,0], [0,239],
			[86,79], [86,161],
			[137,66], [137,173],
                  [287,0],[287,239]])
destination = np.array([[0,6], [0,229],
			[147,92], [147,146],
			[199,89], [199,148],
                  [287,72],[287,167]])


grid_z = griddata(destination, source, (grid_x, grid_y), method='cubic')
map_x = np.append([], [ar[:,1] for ar in grid_z]).reshape(288,240)
map_y = np.append([], [ar[:,0] for ar in grid_z]).reshape(288,240)

dstMap1, dstMap2 = cv2.convertMaps(map_x.astype(np.float32), map_y.astype(np.float32), cv2.CV_16SC2)
print("Matrix Warp: " + str((time.clock()-t1)*1000) + ' ms')

for frame in cam.capture_continuous(rawCapture, format='bgr', use_video_port=True):
	frame = rawCapture.array
	rawCapture.truncate(0)

	warped = cv2.remap(frame, dstMap1, dstMap2,  cv2.INTER_LINEAR, warped, cv2.BORDER_REPLICATE)

	altura, anchura  = frame.shape[:2]
	_ , thresh = cv2.threshold(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),100,255,cv2.THRESH_BINARY_INV)
	sl = altura / DIV
	
	inx = []

	for i in range(DIV):
	    	altura = i*sl
	    	diff = np.diff(thresh[altura], n=2)
	    	inx.append(np.where(diff == diff.max())[0]) 
	

        # Display the resulting frame
        #out.write(vis)
        cv2.imshow('frame',frame)
      	del imgList[:]
        del pointsList[:]
 	del inx[:]
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break	
	print 'Loop: ' + str((time.clock()-t1)*1000) + ' ms'
	t1 = time.clock()

cap.release()
cv2.destroyAllWindows()
